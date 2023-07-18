import gtts, googletrans
from moviepy.editor import VideoFileClip, AudioFileClip
import speech_recognition as sr
import os

t = googletrans.Translator()
r = sr.Recognizer()

resultName = "result"
def split_video(video_path):
    video = VideoFileClip(video_path)
    video_without_audio = video.without_audio()
    audio = video.audio

    video_without_audio.write_videofile("output_video.mp4")
    audio.write_audiofile("output_audio.wav")

    video.close()
    audio.close()

def transcribe_speech(filename):
    with sr.AudioFile(filename) as source:
        audio_listened = r.record(source)
        text = r.recognize_google(audio_listened, language='en-US')
        return text

def translate_text(text):
    translation = t.translate(text, 'ru', 'en')
    return translation.text

def tts(text):
    voice= gtts.gTTS(text, lang="ru")
    voice.save('translation_audio.wav')

def save_result():
    video = VideoFileClip("output_video.mp4")
    audio = AudioFileClip('translation_audio.wav')

    video = video.set_audio(audio)
    video.write_videofile(f'{resultName}.mp4')

split_video('filename.mp4')
text = translate_text(transcribe_speech("output_audio.wav"))
tts(text)
save_result()

os.remove("output_video.mp4")
os.remove("output_audio.wav")
os.remove('translation_audio.wav')