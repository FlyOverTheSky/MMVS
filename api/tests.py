import os
import random
import uuid

import requests
import json

from dotenv import load_dotenv

from rest_framework.test import APITestCase, APIRequestFactory


load_dotenv()

TEST_VIDEO_URL = os.getenv("TEST_VIDEO_URL", "")
TEST_FILES_PATH = os.getenv("TEST_FILES_PATH", "")
INDEX_URL = os.getenv("INDEX_URL", "")


class VideoTestCase(APITestCase):

    test_video_response = requests.get(url=TEST_VIDEO_URL, stream=True)
    test_video_filename = f"test_video_{random.randint(1, 100000)}.mp4"
    test_video_path = os.path.join(TEST_FILES_PATH, test_video_filename)

    def setUp(self):
        with open(f"{self.test_video_path}", 'wb') as file:
            file.write(self.test_video_response.content)

    def test_post_and_get_file(self):
        """Test for /file/ POST, /file/id/ GET requests."""
        test_video_file = open(
            file=self.test_video_path,
            mode='rb'
        )

        post_request = requests.post(
            url=f"{INDEX_URL}/file/",
            files={'file': test_video_file}
        )

        test_video_id = json.loads(post_request.content.decode('utf-8')).get('id')
        test_video_id = uuid.UUID(test_video_id)

        get_request = requests.get(
            url=f'{INDEX_URL}/file/{test_video_id}'
        )
        get_repsonse_data = json.loads(get_request.content.decode('utf-8'))
        get_response_video_id = get_repsonse_data.get('id')
        get_response_video_filename = get_repsonse_data.get('filename')
        self.assertEqual(
            first=uuid.UUID(get_response_video_id),
            second=test_video_id,
            msg='Полученный id и id при загрузке не совпадают'
        )
        self.assertEqual(
            first=f"{str(get_response_video_filename)}.mp4",
            second=self.test_video_filename,
            msg='Полученное имя файла и заданное не совпадают',
        )

    def test_delete_file(self):
        test_video_file = open(
            file=self.test_video_path,
            mode='rb'
        )
        post_request = requests.post(
            url=f"{INDEX_URL}/file/",
            files={'file': test_video_file}
        )
        test_video_id = json.loads(post_request.content.decode('utf-8')).get('id')
        test_video_id = uuid.UUID(test_video_id)

        delete_request = requests.delete(
            url=f'{INDEX_URL}/file/{test_video_id}'
        )

        delete_response_data = json.loads(delete_request.content.decode('utf-8'))

        self.assertEqual(
            first=bool(delete_response_data.get('success')),
            second=True
        )
