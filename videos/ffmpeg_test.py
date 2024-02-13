import ffmpeg
import os
import time
input_file_name = "test_video_high_res.mp4"
input_file_path = os.path.join(os.getcwd(), input_file_name)
output_file_name = "test_video_high_res_result.mp4"
output_file_path = os.path.join(os.getcwd(), output_file_name)

input_file_name_2 = "test_video_high_res_2.mp4"
input_file_path_2 = os.path.join(os.getcwd(), input_file_name_2)
output_file_name_2 = "test_video_high_res_result_2.mp4"
output_file_path_2 = os.path.join(os.getcwd(), output_file_name_2)


# stream = ffmpeg.input(input_file_path)
# stream = ffmpeg.output(stream, output_file_path, vf='scale=150:150')
# ffmpeg.run(stream)


process1 = (
    ffmpeg
    .input(input_file_path)
    .output(output_file_path, vf='scale=1000:1000')
    .run_async(pipe_stdin=True, pipe_stdout=True)
)

process2 = (
    ffmpeg
    .input(input_file_path_2)
    .output(output_file_path_2, vf='scale=1000:1000')
    .run_async(pipe_stdin=True, pipe_stdout=True)
)


async def start_process(process):
    await process.communicate()


print('Start')
start_process(process1)
print('Equator')
start_process(process2)
print('Finish')

