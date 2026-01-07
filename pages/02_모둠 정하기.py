import streamlit as st
import random
import time
import math

# 페이지 설정
st.set_page_config(page_title="학급 도우미: 발표 & 모둠", page_icon="🏫", layout="wide")

# 사이드바: 공통 명단 입력
st.sidebar.title("👥 명단 설정")
names_input = st.sidebar.text_area(
    "명단을 입력하세요 (줄바꿈 또는 쉼표 구분)",
    "김철수, 이영희, 박민수, 최수지, 정국, 지민, 뷔, 제니, 리사, 로제",
    height=250
)
# 명단 리스트 변환
name_list = [n.strip() for n in names_input.replace(',', '\n').split('\n') if n.strip()]
st.sidebar.info(f"현재 등록된 인원: {len(name_list)}명")

# 사이드바: 메뉴 선택
st.sidebar.divider()
menu = st.sidebar.radio("메뉴 선택", ["🎤 1. 발표자 뽑기", "🧩 2. 모둠 정하기"])

# --- 페이지 1: 발표자 뽑기 ---
if menu == "🎤 1. 발표자 뽑기":
    st.title("🎤 랜덤 발표자 뽑기")
    st.write("명단 중에서 발표자를 무작위로 추첨합니다.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        num_to_pick = st.number_input("뽑을 인원 수", min_value=1, max_value=max(1, len(name_list)), value=1)
        btn_pick = st.button("🚀 추첨 시작", use_container_width=True)

    if btn_pick:
        if not name_list:
            st.warning("명단을 먼저 입력해 주세요!")
        else:
            with st.spinner('번호표 섞는 중...'):
                time.sleep(1.5)
                winners = random.sample(name_list, num_to_pick)
            
            st.balloons()
            st.success("🎊 당첨자 명단")
            cols = st.columns(num_to_pick if num_to_pick <= 5 else 5)
            for idx, winner in enumerate(winners):
                cols[idx % 5].metric(label=f"{idx+1}번", value=winner)

# --- 페이지 2: 모둠 정하기 ---
elif menu == "🧩 2. 모둠 정하기":
    st.title("🧩 랜덤 모둠 구성하기")
    st.write("인원수에 맞춰 모둠을 자동으로 구성해 드립니다.")

    col1, col2 = st.columns([1, 1])
    with col1:
        mode = st.radio("구성 방식", ["모둠 수 지정", "모둠당 인원 수 지정"])
    
    with col2:
        if mode == "모둠 수 지정":
            group_count = st.number_input("만들 모둠 수", min_value=1, max_value=max(1, len(name_list)), value=2)
        else:
            member_count = st.number_input("한 모둠당 인원 수", min_value=1, max_value=max(1, len(name_list)), value=4)

    if st.button("🎲 모둠 구성하기", use_container_width=True):
        if not name_list:
            st.warning("명단을 먼저 입력해 주세요!")
        else:
            shuffled_names = name_list.copy()
            random.shuffle(shuffled_names)
            
            # 모둠 계산
            if mode == "모둠 수 지정":
                n = group_count
            else:
                n = math.ceil(len(shuffled_names) / member_count)
            
            # 리스트 나누기
            groups = [[] for _ in range(n)]
            for i, name in enumerate(shuffled_names):
                groups[i % n].append(name)
            
            st.markdown("---")
            st.subheader("📋 구성 결과")
            
            # 결과 출력 (Grid 형태)
            cols = st.columns(3) # 3열로 출력
            for i, group in enumerate(groups):
                with cols[i % 3]:
                    with st.container(border=True):
                        st.markdown(f"### 🚩 {i+1}모둠")
                        for member in group:
                            st.write(f"- {member}")
            st.snow()
