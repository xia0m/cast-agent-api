import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

import test_token as token


class CastTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "cast_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
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

    def test_create_new_movie(self):
        movie_info = {
            "title": "aaa",
            "release_date": "02/20/2020"
        }
        res = self.client().post(
            '/movies', headers={'Authorization': token.producer}, json=movie_info)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

    def test_fail_create_new_movie(self):
        movie_info = {
            "title": "a new movie",
            "release_date": "abc"
        }
        res = self.client().post(
            '/movies', headers={'Authorization': token.producer}, json=movie_info)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_new_actor(self):
        actor_info = {
            "name": "nnn",
            "gender": "Female",
            "age": 36,
            "movie_id": 1

        }
        res = self.client().post(
            '/actors', headers={'Authorization': token.producer}, json=actor_info)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])

    def test_fail_create_new_actor(self):
        actor_info = {
            "name": "new actor",
            "gender": "Female",
            "age": "ten",
            "movie_id": 1
        }
        res = self.client().post(
            '/actors', headers={'Authorization': token.producer}, json=actor_info)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_one_movie(self):
        res = self.client().delete(
            '/movies/24', headers={'Authorization': token.producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['deleted'])

    def test_fail_delete_one_movie(self):
        res = self.client().delete(
            '/movies/100', headers={'Authorization': token.producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_one_actor(self):
        res = self.client().delete(
            '/actors/14', headers={'Authorization': token.producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['deleted'])

    def test_404_delete_one_actor(self):
        res = self.client().delete(
            '/actors/100', headers={'Authorization': token.producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_one_movie(self):
        res = self.client().patch(
            '/movies/1', headers={'Authorization': token.director}, json={
                "title": "new_test_title"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['updated_movie_id'])

    def test_fail_update_one_movie(self):
        res = self.client().patch(
            '/movies/100', headers={'Authorization': token.director}, json={
                "title": "new_test_title"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_one_actor(self):
        res = self.client().patch(
            '/actors/1', headers={'Authorization': token.director}, json={
                "name": "new_test_name"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['updated_actor_id'])

    def test_fail_update_one_actor(self):
        res = self.client().patch(
            '/actors/100', headers={'Authorization': token.director}, json={
                "title": "new_test_title"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_all_movies(self):

        res = self.client().get(
            '/movies', headers={'Authorization': token.assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_unauth_get_all_movies(self):
        res = self.client().get(
            '/movies', headers={'Authorization': 'Bearer test'})

        self.assertEqual(res.status_code, 401)

    def test_get_all_actors(self):
        res = self.client().get(
            '/actors', headers={'Authorization': token.assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_unauth_get_all_actors(self):
        res = self.client().get(
            '/actors', headers={'Authorization': 'Bearer test'})

        self.assertEqual(res.status_code, 401)

    def test_get_one_movie(self):
        res = self.client().get(
            '/movies/1', headers={'Authorization': token.assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_unable_to_get_one_movie(self):
        res = self.client().get(
            '/movies/100', headers={'Authorization': token.assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_one_actor(self):
        res = self.client().get(
            '/actors/1', headers={'Authorization': token.assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_unable_to_get_one_actor(self):
        res = self.client().get(
            '/actors/100', headers={'Authorization': token.assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_unauth_add_actors(self):
        actor_info = {
            "name": "b",
            "gender": "Female",
            "age": 36,
            "movie_id": 1

        }
        res = self.client().post(
            '/actors', headers={'Authorization': token.assistant}, json=actor_info)
        self.assertEqual(res.status_code, 401)

    def test_unauth_delete_movie(self):

        res = self.client().delete(
            '/movies/17', headers={'Authorization': token.director})
        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
