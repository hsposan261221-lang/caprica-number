import streamlit as st
from kaprekar import run_kaprekar

st.set_page_config(
    page_title="Kaprekar Explorer",
    page_icon="🧮",
    layout="wide"
)

st.markdown("""
<style>

html, body, [class*="css"]{
    font-family: "Segoe UI", sans-serif;
}

.main-title{
    text-align:center;
    font-size:54px;
    font-weight:800;
    color:#2563EB;
    margin-bottom:0;
}

.sub-title{
    text-align:center;
    color:#666;
    font-size:20px;
    margin-bottom:35px;
}

.card{
    background:white;
    border-radius:18px;
    padding:28px;
    box-shadow:0 8px 25px rgba(0,0,0,.08);
    border:1px solid #e5e7eb;
}

.result{
    background:#f8fafc;
    border-radius:15px;
    padding:18px;
    margin-top:15px;
    border-left:6px solid #2563EB;
}

.step{
    font-size:22px;
    font-weight:700;
}

.big{
    font-size:30px;
    font-weight:bold;
    text-align:center;
}

div.stButton>button{
    width:100%;
    height:55px;
    font-size:20px;
    border-radius:12px;
    background:#2563EB;
    color:white;
    border:none;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
"""
<div class="main-title">
Kaprekar Explorer
</div>

<div class="sub-title">
카프리카 상수 · 귀착수 연구 플랫폼
</div>
""",
unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "메뉴",
    [
        "🔍 단일 탐구",
        "📊 전체 분석",
        "ℹ 연구 정보"
    ]
)

if menu == "🔍 단일 탐구":

    col1,col2=st.columns([1,1])

    with col1:

        st.markdown("<div class='card'>",unsafe_allow_html=True)

        base=st.selectbox(
            "진법",
            list(range(2,37)),
            index=8
        )

        number=st.text_input(
            "시작 숫자",
            value="3524"
        )

        show=st.checkbox(
            "연산 과정 보기",
            value=True
        )

        start=st.button("🔎 탐구 시작")

        st.markdown("</div>",unsafe_allow_html=True)

    with col2:

        st.markdown("<div class='card'>",unsafe_allow_html=True)

        st.markdown("### 연구 정보")

        st.write(f"**현재 진법 :** {base}")

        st.write("지원 기능")

        st.write("✅ 2~36진법")

        st.write("✅ 귀착수 탐색")

        st.write("✅ 루프 탐색")

        st.write("✅ 반복 횟수 계산")

        st.markdown("</div>",unsafe_allow_html=True)

    if start:

        result=run_kaprekar(base,number)

        st.divider()

        st.subheader("탐구 결과")

        if show:

            for i,step in enumerate(result["steps"],1):

                st.markdown(f"""
<div class="result">

### STEP {i}

<div class="step">

{step['high']} − {step['low']}

↓

{step['result']}

</div>

</div>
""",unsafe_allow_html=True)

        if result["status"]=="constant":

            st.success(f"🎉 귀착수 발견 : {result['constant']}")

        else:

            st.warning("🔁 루프가 발견되었습니다.")
