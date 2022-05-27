from pytube import YouTube
import sys, os, subprocess
import argparse
import pyfiglet
import logging
import re
from moviepy.editor import *
# from tqdm import tqdm
# import ffmpeg


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info(" Started running")


def __download_video(link: str) -> bool:
    """
    Method to download the video from youtube
    :param link: str link for the video
    :return: True if downloaded or False is exception occurred
    """
    try:
        video = YouTube(link)
        video_name = re.sub('[^a-zA-Z0-9\n\.]', ' ', video.title).replace(" ", "")
        # video_name = video.title.replace("!@#$%^&*()[]{};:,./<>?\|`~-=_+", " ").replace(" ", '_')
        video.streams.filter(adaptive=True, resolution="1080p").first().download(filename=video_name, output_path="../test_downloads")
        logger.info("Video was Downloaded in the current Directory - {}".format(video.title.replace(" ", '_')))
        __download_audio(link)
        logger.info("Video File Name: " + video.title)
        import os
        print(os.getcwd())
        video_file = VideoFileClip("../test_downloads/" + video_name + ".mp4")
        audio_file = AudioFileClip("../test_downloads/" + "audio_" + video_name + ".mp4")
        video_clip = video_file.set_audio(audio_file)

        print(video_clip)
        video_clip.write_videofile("../test_downloads/output.mp4", fps=60, codec="mpeg4")
        logger.info("The merged file has been saved")
    except Exception as e:
        logger.error("Failed: Exception occured: \n {}".format(e))
        sys.exit(0)

    return True


def __download_audio(link: str) -> bool:
    """
    Method to download the audio from youtube
    :param link: str link for the video
    :return: True if downloaded or False is exception occurred
    """
    try:
        video = YouTube(link)
        audio_name = re.sub('[^a-zA-Z0-9\n\.]', ' ', video.title).replace(" ", "")
        print("video streams: ", video.streams)
        video.streams.filter(adaptive=True, mime_type='audio/mp4').first().download(filename="audio_" + audio_name, output_path="../test_downloads")
        # video.streams.filter(adaptive=True,only_audio=True).first().download(filename="audio_"+video.title+'.mp4')
        logger.info("Audio was Downloaded in the current Directory - {}".format(video.title))
    except Exception as e:
        logger.error("Failed: Exception occured: \n {}".format(e))
        sys.exit(0)
    return True


def main(args):
    print('\n' + pyfiglet.figlet_format("pyMSPyt", font='slant'))
    print("A CLI for downloading Youtube Audio/Video\n")
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--audio_only", help="Downloads only the audio", action="store_true")
    parser.add_argument("-l", "--link", help="Link for the video")

    args = parser.parse_args(args)
    import time

    time.sleep(3)
    if not args.link:
        logger.error("Please enter the link in the following format -> -l <link/url>")
    elif args.audio_only:
        __download_audio(args.link)
    else:
        __download_video(args.link)
    return True


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
