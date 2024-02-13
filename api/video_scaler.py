import time

import ffmpeg
import os


async def start_process(process):
    """Method to async start ffmpeg-process"""
    process.communicate()


async def create_process(video_dir_path: str, file_name: str, width: int, height: int):
    """Method to create ffmpeg-processes.file_name without .mp4."""
    resolution = f"{str(width)}:{str(height)}"
    input_file_path = video_dir_path + file_name + '.mp4'
    output_file_path = f"{video_dir_path}{file_name}_{width}x{height}.mp4"
    print(output_file_path)
    await start_process(
        ffmpeg
        .input(input_file_path)
        .output(
            os.path.join(output_file_path),
            vf=f'scale={resolution}'
        )
        .run_async()
    )
