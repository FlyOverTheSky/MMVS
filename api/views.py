from adrf.viewsets import ViewSet


import os.path
import random

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from MMVS.settings import VIDEO_PATH
from api.models import VideoModel
from api.serializers import VideoSerializer, VideoResolutionSerializer
from api.video_scaler import create_process


class VideoViewSet(ViewSet):
    queryset = VideoModel.objects.all()
    serializer_class = VideoSerializer

    async def create(self, request):
        """Method to POST request to load video."""
        serializer = VideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        video = VideoModel(**serializer.validated_data)
        await video.asave()
        data = {
            'id': video.id
        }
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )

    async def partial_update(self, request, pk=None):
        """PATCH-allowed async-method to change video resolution."""
        try:
            video = await VideoModel.objects.aget(pk=pk)
            serializer = VideoResolutionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            video.processing = True
            video.processingSuccess = False
            await video.asave()

        except Exception as error:
            raise ValidationError({'errors': str(error)})

        file_name = video.file.name.removeprefix(VIDEO_PATH).removesuffix('.mp4')
        edited_file_code = random.randint(0, 100000)
        await create_process(
            video_dir_path=VIDEO_PATH,
            file_name=file_name,
            edited_file_code=edited_file_code,
            width=request.data['width'],
            height=request.data['height'],
            initial_video=video
        )

        edited_video_file_name = f"{VIDEO_PATH}{edited_file_code}_{request.data['width']}x{request.data['height']}.mp4"
        edited_video = VideoModel(file=edited_video_file_name)

        await edited_video.asave()

        data = {
            'success': 'True',
            'edited_video_id': edited_video.id
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Method to GET request video by id."""
        video = get_object_or_404(VideoModel, pk=pk)
        data = {
            'id': video.id,
            'filename': video.file.name.removeprefix(VIDEO_PATH).removesuffix('.mp4'),
            'processing': video.processing,
            'processingSuccess': video.processingSuccess,
        }

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        """Method to DELETE request video by id."""
        try:
            video = get_object_or_404(VideoModel, pk=pk)
            path = video.file.name

            if os.path.isfile(path):
                os.remove(path)
            video.delete()

            data = {'success': True}
            current_status = status.HTTP_200_OK

        except Exception as error:
            data = {
                'error': str(error)
            }
            current_status = status.HTTP_400_BAD_REQUEST

        return Response(
            data=data,
            status=current_status
        )
