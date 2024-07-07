import streamlit as st
from openai import OpenAI
import logging
import os 

st.set_page_config(
    page_title="Index",
    page_icon="👋",
)
st.title("你的數碼小助手 Your Digital Assistant")

logger = logging.getLogger("Streamlit")
logger.setLevel(logging.INFO)
handler = logging.FileHandler('streamlit.log')
formatter = logging.Formatter("%(asctime)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# logged_messages = set()

# def log_info(log_message):
#     if log_message not in logged_messages:
#         logger.info(log_message)
#         logged_messages.add(log_message)

if "login_status" not in st.session_state or st.session_state["login_status"] == False:
    with st.form("login"):
        st.markdown("## Login Page")
        password = st.text_input("**Password**", type = "password", autocomplete ="password")
        submit = st.form_submit_button()
        
        if submit == True and password.strip() == st.secrets["login"]:
            st.session_state["login_status"] = True
            #logger.info("Login")
            logger.info("Login")
            st.rerun()
        else:
            st.session_state["login_status"] = False 
            
            if submit == True and password != st.secrets["login"]: 
                # Only display with wrong password input
                st.write(":red[Wrong password.Please try again]")
                logger.info("Failed login")

if st.session_state["login_status"] == True:
    st.toast('Successfully logged in', icon="✅")
    st.markdown("""
                ## 簡單介紹
                大家好，歡迎來到我們的網站。 👋
                
                我們希望透過這個項目，讓你們在數碼世界中遇到任何挑戰，都求助有門。
                
                遇到不懂的歡迎前來詢問，我們的親切、耐心的人工智慧會努力解答你的一切問題的 😀
                
                """)

    st.markdown("## 實力評估")
    level = st.radio(
        "**評估一下自己使用 ChatGPT 的實力吧，好讓我們可以更好地幫助你 🤗**", 
        # Radio form's title + Bold the title
        ["🟡 不懂","🟢 已入門","🔵 熟練",],
        captions = ["只能用日常語言與 ChatGPT 溝通",
                    "懂得提示詞的基本概念、有意識使用提示詞",
                    "熟練使用提示詞以獲得想要的回應"],
        index = None) # Set preselected option be None
    
    level_index = {"🟡 不懂":"begin", "🟢 已入門" : "intermediate", "🔵 熟練": "expert"}
    
    if level is not None:
        st.session_state["level"] = level_index[level]
        st.switch_page("pages/chatbot.py")
        
        
    # if level == "🟡 不懂":
    #     logger.info(f"Choice :{level}")
    #     st.switch_page("pages/01begin.py")
        
    # elif level == "🟢 已入门":
    #     logger.info(f"Choice :{level}")
    #     st.switch_page("pages/02intermediate.py")
        
    # elif level == "🔵 熟练":
    #     logger.info(f"Choice :{level}")
    #     st.switch_page("pages/03expert.py")
        
    st.page_link("pages/quiz.py", label="❓ 不知道自己水平？請點擊這裡")

