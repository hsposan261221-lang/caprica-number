import streamlit as st
from kaprekar import run_kaprekar

# 페이지 기본 설정
st.set_page_config(
    page_title="Kaprekar Explorer",
    page_icon="🧮",
    layout="wide"
)

# AI 느낌의 복잡한 CSS를 빼고, 네이티브 타이틀 사용
st.title("Kaprekar Explorer")
st.caption("카프리카 상수 · 귀착수 연구 플랫폼")
st.divider()

# 사이드바 메뉴
menu = st.sidebar.radio(
    "메뉴",
    ["🔍 단일 탐구", "📊 전체 분석", "ℹ️ 연구 정보"]
)

if menu == "🔍 단일 탐구":
    col1, col2 = st.columns([1, 1])

    with col1:
        # 억지 HTML 대신 최신 Streamlit의 네이티브 컨테이너(카드 효과) 사용
        with st.container(border=True):
            st.subheader("탐구 설정")
            base = st.selectbox("진법", list(range(2, 37)), index=8)
            number = st.text_input("시작 숫자 (최대 4자리)", value="3524", max_chars=4)
            show = st.checkbox("연산 과정 자세히 보기", value=True)
            start = st.button("탐구 시작", type="primary", use_container_width=True)

    with col2:
        with st.container(border=True):
            st.subheader("현재 연구 환경")
            st.write(f"- **기준 진법:** {base}진법")
            st.write("- **지원 기능:**")
            st.write("  ✅ 2~36진법 지원\n  ✅ 귀착수(상수) 탐색\n  ✅ 루프(순환) 자동 감지")

    # 버튼을 눌렀을 때 실행
    if start:
        # 입력한 숫자가 해당 진법에 맞는지 예외 처리 (오류 방지)
        try:
            result = run_kaprekar(base, number)
            st.divider()
            st.subheader("탐구 결과")

            # 결과 상태에 따른 UI
            if result["status"] == "constant":
                st.success(f"🎉 귀착수 발견! 최종 상수: **{result['constant']}** (총 {result['count']}단계)")
            else:
                st.warning(f"🔁 루프(순환)가 발견되었습니다. (총 {result['count']}단계)")
                st.info(f"루프 구간: {' ➔ '.join(result['loop'])}")

            # 연산 과정 시각화 (Expander와 Metric 활용하여 세련되게 표현)
            if show:
                st.write("### 연산 상세 과정")
                for i, step in enumerate(result["steps"], 1):
                    with st.expander(f"Step {i} ➔ 결과: {step['result']}", expanded=True):
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("내림차순 (최댓값)", step['high'])
                        col_b.metric("오름차순 (최솟값)", step['low'])
                        col_c.metric("뺄셈 결과", step['result'])

        except ValueError as e:
            st.error(f"입력 오류: {e} (해당 진법에 맞는 숫자를 입력했는지 확인해 줘!)")

elif menu == "📊 전체 분석":
    st.info("전체 분석 기능은 아직 준비 중이야.")

elif menu == "ℹ️ 연구 정보":
    st.info("이 웹페이지는 다양한 진법에서의 카프리카 상수 규칙을 탐구하기 위해 제작되었어.")
