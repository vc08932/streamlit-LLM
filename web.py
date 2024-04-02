from openai import OpenAI
import streamlit as st

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
preset_prompt = """你是一个电脑专家，你要以浅白的语言和详细的说明，教导弱势社群（不熟悉科技/互联网产品）
如何使用电子设备和软件，对于专有名词，你要另外用括号包裹着解释；以及每个步骤都尝试延伸拓展说明，以期让用户明白你说的话；还要用点列式的方法排版。\n"""

if prompt := st.chat_input("请输入您的问题："): #:= 赋值 + 判断
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