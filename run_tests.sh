#!/bin/bash
export PYTHONPATH=$(pwd)

# echo "Running core tests"
# pytest tests/core/ --cov=game.core --cov-report=term-missing -v

# echo "Running scene tests"
# pytest tests/scenes/ --cov=game.scenes --cov-report=term-missing -v

echo "Running all tests together"
pytest --cov=. --cov-report=term-missing -v

echo "All tests completed!"
