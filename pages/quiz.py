import streamlit as st 
import json
import time
import logging


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


# if 'logger' not in st.session_state:
#     st.session_state['logger'] = st_log.create_logger(name = 'app', level = 'INFO')
# logger = st.session_state['logger']
# print(st.session_state['logger'])
   
# def redirect():
#     st.switch_page("pages/chatbot.py")
st.set_page_config(initial_sidebar_state = "collapsed")    
        
if "level" not in st.session_state:
    st.session_state.level = []
    
elif len(st.session_state.level) >= 1:
        st.success(f" **你已經填寫過了，請回到你原本的頁面**",icon = "⭕")
        time.sleep(1)
        st.switch_page("pages/chatbot.py")
        
else:
    with st.form("Quiz"):
        st.markdown("## 做一个小测试吧 💯")
        
        score = 0
        
        with open("quiz_question.json",encoding='utf-8') as file:
            ques=json.load(file,strict=False) # strict=False allows to store '\n','\t' etc. 
        
        for i in ("Q1","Q2","Q3","Q4","Q5","Q6"):
            #st.write(ques[i]["Choice"][1])
            question = st.radio(
                f"**{str(i)[1]} . {ques[i]["Question"]}**", 
                [ques[i]["Choice"][k] for k in range(4)],
                index = None) # Set preselected option be None
            
            ans_index = int(ques[i]["Ans"])
            if question == ques[i]["Choice"][ans_index]:
                st.write(":red[✅ 恭喜你，答對了]")
                score += 1
                logger.info(f"QuizAns: {question}")
                #log_info(f"QuizAns: {question}")
                
            elif question is not None:
                logger.info(f"QuizAns: {question}")
                
                #log_info(f"QuizAns: {question}")
                st.write(":grey[❌ 沒關係，再接再厲]")
                st.markdown(f'正确答案是 **{ques[i]["Choice"][ans_index]}**')
                     
                
            st.divider()
        
                
        if  st.form_submit_button("遞交", type = "primary") == True:         
            
            st.subheader(f":blue[你的分數：**{score}**]")
        
            if score >= 5:
                st.page_link("pages/chatbot.py", label="**你已經是熟練級別了**")
                st.session_state.level.append("expert")
                
            elif score >=3 :
                st.page_link("pages/chatbot.py", label="**你已經到了已入門等級了**")
                st.session_state.level.append("intermediate")
                
            elif score >=0:
                st.page_link("pages/chatbot.py", label="**你看來不是很熟悉大語言模型了**")
                st.session_state.level.append("begin")

            st.toast("請點擊按鈕跳到指定頁面，否則將在 10 秒後自動跳轉",icon = "💬")
            
            time.sleep(10)
            st.switch_page("pages/chatbot.py")