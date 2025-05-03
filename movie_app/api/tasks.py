import os
import subprocess

def convert_480p(source):
    output_dir = os.path.dirname(source)
    target = os.path.join(output_dir, "480p.m3u8")
    ts_pattern = os.path.join(output_dir, "480p_%03d.ts")

    cmd = (
        f'ffmpeg -i "{source}" '
        f'-vf scale=854:480 -c:a aac -ar 48000 -b:a 96k '
        f'-c:v h264 -profile:v main -preset veryfast -crf 28 '
        f'-g 48 -keyint_min 48 -sc_threshold 0 '
        f'-b:v 600k -maxrate 700k -bufsize 1000k '
        f'-hls_time 4 -hls_playlist_type vod '
        f'-hls_segment_filename "{ts_pattern}" "{target}"'
    )
    print(f"[480p HLS] Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

def convert_720p(source):
    output_dir = os.path.dirname(source)
    target = os.path.join(output_dir, "720p.m3u8")
    ts_pattern = os.path.join(output_dir, "720p_%03d.ts")

    cmd = (
        f'ffmpeg -i "{source}" '
        f'-vf scale=1280:720 -c:a aac -ar 48000 -b:a 96k '
        f'-c:v h264 -profile:v main -preset veryfast -crf 28 '
        f'-g 48 -keyint_min 48 -sc_threshold 0 '
        f'-b:v 1200k -maxrate 1400k -bufsize 2000k '
        f'-hls_time 4 -hls_playlist_type vod '
        f'-hls_segment_filename "{ts_pattern}" "{target}"'
    )
    print(f"[720p HLS] Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

def convert_1080p(source):
    output_dir = os.path.dirname(source)
    target = os.path.join(output_dir, "1080p.m3u8")
    ts_pattern = os.path.join(output_dir, "1080p_%03d.ts")

    cmd = (
        f'ffmpeg -i "{source}" '
        f'-vf scale=1920:1080 -c:a aac -ar 48000 -b:a 96k '
        f'-c:v h264 -profile:v main -preset veryfast -crf 28 '
        f'-g 48 -keyint_min 48 -sc_threshold 0 '
        f'-b:v 2500k -maxrate 2800k -bufsize 3500k '
        f'-hls_time 4 -hls_playlist_type vod '
        f'-hls_segment_filename "{ts_pattern}" "{target}"'
    )
    print(f"[1080p HLS] Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)


