import streamlit as st
import tempfile
import os

st.title("📄 ChatPDF")

st.write(
    "PDF 파일을 업로드하고 문서 내용에 대해 질문할 수 있습니다."
)

# API Client 확인
if "openai_client" not in st.session_state:
    st.warning(
        "왼쪽 사이드바에 OpenAI API Key를 입력해주세요."
    )
    st.stop()

client = st.session_state.openai_client


# Session State 초기화
if "pdf_messages" not in st.session_state:
    st.session_state.pdf_messages = []

if "pdf_vector_store_id" not in st.session_state:
    st.session_state.pdf_vector_store_id = None

if "pdf_filename" not in st.session_state:
    st.session_state.pdf_filename = None

if "pdf_uploader_version" not in st.session_state:
    st.session_state.pdf_uploader_version = 0


# Clear 버튼용
def clear_pdf_chat():
    st.session_state.pdf_messages = []


# Leave 버튼용
def leave_pdf():
    vector_store_id = st.session_state.pdf_vector_store_id

    if vector_store_id:
        try:
            client.vector_stores.delete(
                vector_store_id
            )
        except Exception:
            pass

    st.session_state.pdf_messages = []
    st.session_state.pdf_vector_store_id = None
    st.session_state.pdf_filename = None
    st.session_state.pdf_uploader_version += 1


# PDF가 아직 등록되지 않은 경우
if st.session_state.pdf_vector_store_id is None:

    uploaded_file = st.file_uploader(
        "PDF 파일을 업로드하세요",
        type=["pdf"],
        accept_multiple_files=False,
        key=f"pdf_uploader_{st.session_state.pdf_uploader_version}"
    )

    if uploaded_file is not None:

        if st.button(
            "PDF 사용하기",
            type="primary"
        ):

            try:
                with st.spinner(
                    "PDF를 분석하고 있습니다..."
                ):

                    # 임시 PDF 저장
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as temp_file:

                        temp_file.write(
                            uploaded_file.getvalue()
                        )

                        temp_path = temp_file.name


                    # Vector Store 생성
                    vector_store = (
                        client.vector_stores.create(
                            name=(
                                "Streamlit ChatPDF - "
                                + uploaded_file.name
                            )
                        )
                    )


                    # PDF를 Vector Store에 업로드
                    with open(
                        temp_path,
                        "rb"
                    ) as f:

                        file_batch = (
                            client
                            .vector_stores
                            .file_batches
                            .upload_and_poll(
                                vector_store_id=vector_store.id,
                                files=[f]
                            )
                        )


                    # 임시 파일 삭제
                    os.remove(
                        temp_path
                    )


                    if file_batch.status != "completed":
                        raise RuntimeError(
                            "PDF 처리에 실패했습니다."
                        )


                    # Session State 저장
                    st.session_state.pdf_vector_store_id = (
                        vector_store.id
                    )

                    st.session_state.pdf_filename = (
                        uploaded_file.name
                    )

                st.success(
                    "PDF 분석이 완료되었습니다."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"PDF 처리 중 오류가 발생했습니다: {e}"
                )

    st.stop()


# PDF 대화 화면
st.success(
    f"현재 PDF: {st.session_state.pdf_filename}"
)


col1, col2 = st.columns(2)


with col1:
    st.button(
        "Clear",
        on_click=clear_pdf_chat,
        use_container_width=True
    )


with col2:
    st.button(
        "Leave",
        on_click=leave_pdf,
        use_container_width=True
    )


# 이전 대화 출력
for message in st.session_state.pdf_messages:

    with st.chat_message(
        message["role"]
    ):
        st.write(
            message["content"]
        )


# 질문 입력
prompt = st.chat_input(
    "PDF 내용에 대해 질문하세요"
)


if prompt:

    st.session_state.pdf_messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)


    with st.chat_message("assistant"):

        try:
            stream = client.responses.create(
                model="gpt-6-luna",

                input=st.session_state.pdf_messages,

                tools=[
                    {
                        "type": "file_search",
                        "vector_store_ids": [
                            st.session_state.pdf_vector_store_id
                        ]
                    }
                ],

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


    st.session_state.pdf_messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )