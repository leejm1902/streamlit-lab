import streamlit as st

st.title("💬 Chat")

st.write(
    "gpt-6-luna와 대화할 수 있습니다."
)

# API Client 확인
if "openai_client" not in st.session_state:
    st.warning(
        "왼쪽 사이드바에 OpenAI API Key를 입력해주세요."
    )
    st.stop()

client = st.session_state.openai_client


# 대화 기록 초기화
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


def clear_chat():
    st.session_state.chat_messages = []


# Clear 버튼
st.button(
    "Clear",
    on_click=clear_chat
)


# 이전 대화 출력
for message in st.session_state.chat_messages:
    with st.chat_message(
        message["role"]
    ):
        st.write(
            message["content"]
        )


# 사용자 입력
prompt = st.chat_input(
    "메시지를 입력하세요"
)


if prompt:

    # 사용자 메시지 저장
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # 사용자 메시지 화면 출력
    with st.chat_message("user"):
        st.write(prompt)


    # GPT 응답
    with st.chat_message("assistant"):

        try:
            stream = client.responses.create(
                model="gpt-6-luna",
                input=st.session_state.chat_messages,
                stream=True
            )

            response = st.write_stream(
                stream
            )

        except Exception as e:
            response = (
                f"오류가 발생했습니다: {e}"
            )

            st.error(response)


    # Assistant 메시지 저장
    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )