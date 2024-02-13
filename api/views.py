from adrf.viewsets import ViewSet


import os.path

from asgiref.sync import sync_to_async
from rest_framework import viewsets, status
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
        video = await VideoModel.objects.aget(pk=pk)

        serializer = VideoResolutionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_name = video.file.name.removeprefix(VIDEO_PATH).removesuffix('.mp4')
        await create_process(
            video_dir_path=VIDEO_PATH,
            file_name=file_name,
            width=request.data['width'],
            height=request.data['height']

        )
        edited_video_file_name = f"{VIDEO_PATH}{file_name}_{request.data['width']}x{request.data['height']}.mp4"
        edited_video = VideoModel(file=edited_video_file_name)
        await edited_video.asave()
        data = {
            'success': 'True',
            'edited_video_id': edited_video.id
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
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
