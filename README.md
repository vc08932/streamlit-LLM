## 代码解释 (By ChatGPT)
这段代码实现了一个类似于ChatGPT的聊天机器人。下面是对代码的逐行解释：

1. `from openai import OpenAI`: 导入名为OpenAI的自定义模块，用于与OpenAI API进行交互。
2. `import streamlit as st`: 导入Streamlit模块，用于创建交互式Web应用。
3. `st.title("ChatGPT-like clone")`: 在应用中显示标题为"ChatGPT-like clone"。
4. `client = OpenAI(api_key=st.secrets["openai_api"])`: 创建一个OpenAI客户端对象，使用Streamlit的secrets模块获取OpenAI API的密钥。
5. `if "openai_model" not in st.session_state:`: 检查会话状态中是否存在"openai_model"变量，如果不存在则执行下面的代码。会话状态是一个存储应用程序状态的字典。
6. `st.session_state["openai_model"] = "gpt-3.5-turbo"`: 将会话状态中的"openai_model"设置为"gpt-3.5-turbo"，这是ChatGPT模型的名称。
7. `if "messages" not in st.session_state:`: 检查会话状态中是否存在"messages"变量，如果不存在则执行下面的代码。
8. `st.session_state.messages = []`: 将会话状态中的"messages"初始化为空列表，用于存储聊天历史记录。
9. `for message in st.session_state.messages:`: 遍历会话状态中的每个消息。
10. `with st.chat_message(message["role"]):`: 使用给定的角色创建一个聊天消息块。角色可以是"user"或"assistant"。
11. `st.markdown(message["content"])`: 在聊天消息块中显示消息的内容。
12. `if prompt := st.chat_input("What is up?"):`: 显示一个聊天输入框，并将用户输入的内容赋值给prompt变量。如果用户输入了内容（非空），则执行下面的代码。
13. `st.session_state.messages.append({"role": "user", "content": prompt})`: 将用户的输入作为消息添加到会话状态的消息列表中，角色为"user"。
14. `with st.chat_message("user"):`: 创建一个用户角色的聊天消息块。
15. `st.markdown(prompt)`: 在聊天消息块中显示用户的输入内容。
16. `st.write(st.session_state.messages)`: 在应用中显示当前的聊天历史记录。
17. `with st.chat_message("assistant"):`: 创建一个助手角色的聊天消息块。
18. `stream = client.chat.completions.create(...)`: 调用OpenAI API的chat.completions.create方法，使用之前的聊天历史记录向助手请求生成回复。
19. `response = st.write_stream(stream)`: 从OpenAI API的响应流中读取助手的回复，并将其赋值给response变量。
20. `st.session_state.messages.append({"role": "assistant", "content": response})`: 将助手的回复作为消息添加到会话状态的消息列表中，角色为"assistant"。

这段代码实现了一个简单的聊天机器人应用，用户可以在聊天输入框中与机器人进行对话，机器人会调用OpenAI API生成回复，并将对话历史记录显示在应用中。