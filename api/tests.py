import os

import requests

from dotenv import load_dotenv

from rest_framework.test import APITestCase, APIRequestFactory

from api.models import VideoModel
from MMVS.settings import VIDEO_PATH
load_dotenv()

TEST_VIDEO_URL = os.getenv("TEST_VIDEO_URL", "")


class VideoTestCase(APITestCase):

    test_video_response = requests.get(url=TEST_VIDEO_URL)
    test_video_path = os.path.join(VIDEO_PATH, 'test_video.mp4')

    def setUp(self):
        with open(f"{self.test_video_path}", 'wb+') as file:
            file.write(self.test_video_response.content)

    def test_post_file(self):
        with open(f"{self.test_video_path}") as test_video_file:
            factory = APIRequestFactory()
            post_request = factory.post(
                path='/file/',
                data={'upload_file': test_video_file}
            )
            print(post_request.POST)
