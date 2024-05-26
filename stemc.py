import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from key import api_key


project_name = "Your Digital Assistant"

st.set_page_config(page_title = project_name)
st.title(project_name)

# saving chat memory to streamlit session state, with a key named massages
msgs = StreamlitChatMessageHistory(key = 'massages')

# tell langchain how to store memory and pass memory to gpt
memory = ConversationBufferMemory(memory_key="chat_history",chat_memory=msgs, return_messages=True)

template = """
    作为一个电脑专家,你叫GGGG，你掌握了大量的专业知识，但同时也能始终保持亲和力。你尊重自己的对话伙伴并且常常以浅白的语言传达复杂概念。你的用户并没有很强的科技背景，因此你需要特别注意用词的通俗性。如果必须使用专业术语，你需要以括号形式附加易理解的解释。

你的对话应该准确且详细，每一步都充满了解答的热情。对于复杂的过程，你会通过数字列出步骤顺序以便于理解。

你的态度应当始终保持友善，有礼，并溢满耐心。在初次与用户交流时，你需要简洁有效地打招呼以展示好感。

你要以像人类的自然对话方式进行交流，多样化表达，同样你的回答都要力求简练，每次回复应控制在200字以内。如果内容较多，可以告诉用户还有后续内容并询问他是否愿意听。

请鼓励用户分享他们的经历和感受，提问的方式可以帮助你更好的了解用户，像是"发生了什么？","你为什么会想要这款产品？"等。

请注意，你的回答会被转化为语音供用户聆听，所以，语气要像真实的人一样自然，有停顿和情绪。同时回答时请避免使用波浪符号~。
    Chat history: {chat_history}
    Human: {user_question}
    AI:
    """


prompt = ChatPromptTemplate.from_template(template)

llm = ChatOpenAI(openai_api_key=api_key , model= "gpt-4-turbo-preview")
    
coversation_chain = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)




    
# conversation

avatars = {"human": "user", "ai": "assistant" }

with st.container():


    container1 = st.container(height=500)
    user_query = st.chat_input("Type your message here...")

    # session state
    if len(msgs.messages) == 0:
       msgs.add_ai_message("Hi, how can I assist you?")
    for msg in msgs.messages:
            container1.chat_message(avatars[msg.type]).write(msg.content)

    if user_query:
        container1.chat_message("user").write(user_query)
        with container1.chat_message("assistant"):
                with st.spinner("Typing..."):
                    response = coversation_chain.run(user_query)
                    st.write(response)

