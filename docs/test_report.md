
# Test Report

## 1. Testing Objective
Verify the main functionality of the Customer Service Ticket API using automated tests.

## 2. Testing Framework
Pytest with FastAPI TestClient and an isolated in-memory SQLite test database.

## 3. Test Results

| Test Case | Expected Result | Actual Result |
|---|---|---|
| Home endpoint | HTTP 200 | Passed |
| Create ticket | Ticket created | Passed |
| Invalid ticket | HTTP 422 | Passed |
| Get all tickets | HTTP 200 | Passed |
| Ticket not found | HTTP 404 | Passed |
| Assign ticket | HTTP 200 | Passed |
| Update priority | HTTP 200 | Passed |
| Update status | HTTP 200 | Passed |
| Audit history | Audit records returned | Passed |

## 4. Summary

Total automated tests: 9

Passed: 9

Failed: 0

Command used:

`python -m pytest -v`

## 5. Manual Validation

Swagger UI was used to verify ticket creation, invalid input rejection, and API responses.

## 6. Testing Limitations

The current test suite covers the main API workflows. Additional tests are recommended for search filters, overdue-ticket conditions, invalid updates, and database failure scenarios.
