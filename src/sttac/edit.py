import ffmpeg
from os import path
from pydub import AudioSegment

# global variables
CHANNEL = 1
SAMPLE_RATE = 16000

def to_wav(src: str, start: int = 0, duration: int = -1) -> None:
    """
    Convert and trim source file to .wav file in required format

    Parameter:
        src (str): Path of source audio file
        start (int): Timestamp starting to trim the audio in seconds
        duration (int): Length of the audio segment after trimming
    """
    if not path.exists(src):
        raise FileNotFoundError("Source File Not Found")
    
    pathname, ext = path.splitext(src)
    output_name = pathname + ".wav"
    ffmpeg.input(src).output(output_name).run()

    set_format(output_name, start, duration)

def set_format(src: str, start: int = 0, duration: int = -1) -> None:
    """
    Convert and trim source .wav file to required format

    Parameter:
        src (str): Path of source audio file
        start (int): Timestamp starting to trim the audio in seconds
        duration (int): Length of the audio segment after trimming
    """
    if not path.exists(src):
        raise FileNotFoundError("Source File Not Found")

    audio = AudioSegment.from_wav(src)
    audio = audio.set_channels(CHANNEL) # set to mono
    audio = audio.set_frame_rate(SAMPLE_RATE) # set to 16kHz

    if duration != -1:
        audio = audio[start*1000: (start+duration)*1000]
    else:
        audio = audio[start*1000:]

    audio.export(src, format="wav")

if __name__ == "__main__":
    to_wav("../../tests/bbc.mov", duration=30)