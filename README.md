# taehee-won-core

## Description

taehee-won-core is a versatile Python framework designed for enhancing Python programming tasks.  
It offers utility functions and modular components for data handling, database management, and more,  
streamlining the development process for both simple scripts and complex applications.

## Features

- Data Handling Utilities
- Database Management Tools
- Efficient Code Structure

## Unit Testing

To run the unit tests for the project, use the following command by default:
```
python -m unittest
```

This command will run the standard test cases.  
However, there are certain tests in the project that are designed to run only under specific conditions.  
These tests are controlled through environment variables:

- TEST_MONGODB=1: Set this environment variable to run tests related to MongoDB.
- TEST_INTERNET=1: Set this environment variable to run tests that require an internet connection.
- TEST_CLI=1: Set this environment variable to run tests related to the command line interface.

To execute all conditional tests, you can set TEST_ALL=1.  
This will ignore all the specific conditions and run every test:
```
TEST_ALL=1 python -m unittest
```

You can also set environment variables individually to run specific groups of tests.  
For example, to run only MongoDB-related tests, you would use:
```
TEST_MONGODB=1 python -m unittest
```

Use these options appropriately to effectively manage and execute the tests for your project.
