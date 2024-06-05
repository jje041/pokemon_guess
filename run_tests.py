import os
import sys
import unittest

# Add the parent directory to the sys.path to allow importing from backend.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'game_api')))

test_loader = unittest.TestLoader()
test_suite = test_loader.discover("tests")

if __name__ == "__main__":
    print("Running all tests....")
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)

