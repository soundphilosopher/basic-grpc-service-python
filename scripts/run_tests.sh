#!/bin/bash
# 🧪 Comprehensive Test Runner for Basic gRPC Service
#
# This script sets up the test environment and runs all tests with proper
# configuration and reporting. It handles dependencies, test discovery,
# and provides detailed output for debugging.
#
# Usage:
#   ./scripts/run_tests.sh [OPTIONS]
#
# Options:
#   --coverage    Run tests with coverage reporting
#   --verbose     Extra verbose output
#   --fast        Skip dependency checks (faster for repeated runs)
#   --help        Show this help message

set -e

# Colors for pretty output 🎨
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default options
COVERAGE=false
VERBOSE=false
FAST=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --coverage)
            COVERAGE=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --fast)
            FAST=true
            shift
            ;;
        --help)
            echo "  Basic gRPC Service Test Runner"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --coverage    Run tests with coverage reporting"
            echo "  --verbose     Extra verbose output"
            echo "  --fast        Skip dependency checks (faster for repeated runs)"
            echo "  --help        Show this help message"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED} Unknown option: $1${NC}"
            echo "Use --help for available options"
            exit 1
            ;;
    esac
done

echo -e "${CYAN}  Basic gRPC Service Test Runner${NC}"
echo "=================================="

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]]; then
    echo -e "${RED} Error: pyproject.toml not found${NC}"
    echo -e "${YELLOW}Please run this script from the project root directory${NC}"
    exit 1
fi

# Install dependencies (unless --fast is specified)
if [[ "$FAST" != true ]]; then
    echo -e "\n${BLUE} Installing dependencies...${NC}"

    # Install dev dependencies
    echo "  Installing dev dependencies..."
    pip install -e ".[dev]" --quiet

    # Install coverage if requested
    if [[ "$COVERAGE" == true ]]; then
        echo "  Installing coverage tools..."
        pip install coverage pytest-cov --quiet
    fi

    echo -e "${GREEN}󰗠 Dependencies installed${NC}"
fi

# Test discovery
echo -e "\n${PURPLE} Discovering tests...${NC}"
test_files=($(find tests -name "test_*.py" -type f))
test_count=${#test_files[@]}

echo "Found $test_count test files:"
for file in "${test_files[@]}"; do
    echo "   $file"
done

# Build pytest command
PYTEST_CMD="python -m pytest tests/ --asyncio-mode=auto"

# Add verbose flags
if [[ "$VERBOSE" == true ]]; then
    PYTEST_CMD="$PYTEST_CMD -vvv -s"
else
    PYTEST_CMD="$PYTEST_CMD -v"
fi

# Add coverage if requested
if [[ "$COVERAGE" == true ]]; then
    PYTEST_CMD="$PYTEST_CMD --cov=services --cov=utils --cov-report=html --cov-report=term-missing"
fi

# Run the tests
echo -e "\n${YELLOW}󰙨 Running tests...${NC}"
echo "Command: $PYTEST_CMD"
echo ""

if eval $PYTEST_CMD; then
    echo -e "\n${GREEN}󱁖 All tests passed!${NC}"

    if [[ "$COVERAGE" == true ]]; then
        echo -e "\n${CYAN} Coverage report generated:${NC}"
        echo "   Terminal summary: shown above"
        echo "   HTML report: htmlcov/index.html"
        echo ""
        echo -e "${BLUE} To view the HTML coverage report:${NC}"
        echo "  python -m http.server 8000 -d htmlcov/"
        echo "  Then open: http://localhost:8000"
    fi

    echo -e "\n${GREEN}󰗠 Test suite completed successfully!${NC}"
    echo -e "Your gRPC service is ready for production! "

else
    echo -e "\n${RED} Some tests failed${NC}"
    echo -e "${YELLOW} Tips for debugging:${NC}"
    echo "  • Run with --verbose for more detailed output"
    echo "  • Check the test output above for specific failures"
    echo "  • Make sure all dependencies are installed"
    echo "  • Verify that protobuf files are properly generated"
    exit 1
fi
