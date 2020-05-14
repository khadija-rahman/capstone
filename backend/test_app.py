import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    @classmethod
    def setUpClass(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.jwt_assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJNQXRpbEFHVDg1clFlQkRTTG5pdiJ9.eyJpc3MiOiJodHRwczovL2dyYWluLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWI1Nzc5ZjQ2MjU5NDBiZjk2YzU2NjgiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU4OTQ0MzA2MywiZXhwIjoxNTg5NTI5NDYzLCJhenAiOiJzYzVzSE5rdjJ5VGY0cDBQTlkyUktYb2RNQlBPOXhkbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.RAejJJDKPhe5-nR2HV5irbEzAyaAkjzWFofGsmIAaW1dj7MdecbmJ_b6L6K_sZW1CRK7SxFVmpoozFvD85LaX8svhl11OOn7zUpBgnM-ZdOh6ylPcxUxWsHBIPue9hc7tTeo4QNs1w6RmCXVg4pLrOV3e85A8MheiV4IkWX9NFfOLm1Eh0JMp64brGz6htAV5RgWqHa7bz0VIDPO3M1ivc386VUGtznemVHB7Kzcpr7e_JwwIqW9gujMeUFanmFmulWdSTq4YReW2exAlu38GKbnn7wCUnlJvM8URFEcHYFs2FJf8i8bc6GV4ZsgF3ciMZRHBAeKuPyrAHZiQrXyeg"
        self.jwt_casting_director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJNQXRpbEFHVDg1clFlQkRTTG5pdiJ9.eyJpc3MiOiJodHRwczovL2dyYWluLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWJkMGY3NzU0NmRiZTBjMDY2MTdjZTciLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU4OTQ0ODYzNCwiZXhwIjoxNTg5NTM1MDM0LCJhenAiOiJzYzVzSE5rdjJ5VGY0cDBQTlkyUktYb2RNQlBPOXhkbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJ1cGRhdGU6YWN0b3IiLCJ1cGRhdGU6bW92aWUiXX0.AIOLBp5SAqvec3OEEI8wtBND4S4KyCEvbU6LUVU_5ZLNWkxtA-e6e6k8OslXyAV6SjyylqZPcfE8gplVznt39syY24jzzLEe3D8f1KTYqGG3a1ULK97lf7aMdT3FimqQa1APNFwaQIcIZ1_9o4eLv_gC-nsnwmbgRDZt_oPFR-C-AUdyi5zgfLGxffXtCVr6ZGlIi3cpZ6Q2uz4MtwhqC7NXA0wjIKa-60q1JSp8gHr-vvF44LvjNTCdSJDW-t2G6p6cmn6W_PqpgafxMmubIGSFc53CsEZytjn0Q2fqAlgbQ3dGoywB6qZkAccCBSvt35HT11XafQcciaZkuhKaxg"
        self.jwt_exec_producer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJNQXRpbEFHVDg1clFlQkRTTG5pdiJ9.eyJpc3MiOiJodHRwczovL2dyYWluLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwOTI0NjkyMDk0Njc3NjA2MTYxOSIsImF1ZCI6WyJjYXBzdG9uZSIsImh0dHBzOi8vZ3JhaW4uZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4OTQ0MzkzMiwiZXhwIjoxNTg5NTMwMzMyLCJhenAiOiJzYzVzSE5rdjJ5VGY0cDBQTlkyUktYb2RNQlBPOXhkbiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3IiLCJhZGQ6bW92aWUiLCJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInVwZGF0ZTphY3RvciIsInVwZGF0ZTptb3ZpZSJdfQ.r_zmxfRr_kPitnDv2WHTNUEUpVinqa9v1gHkad0anWAupC4-ipuHYzloaSMqIY-JFMRVmCxU6v-emW_q-m7zWEr02kmr_cBIADSHsQNQiWrVWAf2JGGNhjTpGeeyQDs34lrRXtDpng8irkVdIO1kt9n8xXOsyXvOryG-Nn-0_Zh1vEOx8adHfsm5bJf7r5gnrhUIlwmxWkTPF06Don99Xamev__EHUJVZ3DqVI1YTe7ZCp-vt-xl_8jgFLSn2Q8TgkyutkRtWhWF6_fpebjrqQ3Btax5BITReG8TUAhV2vCshXZOiTbfnaeOGNYBuNqWuINX4AW9lieJ9IRkbH-Isw"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.drop_all()
            self.db.create_all()

    @classmethod
    def tearDownClass(self):
        """Executed after reach test"""
        # self.db.drop_all()
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_1_add_movies(self):
        res = self.client().post(
            '/movies',
            headers={"Authorization": "Bearer {}".format(
                self.jwt_exec_producer)},
            json={"title": "Shape of liquid", "release_date": "2020-04-12"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], 1)

    def test_1_add_movies_401(self):
        res = self.client().post(
            '/movies',
            headers={"Authorization": "Bearer {}".format(
                self.jwt_casting_director)},
            json={"title": "Shape of liquid", "release_date": "2020-04-12"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


    def test_2_update_movies(self):
        res = self.client().patch(
            '/movies/1',
            headers={"Authorization": "Bearer {}".format(
                self.jwt_exec_producer)},
            json={"title": "Shape of liquid", "release_date": "2020-04-13"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['release_date'],
                         'Mon, 13 Apr 2020 00:00:00 GMT')

    def test_2_update_movies_401(self):
        res = self.client().post(
            '/movies',
            headers={"Authorization": "Bearer badtoken"},
            json={"title": "Shape of liquid", "release_date": "2020-04-12"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_3_get_movies(self):
        res = self.client().get(
            '/movies', headers={"Authorization": "Bearer {}".format(self.jwt_assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_3_get_movies_401(self):

        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_4_get_movie(self):
        res = self.client().get(
            '/movies/1', headers={"Authorization": "Bearer {}".format(self.jwt_assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 1)

    def test_4_get_movie_401(self):
        res = self.client().get("/movies/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_5_delete_movie(self):
        res = self.client().delete(
            '/movies/1', headers={"Authorization": "Bearer {}".format(self.jwt_exec_producer)}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_5_delete_movie_401(self):
        res = self.client().delete("/movies/1",
                                   headers={"Authorization": "Bearer {}".format(self.jwt_casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)





    def test_10_add_actors(self):
        res = self.client().post(
            '/actors',
            headers={"Authorization": "Bearer {}".format(
                self.jwt_exec_producer)},
            json={"name": "Tom Smith", "age": 30, "gender": "Male"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], 1)

    def test_10_add_actors_401(self):
        res = self.client().post(
            '/actors',
            headers={"Authorization": "Bearer badtoken"},
            json={"name": "Tom Smith", "age": 30, "gender": "Male"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_11_update_actors(self):
        res = self.client().patch(
            '/actors/1',
            headers={"Authorization": "Bearer {}".format(
                self.jwt_exec_producer)},
            json={"name": "Tom Smith", "age": 35, "gender": "Male"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['age'], 35)

    def test_11_update_actors_401(self):
        res = self.client().post(
            '/actors',
            headers={"Authorization": "Bearer badtoken"},
            json={"name": "Tom Smith", "age": 35, "gender": "Male"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_12_get_actors(self):
        res = self.client().get(
            '/actors', headers={"Authorization": "Bearer {}".format(self.jwt_assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_12_get_actors_401(self):

        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_13_get_actor(self):
        res = self.client().get(
            '/actors/1', headers={"Authorization": "Bearer {}".format(self.jwt_assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], 1)

    def test_13_get_actor_401(self):
        res = self.client().get("/actors/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_14_delete_actor(self):
        res = self.client().delete(
            '/actors/1', headers={"Authorization": "Bearer {}".format(self.jwt_exec_producer)}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_14_delete_actor_401(self):
        res = self.client().delete("/actors/1",
                                   headers={"Authorization": "Bearer {}".format(self.jwt_assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
