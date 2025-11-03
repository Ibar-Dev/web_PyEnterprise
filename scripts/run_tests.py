#!/usr/bin/env python3
"""
Test runner script for PyEnterprise
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle the result"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def main():
    """Main test runner"""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print("🚀 PyEnterprise Test Suite")
    print("=" * 60)

    # Check if we're in a git repository
    is_git = subprocess.run("git status", shell=True, capture_output=True).returncode == 0

    # Parse command line arguments
    args = sys.argv[1:]

    # Default options
    run_unit = True
    run_integration = False
    run_e2e = False
    coverage = True
    verbose = False

    # Parse arguments
    for arg in args:
        if arg == "--unit-only":
            run_integration = False
            run_e2e = False
        elif arg == "--integration":
            run_integration = True
        elif arg == "--e2e":
            run_e2e = True
        elif arg == "--all":
            run_integration = True
            run_e2e = True
        elif arg == "--no-coverage":
            coverage = False
        elif arg == "-v" or arg == "--verbose":
            verbose = True
        elif arg == "--help":
            print("Usage: python run_tests.py [options]")
            print("Options:")
            print("  --unit-only     Run only unit tests (default)")
            print("  --integration   Run integration tests")
            print("  --e2e          Run end-to-end tests")
            print("  --all          Run all tests")
            print("  --no-coverage  Disable coverage reporting")
            print("  -v, --verbose  Verbose output")
            print("  --help         Show this help")
            return

    # Check requirements
    print("\n📋 Checking test requirements...")

    # Check if pytest is installed
    try:
        import pytest
        print(f"✅ pytest {pytest.__version__} found")
    except ImportError:
        print("❌ pytest not found. Please install it with: pip install pytest")
        return 1

    # Build pytest command
    pytest_cmd = "python -m pytest"

    if verbose:
        pytest_cmd += " -vv"
    else:
        pytest_cmd += " -v"

    if coverage:
        pytest_cmd += " --cov=pyenterprise --cov-report=term-missing --cov-report=html"

    # Add test selection
    test_paths = []

    if run_unit:
        test_paths.append("tests/unit/")

    if run_integration:
        test_paths.append("tests/test_*.py")
        # Set environment variable for integration tests
        os.environ["RUN_INTEGRATION_TESTS"] = "true"

    if run_e2e:
        test_paths.append("tests/e2e/")
        # Set environment variable for E2E tests
        os.environ["RUN_E2E_TESTS"] = "true"

    if test_paths:
        pytest_cmd += " " + " ".join(test_paths)

    # Run tests
    success = True

    if run_unit:
        unit_cmd = pytest_cmd.replace("--cov=pyenterprise", "--cov=pyenterprise --cov-report=term-missing")
        if not run_command(unit_cmd, "Running Unit Tests"):
            success = False

    if run_integration:
        integration_cmd = f"python -m pytest tests/test_*.py -v -m integration"
        if not run_command(integration_cmd, "Running Integration Tests"):
            success = False

    if run_e2e:
        print("\n🌐 Running E2E Tests...")
        print("Note: Make sure the application is running on http://localhost:3000")

        # Check if the app is running
        try:
            import requests
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                print("✅ Application is running")
                e2e_cmd = "python -m pytest tests/e2e/ -v -m e2e"
                if not run_command(e2e_cmd, "Running End-to-End Tests"):
                    success = False
            else:
                print("❌ Application is not responding correctly")
                success = False
        except Exception as e:
            print(f"❌ Cannot connect to application: {e}")
            print("Please start the application first: reflex run")
            success = False

    # Generate coverage report
    if coverage and success:
        print("\n📊 Generating coverage report...")
        coverage_cmd = "python -m coverage html"
        run_command(coverage_cmd, "Generating HTML Coverage Report")
        print("\n📈 Coverage report generated in htmlcov/index.html")

    # Final summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 All tests passed!")
        print("\n📊 Test Summary:")
        if run_unit:
            print("  ✅ Unit Tests: PASSED")
        if run_integration:
            print("  ✅ Integration Tests: PASSED")
        if run_e2e:
            print("  ✅ E2E Tests: PASSED")
    else:
        print("❌ Some tests failed!")
        print("\n📊 Test Summary:")
        if run_unit:
            print("  ❌ Unit Tests: FAILED")
        if run_integration:
            print("  ❌ Integration Tests: FAILED")
        if run_e2e:
            print("  ❌ E2E Tests: FAILED")
        return 1

    print(f"\n🔗 Useful Links:")
    print(f"  📈 Coverage Report: htmlcov/index.html")
    print(f"  🧪 Run specific test: python -m pytest tests/unit/test_auth.py -v")
    print(f"  🏃 Run with coverage: python -m pytest --cov=pyenterprise tests/")

    return 0

if __name__ == "__main__":
    sys.exit(main())