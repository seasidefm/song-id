import subprocess

command = "ffmpeg -i {FILE_NAME}.mp4 {FILE_NAME}.mp3"


def convert_mp4_to_mp3(filename: str) -> str:
    isolated_filename = filename[:-4]
    subprocess.run(
        command.replace("{FILE_NAME}", isolated_filename).split(' ')
    )

    return f"{isolated_filename}.mp3"
