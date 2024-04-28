from openai import OpenAI
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from pathlib import Path
import os


st.title("CityU STEM Challenge - LLM Model")

client = OpenAI(api_key=st.secrets["openai_api"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4" # Set model

if "messages" not in st.session_state: # Initialize chat history
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"]) # Print message
        
st.write(st.session_state["openai_model"])


tts=st.checkbox("Text to Voice",)
def text_to_speech(text, path): #text to speech   
    # 替换为您的 OpenAI API 密钥
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    speech_file_path = "speech.mp3"
    with open(speech_file_path, 'wb') as file:
        file.write(response.content)
        
response="gpt response"
def callgpt(): # Call openai's api
    with st.chat_message("assistant"):
=======

preset_prompt = """你是一个电脑专家，你要以浅白的语言和详细的说明，教导弱势社群（不熟悉科技/互联网产品）
如何使用电子设备和软件，对于专有名词，你要另外用括号包裹着解释；以及每个步骤都尝试延伸拓展说明，以期让用户明白你说的话；还要用点列式的方法排版。\n"""

if prompt := st.chat_input("请输入您的问题："): #:= 赋值 + 判断
    
    if len(st.session_state.messages) < 1:
        st.session_state.messages.append({"role": "user", "content": preset_prompt + prompt}) 
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
    
    
    #st.session_state.messages.append({"role": "user", "content": preset_prompt + prompt})
    with st.chat_message("user"): # Print out your input
        st.markdown(prompt)
        
    st.write(st.session_state.messages) # For debug
    
    with st.chat_message("assistant"): # Call openai's api

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            temperature = 0.2, 
            # Set temperature to 0.2 to get more stable and consistent answer
            stream=True,
        )
        global response
        response= st.write_stream(stream)
        if tts:
            text_to_speech(response,"speech.mp3")
            st.audio("speech.mp3", format="audio/mpeg", loop=False)

preset_prompt = """你是一个电脑专家，你要以浅白的语言和详细的说明，教导弱势社群（不熟悉科技/互联网产品）
如何使用电子设备和软件，对于专有名词，你要另外用括号包裹着解释；以及每个步骤都尝试延伸拓展说明，以期让用户明白你说的话；还要用点列式的方法排版。\n"""

if prompt := st.chat_input("请输入您的问题："): #:= 赋值 + 判断
    st.session_state.messages.append({"role": "user", "content": preset_prompt + prompt})
    with st.chat_message("user"): # Print out your input
        st.markdown(prompt)
    st.write(st.session_state.messages) # For debug
    
    callgpt()
    st.session_state.messages.append({"role": "assistant", "content": response})
    
audio_record = audio_recorder(text="",icon_size="5x") #audio record
voice_to_text="no audio recorded" #defined voice_to_text
if audio_record:
    audio_file = "audio_file.wav"
    with open(audio_file, "wb") as f:
        f.write(audio_record)
    recognizer =sr.Recognizer()
    with sr.AudioFile("audio_file.wav") as source :
        audio =recognizer.record(source)
    try:
        voice_to_text = recognizer.recognize_google(audio, language='zh-CN')
    except sr.UnknownValueError:
        voice_to_text ='Google Speech Recognition could not understand audio'
    except sr.RequestError as e:
        voice_to_text ='could not request results from Google speech Recognition service'
        
if st.button(voice_to_text+":white_check_mark:"):
    
    if len(st.session_state.messages) < 1:
        st.session_state.messages.append({"role": "user", "content": preset_prompt + voice_to_text}) 
    else:
        st.session_state.messages.append({"role": "user", "content": voice_to_text})
    with st.chat_message("user"): # Print out your input
        st.markdown(voice_to_text)
    st.write(st.session_state.messages) # For debug
    callgpt()
    st.session_state.messages.append({"role": "assistant", "content": response})
