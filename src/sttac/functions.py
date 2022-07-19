from vosk import Model, KaldiRecognizer, SetLogLevel
from tqdm import tqdm
import sys
import os
import wave
import json

def check_model(path: str) -> None:
    if not os.path.exists(path):
        print("\nVosk Model Not Found\n")
        exit(1)

def check_src(path: str) -> None:
    if not os.path.exists(path):
        print("\nSource File Not Found\n")
        exit(1)

def extract_text(file_path: str, model_path: str, debug: int = 0):
    """
    Extract text from source audio file

    Parameter:
        file_path (str): Path of the source file
        model_path (str): Path of the Vosk Model
        debug (int): Use -1 to disable debug model. (Enable by default)
    """
    check_src(file_path)
    check_model(model_path)
    SetLogLevel(debug) 

    wf = wave.open(file_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or \
       wf.getframerate() != 16000 or wf.getcomptype() != "NONE":
        print("Audio file must be mono WAV with 16kHz sample rate.")
        exit(1)

    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())

    # set up for process bar
    print("Starting Recognition Process...\n")
    pbar = tqdm(total=os.path.getsize(file_path))

    while True:
        data = wf.readframes(4000)
        if len(data) == 0: # reach the end
            break
        
        pbar.update(len(data))
        rec.AcceptWaveform(data)

    final_result = json.loads(rec.FinalResult())['text']
    print(final_result)

if __name__ == "__main__":
    extract_text("../../tests/bbc.wav", "../../model", -1)