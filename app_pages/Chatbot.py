import streamlit as st

st.title("📚 국립부경대학교 도서관 챗봇")

st.write(
    "국립부경대학교 도서관 규정을 바탕으로 답변합니다."
)

# API Client 확인
if "openai_client" not in st.session_state:
    st.warning(
        "왼쪽 사이드바에 OpenAI API Key를 입력해주세요."
    )
    st.stop()

client = st.session_state.openai_client


# 도서관 규정
LIBRARY_RULES = """
국립부경대학교 도서관 규정

제18조(자격)
다음 각 호에 해당하는 사람은 도서관이 소장하고 있는
자료 및 시설을 이용할 수 있으며 이용 범위는 관장이 별도로 정한다.
1. 교직원 및 재학생
2. 관장의 허가를 받은 그 밖의 사람

제19조(개관 시간)
도서관의 개관 시간은 관장이 별도로 정한다.

제20조(휴관일)
도서관의 휴관일은 다음 각 호와 같다.
다만, 관장은 필요에 따라 이를 조정할 수 있다.
1. 자료실: 공휴일, 개교기념일
2. 일반열람실: 설날, 추석

제21조(자료대출)
제18조에 규정된 사람은 본인의 신분증으로 대출할 수 있다.

제22조(대출책수 및 기간)
단행본 대출 책 수 및 기간은 다음과 같다.
1. 전임교원, 겸임교원, 명예교수, 강사:
   50책 이내 90일
2. 직원, 조교, 대학원생:
   20책 이내 30일
3. 학부생:
   10책 이내 14일

전자책은 5책 이내이며 대출 기간은 5일이다.

제23조(대출 제한 자료)
다음 자료는 대출할 수 없다.
다만 관장이 필요하다고 인정할 때 단기간 대출을 허가할 수 있다.
1. 연속간행물
2. 참고자료
3. 학위논문
4. 귀중자료
5. 비도서자료
6. 관장이 지정한 그 밖의 자료

제24조(대출기간 중 반납)
휴직, 정직, 전출, 퇴직, 정학, 퇴학, 제적,
수료, 졸업 등의 사유가 발생하거나
자료 운용상 필요하여 관장이 요구하면
대출 자료를 즉시 반납하여야 한다.

졸업이나 수료 예정자는 학위수여일 30일 전부터
대출이 중지되고 대출 자료를 반납하여야 한다.

제25조(관내수칙)
이용자는 다음 행위를 해서는 안 된다.
1. 자료 또는 물품 훼손 및 무단 반출
2. 신분증 대여 또는 무단 사용
3. 지정 장소 외 식음 및 흡연
4. 지정 장소 외 게시물 부착
5. 인쇄물 및 기타 물품 배포
6. 다른 이용자에게 방해가 되는 행위

제32조(자료대출 중지)
대출한 자료를 기한 내에 반납하지 않으면
다른 자료 대출 및 도서관 이용을 중지한다.

제33조(자료의 변상)
자료를 분실 또는 훼손하면 도서관에 신고하고
신고일로부터 10일 이내 동일 자료로 변상해야 한다.
"""


# 대화 기록 초기화
if "library_messages" not in st.session_state:
    st.session_state.library_messages = []


def clear_library_chat():
    st.session_state.library_messages = []


# Clear 버튼
st.button(
    "Clear",
    on_click=clear_library_chat
)


# 이전 대화 출력
for message in st.session_state.library_messages:
    with st.chat_message(
        message["role"]
    ):
        st.write(
            message["content"]
        )


# 질문 입력
prompt = st.chat_input(
    "도서관 규정에 대해 질문하세요"
)


if prompt:

    st.session_state.library_messages.append(
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

                instructions=(
                    "당신은 국립부경대학교 도서관 규정 안내 챗봇입니다.\n"
                    "반드시 아래 규정 내용에 근거해서만 답변하세요.\n"
                    "규정에서 확인할 수 없는 내용은 "
                    "'제공된 규정에서 확인할 수 없습니다.'라고 답하세요.\n\n"
                    f"{LIBRARY_RULES}"
                ),

                input=st.session_state.library_messages,

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


    st.session_state.library_messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )