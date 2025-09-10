#!/usr/bin/env python3
"""
Check if code formatting tools are installed and working
"""
import subprocess
import sys


def check_tool(tool_name, import_name=None):
    """Check if a tool is installed and working."""
    try:
        if import_name:
            __import__(import_name)
            print(f"✅ {tool_name} is installed (import check)")
        else:
            result = subprocess.run(
                [sys.executable, "-m", tool_name, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                version = result.stdout.strip() or result.stderr.strip()
                print(f"✅ {tool_name} is installed: {version}")
            else:
                print(f"❌ {tool_name} is not working properly")
                return False
    except ImportError:
        print(f"❌ {tool_name} is not installed (pip install {tool_name})")
        return False
    except subprocess.TimeoutExpired:
        print(f"❌ {tool_name} timed out")
        return False
    except FileNotFoundError:
        print(f"❌ {tool_name} is not installed")
        return False
    except Exception as e:
        print(f"❌ Error checking {tool_name}: {e}")
        return False
    return True


def main():
    """Check all formatting tools."""
    print("🔍 Checking code formatting tools...\n")

    tools = [
        ("black", None),
        ("isort", None),
        ("flake8", None),
        ("autopep8", None),
    ]

    all_good = True
    for tool, import_name in tools:
        if not check_tool(tool, import_name):
            all_good = False

    print()
    if all_good:
        print("🎉 All formatting tools are ready!")
        print("Run 'python scripts/format_code.py' to format your code.")
    else:
        print("⚠️  Some tools are missing. Install them with:")
        print("pip install black isort flake8 autopep8")

    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())
