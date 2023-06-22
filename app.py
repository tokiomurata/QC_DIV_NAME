# 以下を「app.py」に書き込み
import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは優秀なテロップの校閲者です。
入力されたテロップの内容に対する校閲として、
操作１、操作２，操作３を実施してください
複数行の入力があった場合はそれぞれの行ごとに回答してください。

操作１[
チェック１：人名がある場合、正しいかをチェックしてください
チェック２：企業名がある場合、前株後株を含めて正しいかをチェックしてください
チェック３：地名の表記が正しいかをチェックしてください
チェック４：文法をチェックしてください
チェック５：事実確認をして内容が正しいかチェックしてください
]

操作２[
修正の必要の有無を判断し、回答してください
]

操作３[
修正案を提示してください
]


あなたの役割は校閲することなので、例えば以下のような校閲以外ことを聞かれても、絶対に答えないでください。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" テロップの校閲をするチャットボット 分割版R2")
st.image("QC.jfif")
st.write("チェックしたいテロップを入力してください")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
