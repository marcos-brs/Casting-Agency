import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies

TOKEN_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImYyQWhKd2c1aFd5X1hhMlptT1ZPaSJ9' \
                  '.eyJpc3MiOiJodHRwczovL2NvZmZlZS1zaG9wLXplcm9jb29sYnIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMWVjMjZlZDkzYzEwMDAzZGNiMDNmMSIsImF1ZCI6ImNhcHN0b25lLWRldiIsImlhdCI6MTU5NTkzODQ0MiwiZXhwIjoxNTk2MDI0ODQyLCJhenAiOiJUMXJ2aE1QMkJwQmlkVU1qNjJ2S05oWjRQZW1IT0NIRiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.kWw6MCEFH0E_E8hTFyfJc12OJvea_6XRHxPitiiCQdJJalF1AXR_z4GE-xyu0hIHzRV8PpgfNSW3_s58BUy1AULfx3Osf3ooYj7-StPG4tnuG0O2GE0AvTclHdhpY1qy8yBkpM7YFLwK1QBAYTdTpvW_74aTzCM6VxF2cEi8VSZzOVAEDJU9fuKiDqEy9K_00Oydrpv-R9tbuFdxlTN3slX7-IQoIgrEQmz2IlpJmReI02NiOMEEA-j9_Q79wcDJ4gqEkEQTyr8Y-8wjlZovXaTkhZn-u7ANCDhfBz_dPwANByJN25yPHOYOkZxfuXpA59TZ2ckS468Lr2y8RPSZkw '
TOKEN_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImYyQWhKd2c1aFd5X1hhMlptT1ZPaSJ9' \
                 '.eyJpc3MiOiJodHRwczovL2NvZmZlZS1zaG9wLXplcm9jb29sYnIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMWVjMjM3MjhkZGJhMDAzNzQzYjNiMCIsImF1ZCI6ImNhcHN0b25lLWRldiIsImlhdCI6MTU5NTkzODM4OCwiZXhwIjoxNTk2MDI0Nzg4LCJhenAiOiJUMXJ2aE1QMkJwQmlkVU1qNjJ2S05oWjRQZW1IT0NIRiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.WKMtkDV1WJz6fu43oV1ClgbrjnMSMTHzCh-J-dczp9fwZuHbshflym48gNh6FoTMidHKlC1Wj4EmRYkB-e4_Vb-cYA3kS0Tjli4ng9b3wsdTibj8x7v1DyZrvUGqa9cFOmqMJ-POGPX5vPUqfkrcKJrwZvTrssFY4XrpvGiqnNg-5XpboERmDph7WQMtcnP3tTqgVmzdWVFq5trkOjtMUp1XPQgzq6oyRRbzo6WWSlhqWHRrP3OlswkeEhnVR1k6APFFeuY6tGQ6j9K9orURaHPP5IjOMMKJSDZW1gcA6cXBi900c2-IBlYNB9DbeT3pxpNXGNkiGT533gDa2LQpiA '
TOKEN_EXECUTIVE = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImYyQWhKd2c1aFd5X1hhMlptT1ZPaSJ9' \
                  '.eyJpc3MiOiJodHRwczovL2NvZmZlZS1zaG9wLXplcm9jb29sYnIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMWY2ZTM1YmJkOGNlMDAzZDYyMDY1YiIsImF1ZCI6ImNhcHN0b25lLWRldiIsImlhdCI6MTU5NTkzODQ4MiwiZXhwIjoxNTk2MDI0ODgyLCJhenAiOiJUMXJ2aE1QMkJwQmlkVU1qNjJ2S05oWjRQZW1IT0NIRiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.M49BCvPCPBQ3OUEnEGlbw4PQMoFVSmsKIAsDM0IJ7KiEC8DDi-0vksAikJJVMe8_RrhmzZF92d4fnTDCrTyQ-EG7Xh4_bHG7TOkhfuETY-CpWh3bjGnm5dJI-hvi-KOrH81IAx9sKfAYEjjPGN-CmSmetOmcUojP7Jb6fSIJhhFEmm9HiY9hnCg8ih1IQ_o4ysFM8n19DMrosm73O4kg74V-zeYsbzlxc4nD_azMSZtbHhcXrCISlZLoasQvIbzRAOD5PyKpQl8iZzTgqZ3K59tMj3SLSzS9ZcFxmJ-Kr97Gqj9cnvd8MegZ9b1GceSKTdOglkjacdpSq7oBEDqhDA '


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

    # ROLE: Casting Assistant

    def test_assistant_get_actors(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_ASSISTANT)
        }
        res = self.client().get('/actors', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_assistant_get_movies(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_ASSISTANT)
        }
        res = self.client().get('/movies', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_assistant_post_actors(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_ASSISTANT)
        }
        res = self.client().post('/actors', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_post_movies(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_ASSISTANT)
        }
        res = self.client().post('/movies', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_patch_actors(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_ASSISTANT)
        }
        res = self.client().patch('/actors/1', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_patch_movies(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_ASSISTANT)
        }
        res = self.client().patch('/movies/1', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_delete_actors(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_ASSISTANT)
        }
        res = self.client().delete('/actors/1', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_delete_movies(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_ASSISTANT)
        }
        res = self.client().delete('/movies/1', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # ROLE: Casting Director

    def test_director_get_actors(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_DIRECTOR)
        }
        res = self.client().get('/actors', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_director_get_movies(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_DIRECTOR)
        }
        res = self.client().get('/movies', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_director_post_actors(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_DIRECTOR)
        }
        res = self.client().post('/actors', headers=headers, json={
            "name": "Marcos Santana",
            "age": 22,
            "gender": "male"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_director_post_movies(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_DIRECTOR)
        }
        res = self.client().post('/movies', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_director_patch_actors(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_DIRECTOR)
        }
        res = self.client().patch('/actors/1', headers=headers, json={
            "title": "Marcos BR Santana"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_director_patch_movies(self):

        test_movie = Movies(title='Udacity - the movie', release_date='2020-07-28T12:56:36+00:00')
        test_movie.insert()

        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_DIRECTOR)
        }
        res = self.client().patch('/movies/1', headers=headers, json={
            "title": "Marcos BR Santana"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_director_patch_actor_that_does_not_exist(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_DIRECTOR)
        }
        res = self.client().patch('/actor/666', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_director_patch_movies_that_does_not_exist(self):
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN_DIRECTOR)
        }
        res = self.client().patch('/movies/666', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)


if __name__ == '__main__':
    unittest.main()
