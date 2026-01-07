import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="랜덤 발표자 추첨기", page_icon="🎤")

st.title("🎤 랜덤 발표자 추첨기")
st.markdown("명단을 입력하고 오늘 발표할 행운의 주인공을 뽑아보세요!")

# 1. 명단 입력 섹션
with st.expander("👤 명단 입력하기", expanded=True):
    names_input = st.text_area(
        "이름을 입력하세요 (줄바꿈 또는 쉼표로 구분)",
        "김철수, 이영희, 박민수, 최수지, 정국, 지민, 뷔",
        height=150
    )

# 명단 가공
name_list = [n.strip() for n in names_input.replace(',', '\n').split('\n') if n.strip()]

# 2. 추첨 설정
st.divider()
col1, col2 = st.columns([1, 1])

with col1:
    num_to_pick = st.number_input("뽑을 인원 수", min_value=1, max_value=max(1, len(name_list)), value=1)

with col2:
    st.write(f"현재 총 인원: **{len(name_list)}**명")

# 3. 추첨 버튼 및 결과
if st.button("🚀 추첨 시작!", use_container_width=True):
    if not name_list:
        st.error("명단을 입력해 주세요!")
    else:
        # 긴장감 조성을 위한 프로그레스 바/스피너
        with st.spinner('두구두구두구... 추첨 중입니다...'):
            time.sleep(2)  # 2초 대기
            winners = random.sample(name_list, num_to_pick)
        
        # 결과 발표
        st.balloons()
        st.success("🎉 당첨자를 확인하세요!")
        
        st.markdown("---")
        for i, winner in enumerate(winners):
            # 강조된 박스 형태로 당첨자 표시
            st.subheader(f"🎊 {i+1}번 당첨자: :orange[{winner}]")
        st.markdown("---")

# 하단 안내
st.caption("Tip: 이름 입력 시 엑셀에서 복사해서 붙여넣어도 잘 작동합니다.")
