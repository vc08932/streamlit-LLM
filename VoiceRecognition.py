# pip install SpeechRecognition
# pip install audio-recorder-streamlit
# cd streamlit-LLM
# streamlit run VoiceRecognition.py

#streamlit run VoiceRecognition.py
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr

st.button("Reset", type="primary")

audio = audio_recorder()
if audio:
    audio_file = "audio_file.wav"
    with open(audio_file, "wb") as f:
        f.write(audio)
if st.button('Text'):
    r =sr.Recognizer()
    with sr.AudioFile("audio_file.wav") as source :
        audio2 =r.record(source)
        
    try:
        st.write(r.recognize_google(audio2, language='zh-CN'))
    except sr.UnknownValueError:
        st.write('Google Speech Recognition could not understand audio')
    except sr.RequestError as e:
        st.write('could not request results from Google speech Recognition service')
