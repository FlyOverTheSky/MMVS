from rest_framework import serializers


from api.models import VideoModel


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoModel
        fields = ['file']


class VideoResolutionSerializer(serializers.Serializer):
    width = serializers.IntegerField(min_value=20)
    height = serializers.IntegerField(min_value=20)

    def validate_width(self, parameter):
        if parameter % 2 != 0:
            raise serializers.ValidationError("Параметр ширина должен быть четным.")

    def validate_height(self, parameter):
        if parameter % 2 != 0:
            raise serializers.ValidationError("Параметр высота должен быть четным.")
