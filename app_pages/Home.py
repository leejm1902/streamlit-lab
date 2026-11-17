import streamlit as st
import base64

st.title("🏠 Home")

st.write(
    "GPT에게 질문하거나 이미지를 생성할 수 있습니다."
)

if "openai_client" not in st.session_state:
    st.warning(
        "왼쪽 사이드바에 OpenAI API Key를 입력해주세요."
    )
    st.stop()

client = st.session_state.openai_client


@st.cache_data
def ask_gpt(prompt, _client):
    response = _client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )

    return response.output_text


# -----------------------------
# 텍스트 질문
# -----------------------------

st.header("💬 GPT에게 질문하기")

prompt = st.text_area(
    "질문을 입력하세요",
    placeholder="예: 인공지능이 무엇인지 간단히 설명해줘."
)

if st.button(
    "질문하기",
    key="ask_button"
):
    if prompt.strip():
        try:
            with st.spinner(
                "GPT가 답변을 생성하고 있습니다..."
            ):
                result = ask_gpt(
                    prompt,
                    client
                )

            st.subheader("답변")
            st.write(result)

        except Exception as e:
            st.error(
                f"오류가 발생했습니다: {e}"
            )

    else:
        st.warning(
            "질문을 입력해주세요."
        )


# -----------------------------
# 이미지 생성
# -----------------------------

st.divider()

st.header("🎨 이미지 생성")

image_prompt = st.text_area(
    "생성할 이미지 설명",
    placeholder="예: 밤의 부산 광안대교를 배경으로 한 판타지 전사",
    key="image_prompt"
)

if st.button(
    "이미지 생성",
    key="image_button"
):
    if image_prompt.strip():
        try:
            with st.spinner(
                "이미지를 생성하고 있습니다..."
            ):
                img = client.images.generate(
                    model="gpt-image-2.6-flare",
                    prompt=image_prompt
                )

                image_bytes = base64.b64decode(
                    img.data[0].b64_json
                )

            st.image(
                image_bytes,
                caption="생성된 이미지"
            )

        except Exception as e:
            st.error(
                f"이미지 생성 중 오류가 발생했습니다: {e}"
            )

    else:
        st.warning(
            "이미지 프롬프트를 입력해주세요."
        )