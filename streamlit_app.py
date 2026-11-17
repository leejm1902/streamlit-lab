import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="생성 AI 응용 프로그래밍",
    page_icon="🤖",
    layout="wide"
)

# 사이드바: OpenAI API Key 입력
with st.sidebar:
    st.title("설정")

    api_key = st.text_input(
        "OpenAI API Key",
        type="password"
    )

    st.caption(
        "API Key는 코드나 GitHub에 저장하지 않고 "
        "이 웹페이지에서 직접 입력합니다."
    )

# API Key가 입력되면 client를 session_state에 저장
if api_key:
    if (
        "openai_api_key" not in st.session_state
        or st.session_state.openai_api_key != api_key
    ):
        st.session_state.openai_api_key = api_key
        st.session_state.openai_client = OpenAI(
            api_key=api_key
        )
else:
    st.session_state.pop(
        "openai_client",
        None
    )

    st.session_state.pop(
        "openai_api_key",
        None
    )

# 페이지 네비게이션
pg = st.navigation(
    [
        st.Page(
            "app_pages/Home.py",
            title="Home",
            icon=":material/home:",
            default=True
        ),
        st.Page(
            "app_pages/Chat.py",
            title="Chat",
            icon=":material/chat:"
        ),
        st.Page(
            "app_pages/Chatbot.py",
            title="Library Chatbot",
            icon=":material/local_library:"
        ),
        st.Page(
            "app_pages/ChatPDF.py",
            title="ChatPDF",
            icon=":material/picture_as_pdf:"
        ),
    ]
)

pg.run()