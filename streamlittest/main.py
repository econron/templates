import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)


def main():
    llm = ChatOpenAI(temperature=0)

    st.set_page_config(
        page_title="My Great ChatGPT",
        page_icon="🤗"
    )
    st.header("My Great ChatGPT 🤗")

    st.sidebar.title("Options")
    model = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.1)

    # Streamlitはmarkdownを書けばいい感じにHTMLで表示してくれます
    # (もちろんメイン画面でも使えます)
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown("**Total cost**")
    for i in range(3):
        st.sidebar.markdown(f"- ${i+0.01}")  # 説明のためのダミー

    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]

    # ユーザーの入力を監視
    if user_input := st.chat_input("聞きたいことを入力してね！"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is typing ..."):
            response = llm(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    # チャット履歴の表示
    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else:  # isinstance(message, SystemMessage):
            st.write(f"System message: {message.content}")


if __name__ == '__main__':
    main()