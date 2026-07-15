import streamlit as st
from kaprekar import run_kaprekar

st.set_page_config(
    page_title="Kaprekar Explorer",
    page_icon="🔷",
    layout="wide"
)

st.markdown("""
<style>

.main-title{
font-size:50px;
font-weight:bold;
text-align:center;
color:#2563eb;
}

.sub-title{
text-align:center;
font-size:20px;
color:gray;
margin-bottom:40px;
}

div.stButton > button{
width:100%;
height:55px;
font-size:22px;
border-radius:15px;
background:#2563eb;
color:white;
}

.result-box{
padding:20px;
background:#f5f7fa;
border-radius:15px;
margin-top:20px;
}

</style>
""",unsafe_allow_html=True)

st.markdown(
'<div class="main-title">🔷 Kaprekar Explorer</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="sub-title">카프리카 상수 및 귀착수 탐구 시스템</div>',
unsafe_allow_html=True
)

col1,col2=st.columns(2)

with col1:

    base=st.number_input(
        "진법(Base)",
        min_value=2,
        max_value=36,
        value=10
    )

with col2:

    number=st.text_input(
        "시작 숫자",
        "3524"
    )

if st.button("🔍 탐구 시작"):

    result=run_kaprekar(base,number)

    st.markdown('<div class="result-box">',unsafe_allow_html=True)

    for step in result["steps"]:

        st.write(step)

    if result["type"]=="constant":

        st.success(f"귀착수 발견 : {result['value']}")

    else:

        st.warning("루프 발견")

    st.markdown("</div>",unsafe_allow_html=True)
