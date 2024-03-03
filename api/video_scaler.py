import time

import ffmpeg
import os

from api.models import VideoModel


async def start_process(process, initial_video: VideoModel):
    """Method to async start ffmpeg-process"""
    process.communicate()
    initial_video.processing = False
    initial_video.processingSuccess = True
    await initial_video.asave()


async def create_process(
        video_dir_path: str,
        file_name: str,
        edited_file_code: int,
        width: int,
        height: int,
        initial_video: VideoModel):
    """Method to create ffmpeg-processes.file_name without .mp4."""
    resolution = f"{str(width)}:{str(height)}"
    input_file_path = video_dir_path + file_name + '.mp4'
    output_file_path = f"{video_dir_path}{edited_file_code}_{width}x{height}.mp4"
    await start_process(
        ffmpeg
        .input(input_file_path)
        .output(
            os.path.join(output_file_path),
            vf=f'scale={resolution}'
        )
        .run_async(),
        initial_video=initial_video
    )
