#!/usr/bin/env python3
"""
Futurix AI - Installation Verification Script
Checks all dependencies and system requirements
"""

import sys
import os
import importlib
from typing import Tuple, List


def print_header(text: str):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version() -> Tuple[bool, str]:
    """Check Python version"""
    version = sys.version_info
    required = (3, 8)

    if version >= required:
        return True, f"✅ Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"❌ Python {version.major}.{version.minor} (requires 3.8+)"


def check_package(package_name: str, import_name: str = None) -> Tuple[bool, str]:
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name

    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'unknown')
        return True, f"✅ {package_name} ({version})"
    except ImportError:
        return False, f"❌ {package_name} (not installed)"


def check_command(command: str) -> Tuple[bool, str]:
    """Check if a system command is available"""
    result = os.system(f"which {command} > /dev/null 2>&1")
    if result == 0:
        return True, f"✅ {command}"
    else:
        return False, f"❌ {command} (not found)"


def check_directory(path: str) -> Tuple[bool, str]:
    """Check if a directory exists"""
    if os.path.exists(path) and os.path.isdir(path):
        return True, f"✅ {path}/"
    else:
        return False, f"❌ {path}/ (missing)"


def check_file(path: str) -> Tuple[bool, str]:
    """Check if a file exists"""
    if os.path.exists(path) and os.path.isfile(path):
        return True, f"✅ {path}"
    else:
        return False, f"⚠️  {path} (missing - optional)"


def main():
    """Run all checks"""
    print_header("FUTURIX AI - Installation Verification")

    all_passed = True

    # Check Python version
    print_header("1. Python Version")
    passed, msg = check_python_version()
    print(msg)
    all_passed = all_passed and passed

    # Check core packages
    print_header("2. Core Python Packages")
    packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("python-multipart", "multipart"),
        ("requests", "requests"),
        ("pdf2image", "pdf2image"),
        ("Pillow", "PIL"),
        ("pandas", "pandas"),
        ("fuzzywuzzy", "fuzzywuzzy"),
    ]

    for package, import_name in packages:
        passed, msg = check_package(package, import_name)
        print(msg)
        all_passed = all_passed and passed

    # Check optional packages
    print_header("3. Optional Packages (Gmail)")
    optional_packages = [
        ("google-api-python-client", "googleapiclient"),
        ("google-auth-httplib2", "google_auth_httplib2"),
        ("google-auth-oauthlib", "google_auth_oauthlib"),
    ]

    for package, import_name in optional_packages:
        passed, msg = check_package(package, import_name)
        print(msg)

    # Check system commands
    print_header("4. System Commands")
    commands = ["pdftoppm", "pdfinfo"]

    for cmd in commands:
        passed, msg = check_command(cmd)
        print(msg)
        if not passed:
            print("   Note: Install poppler-utils for PDF support")
            print("   macOS: brew install poppler")
            print("   Linux: sudo apt-get install poppler-utils")

    # Check project structure (new paths)
    print_header("5. Project Structure")

    files = [
        "run.py",
        "requirements.txt",
        "src/api/main.py",
        "src/services/ocr_service.py",
        "src/core/comparison.py",
        "src/core/storage.py",
        "public/index.html",
    ]

    for file in files:
        passed, msg = check_file(file)
        print(msg)
        all_passed = all_passed and passed

    # Check directories (new structure)
    directories = [
        "data/uploads",
        "data/exports",
        "data/samples",
    ]

    for directory in directories:
        passed, msg = check_directory(directory)
        print(msg)
        if not passed:
            print(f"   Creating {directory}/")
            os.makedirs(directory, exist_ok=True)

    # Summary
    print_header("Installation Summary")

    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("\nYou can now start the server:")
        print("  python run.py")
        print("\nOr directly with uvicorn:")
        print("  uvicorn src.api.main:app --reload")
        print("\nAPI will be available at:")
        print("  http://127.0.0.1:8000")
        print("  http://127.0.0.1:8000/docs (Interactive API docs)")
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("\nPlease install missing dependencies:")
        print("  pip install -r requirements.txt")
        print("\nFor poppler (PDF support):")
        print("  macOS: brew install poppler")
        print("  Linux: sudo apt-get install poppler-utils")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        print("\n" + "=" * 60 + "\n")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during verification: {str(e)}")
        sys.exit(1)
