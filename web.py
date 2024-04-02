from openai import OpenAI
import streamlit as st

st.title("ChatGPT-like clone")

client = OpenAI(api_key=st.secrets["openai_api"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo" # Set model

if "messages" not in st.session_state: # Initialize chat history
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"]) # Print message

preset_prompt = """你是一个电脑专家，你要以浅白的语言和详细的说明，教导弱势社群如何使用电子设备和软件，
对于专有名词，你要另外用括号包裹着解释；以及每个步骤都尝试拓展；还要尽量用点列式的方法排版。\n"""

if prompt := st.chat_input("What is up?"): #:= 赋值 + 判断
    st.session_state.messages.append({"role": "user", "content": preset_prompt + prompt})
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
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})