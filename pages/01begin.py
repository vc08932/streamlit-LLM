from openai import OpenAI
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from pathlib import Path
import os

st.title("你的数码小助手")
client = OpenAI(api_key=st.secrets["openai_api"])
system_prompt="""你的人设是:
作为一个电脑专家，你掌握了大量的专业知识，但同时也能始终保持亲和力。你尊重自己的对话伙伴并且常常以浅白的语言传达复杂概念。你的用户并没有很强的科技背景，因此你需要特别注意用词的通俗性。如果必须使用专业术语，你需要以括号形式附加易理解的解释。

你的对话应该准确且详细，每一步都充满了解答的热情。对于复杂的过程，你会通过数字列出步骤顺序以便于理解。

你的态度应当始终保持友善，有礼，并溢满耐心。在初次与用户交流时，你需要简洁有效地打招呼以展示好感。

你要以像人类的自然对话方式进行交流，多样化表达，同样你的回答都要力求简练，每次回复应控制在200字以内。如果内容较多，可以告诉用户还有后续内容并询问他是否愿意听。

请鼓励用户分享他们的经历和感受，提问的方式可以帮助你更好的了解用户，像是"发生了什么？","你为什么会想要这款产品？"等。

请注意，你的回答会被转化为语音供用户聆听，所以，语气要像真实的人一样自然，有停顿和情绪。同时回答时请避免使用波浪符号~。

首次对话你要以简短的方式打招呼"""
#tts = st.checkbox("Text to Voice")
#vtt=""
#audio_record = audio_recorder(text="",icon_size="5x")
gpt_response="gpt_response"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4" # Set model

if "messages" not in st.session_state: # Initialize chat history
    st.session_state.messages = []
    
for message in st.session_state.messages: # Print message
   with st.chat_message(message["role"]):
        st.markdown(message["content"])

def text_to_speech(text, speech_file_path): #text to speech   
    # 替换为您的 OpenAI API 密钥
    speech_response = client.audio.speech.create(
        model="tts-1",
        voice="Nova",
        input=text
    )
    with open(speech_file_path, 'wb') as file:
        file.write(peech_response.content)

def call_gpt():
    global gpt_response
    with st.chat_message("assistant"): 
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
        gpt_response=st.write_stream(stream)# Print out your input
        #if tts:# text to speech for every gpt response
        #    text_to_speech(response,"speech.mp3")
        #    st.audio("speech.mp3", format="audio/mpeg", loop=False)
    return gpt_response

def voice_recognition(audio_path):
    recognizer =sr.Recognizer()
    with sr.AudioFile(audio_path) as source :
        audio =recognizer.record(source)
    try:
        voice_to_text = recognizer.recognize_google(audio, language='zh-CN')
    except sr.UnknownValueError:
        voice_to_text ='Google Speech Recognition could not understand audio'
    except sr.RequestError as e:
        voice_to_text ='could not request results from Google speech Recognition service'
    return voice_to_text

if len(st.session_state.messages) < 1:
    st.session_state.messages.append({"role": "system", "content":system_prompt})
    call_gpt()
    
#if audio_record:
#    with open("audio_file.wav", "wb") as f:
#        f.write(audio_record)
#    vtt=voice_recognition("audio_file.wav")


if prompt := st.chat_input("请输入您的问题："):
    st.session_state.messages.append({"role": "user", "content":prompt})
    with st.chat_message("user"): # Print out your input
        st.write(prompt)
    call_gpt()
    st.session_state.messages.append({"role": "assistant", "content":gpt_response})
    #st.write(st.session_state.messages)
    

    
