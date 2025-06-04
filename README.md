# API Testing Project

This project contains pytest test cases for testing the API endpoints.

## Results
3 failed, 21 passed, 1 skipped in 14.17s 
|           filepath            |               function                | passed | failed | skipped | SUBTOTAL |
| ----------------------------- | ------------------------------------- | -----: | -----: | ------: | -------: |
| regression/test_regression.py | test_create_deal_regression           |      1 |      0 |       0 |        1 |
| regression/test_regression.py | test_get_deal_regression              |      1 |      0 |       0 |        1 |
| regression/test_regression.py | test_update_deal_regression           |      1 |      0 |       0 |        1 |
| regression/test_regression.py | test_get_deals_regression             |      1 |      0 |       0 |        1 |
| regression/test_regression.py | test_merchants_regression             |      1 |      0 |       0 |        1 |
| regression/test_regression.py | test_verified_deal_regression         |      1 |      0 |       0 |        1 |
| v1/test_smoke_v1.py           | test_smoke_green                      |      1 |      0 |       0 |        1 |
| v1/test_smoke_v1.py           | test_verified_date_is_correct         |      1 |      0 |       0 |        1 |
| v1/test_smoke_v1.py           | test_post_verified_date_is_correct    |      1 |      0 |       0 |        1 |
| v1/test_smoke_v1.py           | test_put_verified_date_is_correct     |      1 |      0 |       0 |        1 |
| v1/test_smoke_v1.py           | test_get_deals_green                  |      1 |      0 |       0 |        1 |
| v1/test_smoke_v1.py           | test_get_deal_green                   |      1 |      0 |       0 |        1 |
| v1/test_smoke_v1.py           | test_update_on_non_existing           |      1 |      0 |       0 |        1 |
| v1/test_smoke_v1.py           | test_delete_on_non_existing           |      1 |      0 |       0 |        1 |
| v1/test_smoke_v1.py           | test_merchants_green                  |      1 |      0 |       0 |        1 |
| v2/test_smoke_v2.py           | test_smoke_green                      |      1 |      0 |       0 |        1 |
| v2/test_smoke_v2.py           | test_get_deals_green                  |      1 |      0 |       0 |        1 |
| v2/test_smoke_v2.py           | test_get_deal_green                   |      1 |      0 |       0 |        1 |
| v2/test_smoke_v2.py           | test_update_on_non_existing           |      1 |      0 |       0 |        1 |
| v2/test_smoke_v2.py           | test_delete_on_non_existing           |      1 |      0 |       0 |        1 |
| v2/test_smoke_v2.py           | test_merchants_green                  |      1 |      0 |       0 |        1 |
| v2/test_smoke_v2.py           | test_verified_date_is_correct         |      0 |      1 |       0 |        1 |
| v2/test_smoke_v2.py           | test_post_verified_date_is_correct    |      0 |      1 |       0 |        1 |
| v2/test_smoke_v2.py           | test_put_verified_date_is_correct     |      0 |      1 |       0 |        1 |
| v2/test_smoke_v2.py           | test_search_on_different_query_params |      0 |      0 |       1 |        1 |
| TOTAL                         |                                       |     21 |      3 |       1 |       25 |

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

Get reports
```bash
pip install pytest-md-report
python -m pytest --md-report --md-report-verbose=1 
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