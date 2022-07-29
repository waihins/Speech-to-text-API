from vosk import Model, KaldiRecognizer, SetLogLevel
from tqdm import tqdm
import sys
import os
import wave
import json
import srt
import datetime
from transformers import logging
from recasepunc import CasePuncPredictor
from recasepunc import WordpieceTokenizer

# global variables
CHANNEL = 1
SAMPLE_RATE = 16000
WORDS_PER_LINE = 10

def check_model(path: str) -> None:
    if not os.path.exists(path):
        print("\nVosk Model Not Found\n")
        exit(1)

def check_src(path: str) -> None:
    if not os.path.exists(path):
        print("\nSource File Not Found\n")
        exit(1)

def extract_text(file_path: str, model_path: str, debug: int = 0) -> str:
    """
    Extract text from source audio file

    Parameter:
        file_path (str): Path of the source file
        model_path (str): Path of the Vosk Model
        debug (int): Use -1 to disable debug model. (Enable by default)
    
    Return:
        Speech recognition result as string
    """
    check_src(file_path)
    check_model(model_path)
    SetLogLevel(debug) 

    wf = wave.open(file_path, "rb")
    if wf.getnchannels() != CHANNEL or wf.getsampwidth() != 2 or \
       wf.getframerate() != SAMPLE_RATE or wf.getcomptype() != "NONE":
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
    
    return final_result

def generate_srt(file_path: str, model_path: str, debug: int = 0) -> None:
    """
    Generate SRT file for the source audio file

    Parameter:
        file_path (str): Path of the source file
        model_path (str): Path of the Vosk Model
        debug (int): Use -1 to disable debug model. (Enable by default)
    
    Return:
        None
    """
    check_src(file_path)
    check_model(model_path)
    SetLogLevel(debug) 

    wf = wave.open(file_path, "rb")
    if wf.getnchannels() != CHANNEL or wf.getsampwidth() != 2 or \
       wf.getframerate() != SAMPLE_RATE or wf.getcomptype() != "NONE":
        print("Audio file must be mono WAV with 16kHz sample rate.")
        exit(1)

    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # set up for process bar
    print("Generating SRT file...\n")
    pbar = tqdm(total=os.path.getsize(file_path))

    results = []
    while True:
       data = wf.readframes(4000)
       if len(data) == 0: # reach the end
           break
       pbar.update(len(data))

       if rec.AcceptWaveform(data):
           results.append(rec.Result())

    results.append(rec.FinalResult())

    subs = []
    for i, res in enumerate(results):
       jres = json.loads(res)
       if not 'result' in jres:
           continue
       words = jres['result']
       for j in range(0, len(words), WORDS_PER_LINE):
           line = words[j : j + WORDS_PER_LINE] 
           s = srt.Subtitle(index=len(subs), 
                   content=" ".join([l['word'] for l in line]),
                   start=datetime.timedelta(seconds=line[0]['start']), 
                   end=datetime.timedelta(seconds=line[-1]['end']))
           subs.append(s)

    name, ext = os.path.splitext(file_path)
    filename = name + "-substitled.srt"
    file = open(filename, "w")
    file.write(srt.compose(subs))
    file.close()

# Adapted from example.py (https://github.com/benob/recasepunc)
def reformat(result: str) -> str:
    """
    Add punctuations and recase the speech recognition result

    Parameter:
        result (str): result from the recognition process
    
    Return:
        None
    """
    # check recasepunc model:
    if not os.path.exists("checkpoint"):
        print("Recasepunc Model Not Found")
        exit(1)
    
    logging.set_verbosity_error()
    predictor = CasePuncPredictor('checkpoint')
    tokens = list(enumerate(predictor.tokenize(result)))

    results = ""
    for token, case_label, punc_label in predictor.predict(tokens, lambda x: x[1]):
        prediction = predictor.map_punc_label(predictor.map_case_label(token[1], case_label), punc_label)
        results = results + ' ' + prediction

    return results.strip()

def save_file(result: str, filename: str, format: bool) -> None:
    """
    Save recognition result (raw string) as a txt file

    Parameter:
        result (str): result from the recognition process
        filename (str): name of the output txt file
        reformat (bool): True to format the output, False otherwise
    
    Return:
        None
    """
    print("Saving results to txt files...\n")
    file = open(filename, "w")
    output = result
    if format:
        output = reformat(result)
    file.write(output)
    file.close()

if __name__ == "__main__":
    result = extract_text("tests/bbc.wav", "model", -1)
    save_file(result, "tests/result.txt", False)
    # generate_srt('tests/cs241-part8.wav', 'model', -1)