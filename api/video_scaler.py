import ffmpeg
import os


async def start_process(process):
    process.communicate()


async def create_process(video_dir_path: str, file_name: str, width: int, height: int):
    """file_name without .mp4, output_video_resolution exm:(1000:1000)."""
    resolution = f"{str(width)}:{str(height)}"
    input_file_path = video_dir_path + file_name + '.mp4'
    output_file_path = video_dir_path + file_name + '_edited.mp4'
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
