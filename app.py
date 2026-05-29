import streamlit as st
import random

# 메뉴 리스트
foods = [
    "김치찌개",
    "제육볶음",
    "돈까스",
    "햄버거",
    "치킨",
    "떡볶이",
    "초밥",
    "파스타",
    "마라탕",
    "삼겹살"
]

# 제목
st.title("🍚 오늘 뭐 먹지?")

st.write("버튼을 누르면 메뉴를 추천해줘요!")

# 버튼
if st.button("추천 받기"):
    food = random.choice(foods)
    st.success(f"오늘의 추천 메뉴는 👉 {food}")
