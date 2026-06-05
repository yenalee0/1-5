import streamlit as st
from google import genai

st.set_page_config(
    page_title="반 냄새 상담 챗봇",
    page_icon="💬",
)

st.title("💬 반 냄새 상담 챗봇")
st.caption("반에서 나는 냄새 문제에 대해 이야기해 보세요.")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error(
        "GEMINI_API_KEY가 설정되지 않았습니다. "
        "Streamlit Secrets를 확인하세요."
    )
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# 시스템 프롬프트
SYSTEM_PROMPT = """
너는 '반 냄새 상담 챗봇'이다.

역할:
- 학교 교실에서 발생하는 냄새 문제를 상담한다.
- 학생들이 서로를 놀리거나 공격하지 않도록 돕는다.
- 위생, 환기, 청소, 생활 습관에 대한 건설적인 조언을 제공한다.
- 특정 학생을 비난하거나 괴롭히는 방향으로 답하지 않는다.
- 친절하고 이해하기 쉬운 한국어로 답한다.
"""

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 반에서 나는 냄새 문제에 대해 이야기해 보세요."
        }
    ]

# 기존 메시지 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
user_input = st.chat_input("메시지를 입력하세요")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # 대화 기록 구성
        conversation_text = SYSTEM_PROMPT + "\n\n"

        for msg in st.session_state.messages:
            role = msg["role"]
            content = msg["content"]

            if role == "user":
                conversation_text += f"사용자: {content}\n"
            elif role == "assistant":
                conversation_text += f"챗봇: {content}\n"

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=conversation_text
        )

        answer = response.text

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        error_msg = f"오류가 발생했습니다: {e}"

        with st.chat_message("assistant"):
            st.error(error_msg)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_msg
            }
        )
