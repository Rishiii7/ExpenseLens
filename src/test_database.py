import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.pool import NullPool
from database import (
    getconn,
    create_user_images_table,
    insert_user_image,
    create_authentication_table,
    insert_authentication_details,
    create_receipt_details_table,
    insert_receipt_details,
    closeConnection,
)

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup any necessary configurations for testing at the class level
        pass

    def setUp(self):
        # Setup any necessary test-specific configurations before each test method runs
        pass

    def tearDown(self):
        # Clean up after each test
        pass

    def test_getconn(self):
        # Test the getconn function to ensure it returns a valid connection
        connection = getconn()
        self.assertIsNotNone(connection)
        connection.close()

    def test_create_user_images_table(self):
        # Test the creation of the user_images table
        with patch('sqlalchemy.create_engine') as mock_create_engine:
            # Mock the pool object to avoid actual database connections
            mock_pool = MagicMock(spec=NullPool)
            mock_create_engine.return_value.connect.return_value.__enter__.return_value = mock_pool

            # Call the function you want to test
            create_user_images_table(mock_create_engine)

            # Assertions based on your expectations
            mock_pool.connect.assert_called_once()
            mock_pool.execute.assert_called_with("""
                CREATE TABLE IF NOT EXISTS user_images (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255),
                    image_path VARCHAR(255)
                )
            """)

    def test_insert_user_image(self):
        # Test the insertion of user image data
        with patch('sqlalchemy.create_engine') as mock_create_engine:
            # Mock the pool object to avoid actual database connections
            mock_pool = MagicMock(spec=NullPool)
            mock_create_engine.return_value.connect.return_value.__enter__.return_value = mock_pool

            # Call the function you want to test
            insert_user_image(mock_create_engine, 'test_user', 'test_image_path')

            # Assertions based on your expectations
            mock_pool.connect.assert_called_once()
            mock_pool.execute.assert_called_with("""
                INSERT INTO user_images (username, image_path) VALUES (:username, :image_path)
            """, {"username": 'test_user', "image_path": 'test_image_path'})

    # Add similar test cases for create_authentication_table, insert_authentication_details,
    # create_receipt_details_table, insert_receipt_details, and closeConnection

if __name__ == '__main__':
    unittest.main()
