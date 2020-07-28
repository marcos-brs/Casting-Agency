import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db


class MyTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_user = "postgres"
        self.database_password = "docker"
        self.database_host = "localhost"
        self.database_port = 5432
        self.database_path = "postgresql://{}:{}@{}:{}/{}".format(
            self.database_user, self.database_password, self.database_host, self.database_port, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_example(self):
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
