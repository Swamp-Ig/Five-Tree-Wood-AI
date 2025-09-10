#!/usr/bin/env python3
"""
Format all Python files in the project using Black and isort
"""
import sys
from pathlib import Path

# Try to import the formatting tools directly
try:
    import black
    import isort
    import pylint.lint

    TOOLS_AVAILABLE = True
except ImportError:
    TOOLS_AVAILABLE = False


def run_black(src_dir, check_only=False):
    """Run Black formatter directly."""
    try:
        if not TOOLS_AVAILABLE:
            print("❌ Black not available - install with: pip install black")
            return False

        mode = black.FileMode()
        if check_only:
            # Check if files would be reformatted
            changed_files = []
            for py_file in src_dir.rglob("*.py"):
                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        original = f.read()
                    formatted = black.format_str(original, mode=mode)
                    if original != formatted:
                        changed_files.append(py_file)
                except (OSError, black.InvalidInput):
                    continue

            if changed_files:
                print(f"Would reformat {len(changed_files)} files:")
                for file in changed_files[:5]:  # Show first 5
                    print(f"  {file}")
                if len(changed_files) > 5:
                    print(f"  ... and {len(changed_files) - 5} more")
                return False
            else:
                print("All files already formatted")
                return True
        else:
            # Format files
            formatted_count = 0
            for py_file in src_dir.rglob("*.py"):
                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        original = f.read()
                    formatted = black.format_str(original, mode=mode)
                    if original != formatted:
                        with open(py_file, "w", encoding="utf-8") as f:
                            f.write(formatted)
                        formatted_count += 1
                except (OSError, black.InvalidInput) as e:
                    print(f"Error formatting {py_file}: {e}")
                    continue

            if formatted_count > 0:
                print(f"Reformatted {formatted_count} files")
            else:
                print("No files needed formatting")
            return True

    except (OSError, black.InvalidInput) as e:
        print(f"Error running Black: {e}")
        return False


def run_isort(src_dir, check_only=False):
    """Run isort directly."""
    try:
        if not TOOLS_AVAILABLE:
            print("❌ isort not available - install with: pip install isort")
            return False

        config = isort.Config(profile="black")

        if check_only:
            # Check if imports would be sorted
            changed_files = []
            for py_file in src_dir.rglob("*.py"):
                try:
                    if not isort.check_file(py_file, config=config):
                        changed_files.append(py_file)
                except OSError:
                    continue

            if changed_files:
                print(f"Would sort imports in {len(changed_files)} files:")
                for file in changed_files[:5]:  # Show first 5
                    print(f"  {file}")
                if len(changed_files) > 5:
                    print(f"  ... and {len(changed_files) - 5} more")
                return False
            else:
                print("All imports already sorted")
                return True
        else:
            # Sort imports
            sorted_count = 0
            for py_file in src_dir.rglob("*.py"):
                try:
                    result = isort.file(py_file, config=config)
                    if result:
                        sorted_count += 1
                except (OSError, isort.exceptions.FileSkipped) as e:
                    print(f"Error sorting {py_file}: {e}")
                    continue

            if sorted_count > 0:
                print(f"Sorted imports in {sorted_count} files")
            else:
                print("No files needed import sorting")
            return True

    except (OSError, isort.exceptions.FileSkipped) as e:
        print(f"Error running isort: {e}")
        return False



def run_pylint(src_dir):
    """Run pylint directly."""
    try:
        if not TOOLS_AVAILABLE:
            print("❌ pylint not available - install with: pip install pylint")
            return False

        # Run pylint on the source directory
        args = [str(src_dir)]
        result = pylint.lint.Run(args)
        if result.linter.msg_status == 0:
            print("No style issues found")
            return True
        else:
            print(f"Pylint found issues (exit code {result.linter.msg_status})")
            return False
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error running pylint: {e}")
        return False


def main():
    """Main formatting function."""
    # Get project root (parent of scripts directory)
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"

    print("🚀 Starting PEP8 code formatting...")
    print(f"📁 Project root: {project_root}")
    print(f"📁 Source directory: {src_dir}")

    # Check if source directory exists
    if not src_dir.exists():
        print(f"❌ Source directory not found: {src_dir}")
        return 1

    if not TOOLS_AVAILABLE:
        print("❌ Formatting tools not available. Install with:")
        print("pip install black isort pylint")
        return 1

    # Check import order with isort
    print("\n🔧 Checking import order with isort...")
    isort_success = run_isort(src_dir, check_only=True)

    if not isort_success:
        print("🔧 Fixing import order...")
        run_isort(src_dir, check_only=False)
    else:
        print("✅ Import order check completed successfully")

    # Check code format with black
    print("\n🔧 Checking code format with black...")
    black_success = run_black(src_dir, check_only=True)

    if not black_success:
        print("🔧 Formatting code...")
        run_black(src_dir, check_only=False)
    else:
        print("✅ Code format check completed successfully")


    # Check for style issues with pylint
    print("\n🔧 Checking code style with pylint...")
    pylint_success = run_pylint(src_dir)
    if pylint_success:
        print("✅ Code style check completed successfully")

    print("\n✨ Code formatting complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
