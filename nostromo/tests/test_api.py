from django.test import TestCase
from rest_framework.test import APIClient
from nostromo.models import DataSet
from account.models import User
import datetime
import json


class ApiTestCase(TestCase):

    def setUp(self):
        self.user_tom = User.objects.create_user(first_name='tom', last_name='cruise',email='tom.cruise@itcanfly.com')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_tom.auth_token.key)
        matrix1 = [
            [-0.02, -0.046, -1.004],
            [-0.018, -0.046, -1.003],
            [-0.02, -0.045, -1.005],
            [-0.018, -0.045, -1.004],
            [-0.022, -0.046, -1.004],
            [-0.019, -0.047, -1.005],
            [-0.018, -0.047, -1.007],
            [-0.019, -0.045, -1.005],
            [-0.018, -0.046, -1.008],
            [-0.018, -0.046, -1.005]
        ]
        start_time_unix1 = 1455828698961
        start_time1 = datetime.datetime.utcfromtimestamp(start_time_unix1/1000)
        end_time_unix1 = 1455828579707
        end_time1 = datetime.datetime.utcfromtimestamp(end_time_unix1/1000)

        self.initial_data1 = DataSet.objects.create(
            user=self.user_tom,
            type="accel",
            start_date=start_time1,
            end_date=end_time1,
            data=json.dumps(matrix1)
        )

        matrix2 = [
            [-0.01, -0.046, -1.004],
            [-0.018, -0.046, -1.003],
            [-0.02, -0.045, -1.005],
            [-0.018, -0.045, -1.004],
            [-0.022, -0.046, -1.004],
            [-0.019, -0.047, -1.005],
            [-0.018, -0.047, -1.007],
            [-0.019, -0.045, -1.005],
            [-0.018, -0.046, -1.008],
            [-0.018, -0.046, -1.004]
        ]

        start_time_unix2 = 1455828698964
        start_time2 = datetime.datetime.utcfromtimestamp(start_time_unix2/1000)
        end_time_unix2 = 1455828579709
        end_time2 = datetime.datetime.utcfromtimestamp(end_time_unix2/1000)

        self.initial_data2 = DataSet.objects.create(
            user=self.user_tom,
            type="accel",
            start_date=start_time2,
            end_date=end_time2,
            data=json.dumps(matrix2)
        )

    def testTryToSaveAllDuplicates(self):
        data = [{
            "start": 1455828698961,
            "end": 1455828579707,
            "type": "accel",
            "data": [
                [-0.02, -0.046, -1.004],
                [-0.018, -0.046, -1.003],
                [-0.02, -0.045, -1.005],
                [-0.018, -0.045, -1.004],
                [-0.022, -0.046, -1.004],
                [-0.019, -0.047, -1.005],
                [-0.018, -0.047, -1.007],
                [-0.019, -0.045, -1.005],
                [-0.018, -0.046, -1.008],
                [-0.018, -0.046, -1.005]
            ]
        }, {
            "start": 1455828698964,
            "end": 1455828579709,
            "type": "accel",
            "data": [
                [-0.01, -0.046, -1.004],
                [-0.018, -0.046, -1.003],
                [-0.02, -0.045, -1.005],
                [-0.018, -0.045, -1.004],
                [-0.022, -0.046, -1.004],
                [-0.019, -0.047, -1.005],
                [-0.018, -0.047, -1.007],
                [-0.019, -0.045, -1.005],
                [-0.018, -0.046, -1.008],
                [-0.018, -0.046, -1.004]
            ]
        }]
        expected = {'processed': 2, 'duplicate': 2, 'success': 0}
        response = self.client.post('/api/v1/push/', format='json', data=json.dumps(data))
        self.assertEqual(response.json(), expected)

    def testTryToSaveAllCorrect(self):
        data = [{
            "start": 1455821479707,
            "end": 1455828698951,
            "type": "accel",
            "data": [
                [-0.02, -0.046, -1.004],
                [-0.018, -0.046, -1.003],
                [-0.02, -0.075, -1.005],
                [-0.018, -0.045, -1.004],
                [-0.022, -0.096, -1.004],
                [-0.019, -0.047, -1.005],
                [-0.018, -0.047, -1.007],
                [-0.019, -0.045, -1.005],
                [-0.018, -0.046, -1.008],
                [-0.018, -0.046, -1.005]
            ],
        }, {
            "start": 1455828579701,
            "end": 1455828658964,
            "type": "accel",
            "data": [
                [-0.01, -0.026, -1.004],
                [-0.018, -0.046, -1.003],
                [-0.02, -0.035, -1.005],
                [-0.018, -0.045, -1.004],
                [-0.022, -0.046, -1.004],
                [-0.019, -0.047, -1.005],
                [-0.018, -0.047, -1.007],
                [-0.019, -0.045, -1.005],
                [-0.018, -0.046, -1.008],
                [-0.018, -0.046, -1.004]
            ],
        }]
        response = self.client.post('/api/v1/push/', format='json', data=json.dumps(data))
        expected = {'processed': 2, 'duplicate': 0, 'success': 2}
        self.assertEqual(response.json(), expected)

    def testTryToSaveSomeDuplicate(self):
        data = [{
            "start": 1455828698961,
            "end": 1455828579707,
            "type": "accel",
            "data": [
                [-0.02, -0.046, -1.004],
                [-0.018, -0.046, -1.003],
                [-0.02, -0.045, -1.005],
                [-0.018, -0.045, -1.004],
                [-0.022, -0.046, -1.004],
                [-0.019, -0.047, -1.005],
                [-0.018, -0.047, -1.007],
                [-0.019, -0.045, -1.005],
                [-0.018, -0.046, -1.008],
                [-0.018, -0.046, -1.005]
            ]
        }, {
            "start": 1411828579709,
            "end": 1451828698964,
            "type": "accel",
            "data": [
                [-0.01, -0.046, -1.004],
                [-0.018, -0.046, -1.003],
                [-0.02, -0.045, -1.005],
                [-0.011, -0.045, -1.004],
                [-0.022, -0.046, -1.004],
                [-0.019, -0.047, -1.005],
                [-0.011, -0.047, -1.007],
                [-0.019, -0.045, -1.005],
                [-0.018, -0.046, -1.008],
                [-0.011, -0.046, -1.004]
            ]
        }]
        response = self.client.post('/api/v1/push/', format='json', data=json.dumps(data))
        expected = {'processed': 2, 'duplicate': 1, 'success': 1}
        self.assertEqual(response.json(), expected)
