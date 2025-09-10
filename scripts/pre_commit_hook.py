#!/usr/bin/env python3
"""
Pre-commit hook to automatically format code before commits
Install this by running: python scripts/install_hooks.py
"""
import subprocess
import sys
from pathlib import Path

# Try to import the formatting tools directly
try:
    import black
    import isort

    TOOLS_AVAILABLE = True
except ImportError:
    TOOLS_AVAILABLE = False


def format_file_with_tools(file_path):
    """Format a single file using black and isort directly."""
    try:
        if not TOOLS_AVAILABLE:
            print("❌ Formatting tools not available")
            return False

        file_path = Path(file_path)
        if not file_path.exists():
            return True

        # Read the original file
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        # Sort imports with isort
        sorted_content = isort.code(
            original_content, config=isort.Config(profile="black")
        )

        # Format with black
        mode = black.FileMode()
        formatted_content = black.format_str(sorted_content, mode=mode)

        # Write back if changed
        if original_content != formatted_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(formatted_content)
            return True  # File was changed

        return True  # File was already formatted

    except Exception as e:
        print(f"❌ Error formatting {file_path}: {e}")
        return False


def run_formatters():
    """Run code formatters on staged Python files."""
    try:
        if not TOOLS_AVAILABLE:
            print(
                "❌ Formatting tools not available. Install with: pip install black isort"
            )
            return False

        # Get list of staged Python files using subprocess
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return True  # No git repo, skip hook

        staged_files = [
            f for f in result.stdout.strip().split("\n") if f.endswith(".py") and f
        ]

        if not staged_files:
            return True  # No Python files staged

        print(f"🔧 Formatting {len(staged_files)} Python files...")

        # Format staged files directly
        for file in staged_files:
            if format_file_with_tools(file):
                # Re-stage the formatted file
                subprocess.run(["git", "add", file], check=True)
            else:
                print(f"❌ Failed to format {file}")
                return False

        print("✅ Code formatting complete!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Formatting failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error in pre-commit hook: {e}")
        return False


if __name__ == "__main__":
    success = run_formatters()
    sys.exit(0 if success else 1)
