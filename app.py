import streamlit as st
from kaprekar import run_kaprekar, DIGITS
from itertools import combinations_with_replacement

st.set_page_config(page_title="Kaprekar Explorer", page_icon="🧮", layout="wide")

st.title("Kaprekar Explorer")
st.caption("카프리카 상수 · 귀착수 연구 플랫폼 (최대 60진법 및 음수 진법 지원)")
st.divider()

menu = st.sidebar.radio("메뉴", ["🔍 단일 탐구", "📊 전체 분석", "ℹ️ 연구 정보"])

# 양수, 음수 진법 목록 (-60 ~ -2, 2 ~ 60)
base_options = list(range(-60, -1)) + list(range(2, 61))

if menu == "🔍 단일 탐구":
    col1, col2 = st.columns([1, 1])

    with col1:
        with st.container(border=True):
            st.subheader("탐구 설정")
            base = st.selectbox("진법 선택", base_options, index=base_options.index(10))
            number = st.text_input("시작 숫자 (최대 4자리)", value="3524", max_chars=4)
            show = st.checkbox("연산 과정 자세히 보기", value=True)
            start = st.button("탐구 시작", type="primary", use_container_width=True)

    with col2:
        with st.container(border=True):
            st.subheader("현재 연구 환경")
            st.write(f"- **기준 진법:** {base}진법")
            st.write("- **사용 기호:** 0~9, A~Z, a~x (60진법)")
            st.write("- **지원 기능:** 음수 진법 지원, 루프/상수 완벽 추적")

    if start:
        try:
            result = run_kaprekar(base, number)
            st.divider()
            st.subheader("탐구 결과")

            if result["status"] == "constant":
                st.success(f"🎉 귀착수 발견! 최종 상수: **{result['constant']}** (총 {result['count']}단계)")
            else:
                st.warning(f"🔁 루프(순환)가 발견되었습니다. (총 {result['count']}단계)")
                st.info(f"루프 구간: {' ➔ '.join(result['loop'])}")

            if show:
                st.write("### 연산 상세 과정")
                for i, step in enumerate(result["steps"], 1):
                    with st.expander(f"Step {i} ➔ 결과: {step['result']}", expanded=True):
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("내림차순 (High)", step['high'])
                        col_b.metric("오름차순 (Low)", step['low'])
                        col_c.metric("뺄셈 결과", step['result'])
        except ValueError as e:
            st.error(f"입력 오류: {e} (선택한 진법에 맞는 숫자인지 확인해 줘!)")

elif menu == "📊 전체 분석":
    st.header("📊 진법별 생태계 전체 분석")
    st.write("선택한 진법에 존재하는 **모든 4자리 숫자 조합**을 테스트하여, 어떤 상수와 루프가 숨어있는지 통계를 냅니다.")

    analyze_base = st.selectbox("분석할 진법 선택", base_options, index=base_options.index(10))
    
    if st.button("전체 분석 실행", type="primary"):
        with st.spinner(f"{analyze_base}진법의 모든 경우의 수를 분석 중..."):
            abs_base = abs(analyze_base)
            valid_digits = DIGITS[:abs_base]
            
            constants = set()
            loops = []
            
            # 모든 자릿수의 중복조합(combinations) 생성 -> 연산 속도 최적화
            all_combos = list(combinations_with_replacement(valid_digits, 4))
            
            progress_bar = st.progress(0)
            total = len(all_combos)
            
            for i, combo in enumerate(all_combos):
                if len(set(combo)) == 1:  # 1111처럼 모든 숫자가 같은 경우는 스킵
                    continue
                    
                num_str = "".join(combo)
                res = run_kaprekar(analyze_base, num_str)
                
                if res["status"] == "constant":
                    constants.add(res["constant"])
                elif res["status"] == "loop":
                    # 루프 중복 방지 로직 (시작점이 달라도 같은 루프면 필터링)
                    canonical_loop = tuple(sorted(res["loop"]))
                    if canonical_loop not in [tuple(sorted(l)) for l in loops]:
                        loops.append(res["loop"])
                        
                # 프로그레스 바 업데이트
                if i % 100 == 0:
                    progress_bar.progress(min(i / total, 1.0))
            
            progress_bar.progress(1.0)
            
            st.success(f"분석 완료! 총 {total}개의 고유한 숫자 조합을 모두 탐색했어.")
            
            col1, col2 = st.columns(2)
            with col1:
                with st.container(border=True):
                    st.subheader("🎯 발견된 상수")
                    if constants:
                        for c in constants:
                            st.write(f"- **{c}**")
                    else:
                        st.write("이 진법에는 카프리카 상수가 존재하지 않아!")
            with col2:
                with st.container(border=True):
                    st.subheader("🔁 발견된 루프")
                    if loops:
                        for l in loops:
                            st.write(f"- {' ➔ '.join(l)}")
                    else:
                        st.write("발견된 루프가 없어.")

elif menu == "ℹ️ 연구 정보":
    st.info("이 플랫폼은 최대 60진법 및 음수 진법(-60 ~ -2)에서의 카프리카 상수 규칙을 탐구하기 위해 제작되었어.")
    st.write("**[숫자 입력 가이드]**")
    st.write("10진법 이상의 진법에서는 알파벳을 사용해!\n- `A=10, B=11 ... Z=35`\n- `a=36, b=37 ... x=59`")
