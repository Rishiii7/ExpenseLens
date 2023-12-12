import unittest
from unittest.mock import MagicMock, patch
from analytics import (
    calculate_total_expenditure_latest_month,
    calculate_category_wise_expenditure_latest_month,
    get_latest_transaction_details,
    calculate_highest_spending_category_latest_month,
    monthly_expenditure_trends,
    expenditure_and_percentage_change,
    analytics
)


class TestAnalytics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup any necessary configurations for testing at the class level
        pass

    def setUp(self):
        # Setup any necessary test-specific configurations before each test method runs
        pass

    def tearDown(self):
        # Clean up resources or perform any necessary cleanup after each test method runs
        pass

    def test_calculate_total_expenditure_latest_month(self):
        # Test the function with a mock connection pool and sample data
        pool = MagicMock()
        pool.execute.return_value.fetchall.return_value = [
            {'date': '2023-04-10', 'total_amount': 50.0},
            {'date': '2023-04-15', 'total_amount': 30.0},
            {'date': '2023-03-25', 'total_amount': 20.0},
        ]
        result = calculate_total_expenditure_latest_month(pool, 'test_user')
        self.assertEqual(result, 80.0)

    def test_calculate_category_wise_expenditure_latest_month(self):
        # Test the function with a mock connection pool and sample data
        pool = MagicMock()
        pool.execute.return_value.fetchall.return_value = [
            {'category': 'Groceries', 'date': '2023-04-10', 'total_amount': 20.0},
            {'category': 'Clothing', 'date': '2023-04-15', 'total_amount': 30.0},
            {'category': 'Groceries', 'date': '2023-03-25', 'total_amount': 15.0},
        ]
        result = calculate_category_wise_expenditure_latest_month(pool, 'test_user')
        expected_result = {'Groceries': 20.0, 'Clothing': 30.0}
        self.assertEqual(result, expected_result)

    def test_get_latest_transaction_details(self):
        # Test the function with a mock connection pool and sample data
        pool = MagicMock()
        pool.execute.return_value.fetchall.return_value = [
            {'category': 'Electronics', 'merchant_name': 'Tech Store', 'location': 'City, State', 'date': '2023-04-10', 'total_amount': 50.0},
            {'category': 'Clothing', 'merchant_name': 'Fashion Outlet', 'location': 'City, State', 'date': '2023-04-15', 'total_amount': 30.0},
        ]
        result = get_latest_transaction_details(pool, 'test_user')
        expected_result = [
            {'category': 'Electronics', 'merchant_name': 'Tech Store', 'location': 'City, State', 'date': '2023-04-10', 'total_amount': 50.0},
            {'category': 'Clothing', 'merchant_name': 'Fashion Outlet', 'location': 'City, State', 'date': '2023-04-15', 'total_amount': 30.0},
        ]
        self.assertEqual(result, expected_result)

    def test_calculate_highest_spending_category_latest_month(self):
        # Test the function with a mock connection pool and sample data
        pool = MagicMock()
        pool.execute.return_value.fetchall.return_value = [
            {'category': 'Electronics', 'date': '2023-04-10', 'total_amount': 50.0},
            {'category': 'Clothing', 'date': '2023-04-15', 'total_amount': 30.0},
            {'category': 'Electronics', 'date': '2023-03-25', 'total_amount': 15.0},
        ]
        result = calculate_highest_spending_category_latest_month(pool, 'test_user')
        self.assertEqual(result, 'Electronics')

    def test_monthly_expenditure_trends(self):
        # Test the function with a mock connection pool and sample data
        pool = MagicMock()
        pool.execute.return_value.fetchall.return_value = [
            {'date': '2023-04-10', 'total_amount': 50.0},
            {'date': '2023-04-15', 'total_amount': 30.0},
            {'date': '2023-03-25', 'total_amount': 20.0},
        ]
        result = monthly_expenditure_trends(pool, 'test_user')
        expected_result = pd.DataFrame({'month_year': ['2023-04', '2023-03'], 'total_amount': [80.0, 20.0]})
        pd.testing.assert_frame_equal(result, expected_result)

    def test_expenditure_and_percentage_change(self):
        # Test the function with a mock connection pool and sample data
        pool = MagicMock()
        pool.execute.return_value.fetchall.return_value = [
            {'date': '2023-04-10', 'total_amount': 50.0},
            {'date': '2023-03-25', 'total_amount': 20.0},
        ]
        result = expenditure_and_percentage_change(pool, 'test_user')
        self.assertEqual(result, '60.0+')

    def test_analytics(self):
        # Test the function with a mock connection pool and sample data
        pool = MagicMock()
        pool.execute.return_value.fetchall.return_value = [
            {'date': '2023-04-10', 'total_amount': 50.0},
            {'date': '2023-04-15', 'total_amount': 30.0},
            {'date': '2023-03-25', 'total_amount': 20.0},
        ]
        result = analytics(pool, 'test_user')
        expected_result = (80.0, {'Groceries': 20.0, 'Clothing': 30.0}, [], 'Electronics', pd.DataFrame({'month_year': ['2023-04', '2023-03'], 'total_amount': [80.0, 20.0]}), '60.0+')
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
