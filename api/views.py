from asgiref.sync import sync_to_async

import os.path

from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from MMVS.settings import VIDEO_PATH
from api.models import VideoModel
from api.serializers import VideoSerializer, VideoResolutionSerializer
from api.video_scaler import create_process


class VideoViewSet(viewsets.ModelViewSet):
    queryset = VideoModel.objects.all()
    serializer_class = VideoSerializer

    def create(self, request):
        serializer = VideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        video = VideoModel(**serializer.validated_data)
        video.save()
        data = {
            'id': video.id
        }
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )

    @sync_to_async
    def partial_update(self, request, pk=None):
        video = get_object_or_404(VideoModel, pk=pk)

        serializer = VideoResolutionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        output_video_resolution = f"{request.data['width']}:{request.data['height']}"
        file_name = video.file.name.removeprefix(VIDEO_PATH).removesuffix('.mp4')
        create_process(
            video_dir_path=VIDEO_PATH,
            file_name=file_name,
            output_video_resolution=output_video_resolution
        )

        return Response(
            data={'success': 'True'}
        )

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
