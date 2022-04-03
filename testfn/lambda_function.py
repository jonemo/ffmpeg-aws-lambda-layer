import ffmpeg
import subprocess


def codecs():
    ffmpeg_cmd = [
        "ffmpeg",
        "-codecs",
    ]
    print(f"ffmpeg command: {' '.join(ffmpeg_cmd)}")
    subprocess.run(ffmpeg_cmd)

    ffmpeg_cmd = [
        "ffmpeg",
        "-encoders",
    ]
    print(f"ffmpeg command: {' '.join(ffmpeg_cmd)}")
    subprocess.run(ffmpeg_cmd)


def timelapse():
    return (
        ffmpeg
        .input('./jpegs/*.JPG', pattern_type='glob', framerate=23.976, codec="libx264")
        # https://ffmpeg.org/ffmpeg-filters.html#deflicker
        .filter('deflicker', mode='pm', size=5)
        # https://ffmpeg.org/ffmpeg-filters.html#scale-1
        .filter('scale', size='hd1080')
        # https://ffmpeg.org/ffmpeg-filters.html#crop
        .filter('crop', '1920:1080')
        # https://superuser.com/questions/856025/any-downsides-to-always-using-the-movflags-faststart-parameter
        # https://write.corbpie.com/ffmpeg-preset-comparison-x264-2019-encode-speed-and-file-size/
        .output('movie.mp4', crf=20, preset='slow', movflags='faststart')
        .compile()
        # .view(filename='filter_graph')
        # .run()
    )


def lambda_handler(event, context):
    print("starting")
    codecs()
    ffmpeg_cmd = timelapse()
    print("stopping")
    return {"status": 200, "body": {"hello": "world", "ffmpeg_cmd": " ".join(ffmpeg_cmd)}}
