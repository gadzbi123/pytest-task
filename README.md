# API Testing Project

This project contains pytest test cases for testing the API endpoints.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your API key:
```
API_KEY=your_api_key_here
```

## Running Tests

To run all tests:
```bash
python -m pytest
```

To run a specific test:
```bash
python -m pytest test_api.py::test_get_deals
```

## Test Cases

The project includes test cases for:
- GET /api/v2/GetDeals/ - Fetch deals with query parameters
- POST /api/v2/Deals/ - Create a new deal
- PUT /api/v2/Deals/{id} - Update an existing deal
- DELETE /api/v2/Deals/{id} - Delete a deal

## Notes

- Make sure to set your API key in the `.env` file before running tests
- The tests are designed to run in sequence, where some tests depend on the results of previous tests
- The base URL is configured in `config.py` 