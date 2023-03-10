""" Ffmpeg utils """

import logging
import subprocess

COMMAND = "ffmpeg -y -hide_banner -loglevel error -i {FILE_NAME}.mp4 {FILE_NAME}.mp3"


def convert_mp4_to_mp3(filename: str) -> str:
    """ Util function to convert mp4 to mp3 using ffmpeg """
    logger = logging.getLogger('song-id')

    isolated_filename = filename[:-4]
    logger.info("Converting %s with ffmpeg...", isolated_filename)

    subprocess.run(
        COMMAND.replace("{FILE_NAME}", isolated_filename).split(' ')
    )

    logger.info("Done with conversion for %s!", isolated_filename)
    return f"{isolated_filename}.mp3"
