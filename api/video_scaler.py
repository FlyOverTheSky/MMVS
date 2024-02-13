import ffmpeg
import os


async def start_process(process):
    await process.communicate()


async def create_process(video_dir_path: str, file_name: str, output_video_resolution: str):
    """file_name without .mp4, output_video_resolution exm:(1000:1000)."""
    await start_process(
        ffmpeg
        .input(os.path.join(video_dir_path, file_name, '.mp4'))
        .output(
            os.path.join((video_dir_path, file_name, f'_{output_video_resolution}.mp4')),
            vf=f'scale={output_video_resolution}'
        )
        .run_async(pipe_stdin=True, pipe_stdout=True)
    )
