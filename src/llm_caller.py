import os
from openai import OpenAI
import streamlit as st

client = OpenAI(
    api_key = st.secrets["openai_api"],
)

def call(*prompt): # [system_prompt, user_prompt]
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt[0], 
            },
            {
                "role": "user",
                "content": prompt[1],
            }
        ],
        model = "gpt-4o-mini",
        temperature =  0.1
    )
    return chat_completion.choices[0].message.content

# print(call("潤色一下這句提示詞，使這句話的用詞和語氣像真实的人一样自然，刪除無用的句子（即是值為 None 的句子），但避免直接修改句子意思和信息量，直接輸出潤色後的結果即可。如果細節與背景明顯無關聯或者細節與背景相衝突，可以忽略和刪除背景，並且改進和優化提示詞。",
#     "背景：我在使用 微信 的 Window 端时遇到困难，版本號為 None；\n細節：在安卓手機里微信浏览器无法下载文件"))