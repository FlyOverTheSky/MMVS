import os
import random
import uuid

import requests
import json

from dotenv import load_dotenv
from rest_framework import status

from rest_framework.test import APITestCase, APIRequestFactory


load_dotenv()

TEST_VIDEO_URL = os.getenv("TEST_VIDEO_URL", "")
TEST_FILES_PATH = os.getenv("TEST_FILES_PATH", "")
INDEX_URL = os.getenv("INDEX_URL", "")


class VideoTestCase(APITestCase):

    test_video_response = requests.get(url=TEST_VIDEO_URL, stream=True)

    def setUp(self):
        test_video_filename = f"test_video_{random.randint(1, 100000)}.mp4"
        test_video_path = os.path.join(TEST_FILES_PATH, test_video_filename)

        with open(file=test_video_path, mode='wb') as file:
            file.write(self.test_video_response.content)

        with open(file=test_video_path, mode='rb') as test_video_file:
            post_request = requests.post(
                url=f"{INDEX_URL}/file/",
                files={'file': test_video_file}
            )
        test_video_id = json.loads(post_request.content.decode('utf-8')).get('id')
        test_video_id = uuid.UUID(test_video_id)
        output_func_data = {
            'filename': test_video_filename,
            'status': post_request.status_code,
            'video_id': test_video_id
        }
        return output_func_data

    def test_post_and_get_file(self):
        """Test for /file/ POST, /file/id/ GET requests."""
        response_data = self.setUp()
        test_video_id = response_data.get('video_id')
        request_status_code = response_data.get('status')
        test_video_filename = response_data.get('filename')

        get_request = requests.get(
            url=f'{INDEX_URL}/file/{test_video_id}'
        )
        get_response_data = json.loads(get_request.content.decode('utf-8'))
        get_response_video_id = get_response_data.get('id')
        get_response_video_filename = get_response_data.get('filename')
        self.assertEqual(
            first=uuid.UUID(get_response_video_id),
            second=test_video_id,
            msg='Полученный id и id при загрузке не совпадают'
        )
        self.assertEqual(
            first=f"{str(get_response_video_filename)}.mp4",
            second=test_video_filename,
            msg='Полученное имя файла и заданное не совпадают',
        )
        self.assertEqual(
            first=request_status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=request_status_code,
            second=status.HTTP_200_OK,
        )

    def test_delete_file(self):
        response_data = self.setUp()
        test_video_id = response_data.get('video_id')

        delete_request = requests.delete(
            url=f'{INDEX_URL}/file/{test_video_id}'
        )

        delete_response_data = json.loads(delete_request.content.decode('utf-8'))

        self.assertEqual(
            first=bool(delete_response_data.get('success')),
            second=True
        )
        self.assertEqual(
            first=delete_request.status_code,
            second=status.HTTP_200_OK,
        )

    def test_patch_file(self):
        response_data = self.setUp()
        test_video_id = response_data.get('video_id')
        new_resolution = {
            'width': 320,
            'height': 320,
        }
        patch_request = requests.patch(
            url=f"{INDEX_URL}/file/{test_video_id}",
            data=new_resolution
        )
        print(patch_request.status_code)

