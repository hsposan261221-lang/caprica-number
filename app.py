import streamlit as st

st.set_page_config(
    page_title="카프리카 탐구 프로그램",
    page_icon="🔢",
    layout="centered"
)

st.title("🔢 카프리카 탐구 프로그램")

st.write(
"""
이 프로그램은 다양한 진법에서 카프리카 연산을 수행하여

- 귀착수(카프리카 상수)
- 순환고리(Loop)

를 탐구하기 위한 프로그램입니다.
"""
)

st.divider()

base = st.number_input(
    "진법을 입력하세요",
    min_value=2,
    max_value=36,
    value=10
)

number = st.text_input(
    "시작 숫자를 입력하세요",
    value="3524"
)

if st.button("연산 시작"):
    st.success(f"{base}진법에서 {number}의 탐구를 시작합니다.")
