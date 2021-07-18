import requests
import wave, math, contextlib
import speech_recognition as sr
import re
from googletrans import Translator,constants
from moviepy.editor import AudioFileClip
file_name=""
f_name=""
def video(url):
    #file_name = url.split('/')[-1]+".mp4"
    global file_name
    file_name="video12.mp4"
    print( "Downloading file:%s"%file_name)

    # create response object
    r = requests.get(url, stream = True)

    # download started
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 1024*1024):
            if chunk:
                f.write(chunk)
    return file_name
url= "provide the url here"
def transcript(url):
    global f_name
    video_file_name ="video3.mp4"
    #video_file_name = video(url)
    transcribed_audio_file_name = video_file_name+"_speech.wav"
    audioclip = AudioFileClip(video_file_name)
    audioclip.write_audiofile(transcribed_audio_file_name)
    with contextlib.closing(wave.open(transcribed_audio_file_name,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    total_duration = math.ceil(duration / 60)
    r = sr.Recognizer()
    f_name=video_file_name+"_transcript.txt";
    f = open(f_name, "a")
    f.write("00:00 ::  ")
    for i in range(0, total_duration):
        with sr.AudioFile(transcribed_audio_file_name) as source:
            audio = r.record(source, offset=i*60, duration=60)
        f.write(r.recognize_google(audio))
        if i%2==0  and i!=0:
            f.write(".\n"+str(i)+":00 ::  ")
    f.close()
    return f_name

#transcript()
def translation(lang):
    trans= Translator()
    f=open(f_name,"r");
    new_lang=open(f_name+lang+".txt","a");
    str=f.read()
    st=str.split('\n')
    for line in st:
        translation=trans.translate(line, dest=lang)
        new_lang.write(translation.text)
        new_lang.write('\n')
    f.close()
    new_lang.close()
    return new_lang;
str=transcript(url)
lan=translation("fr");
