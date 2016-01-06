import os
import dejavu
import unittest
import json

from scipy.io import wavfile

class DejavuTestCase(unittest.TestCase):
    "Work in progress ..."
    def setUp(self):
        self.app = dejavu.app.test_client()

    def tearDown(self):
        pass

    def test_json_post(self):
        wav_data = wavfile.read('test_tracks/test_track1.wav')[1]
        wav_data = wav_data.tolist()
        data = [s for d in wav_data for s in d]
        msg = json.dumps({'channels': 2,
                          'length': len(data),
                          'data': data})
        resp = self.app.post('/recognize', data=msg,
                             content_type='application/json')
        print resp


if __name__ == '__main__':
    unittest.main()
