#!/usr/bin/env python3
"""
Install git pre-commit hooks for automatic code formatting
"""
import os
import shutil
import stat
from pathlib import Path


def install_hooks():
    """Install the pre-commit hook."""
    # Get project root (parent of scripts directory)
    project_root = Path(__file__).parent.parent
    git_dir = project_root / ".git"

    if not git_dir.exists():
        print("❌ No git repository found. Initialize git first with 'git init'")
        return False

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)

    # Create the pre-commit hook
    hook_file = hooks_dir / "pre-commit"
    scripts_dir = project_root / "scripts"
    hook_content = f"""#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '{scripts_dir}')
from pre_commit_hook import run_formatters

if __name__ == "__main__":
    success = run_formatters()
    sys.exit(0 if success else 1)
"""

    hook_file.write_text(hook_content)

    # Make the hook executable
    current_permissions = hook_file.stat().st_mode
    hook_file.chmod(current_permissions | stat.S_IEXEC)

    print("✅ Pre-commit hook installed successfully!")
    print("📋 The hook will automatically format Python files before each commit.")
    return True


if __name__ == "__main__":
    success = install_hooks()
    if not success:
        exit(1)
