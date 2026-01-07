import streamlit as st
import random
import math

# 페이지 설정
st.set_page_config(page_title="랜덤 모둠 구성기", page_icon="🧩")

st.title("🧩 랜덤 모둠 구성기")
st.markdown("인원수와 명단에 맞춰 최적의 모둠을 자동으로 구성합니다.")

# 1. 명단 입력 섹션
with st.expander("👤 명단 입력 및 확인", expanded=True):
    names_input = st.text_area(
        "이름을 입력하세요 (줄바꿈 또는 쉼표로 구분)",
        "김철수, 이영희, 박민수, 최수지, 정국, 지민, 뷔, 제니, 리사, 로제",
        height=150
    )
    # 명단 가공
    name_list = [n.strip() for n in names_input.replace(',', '\n').split('\n') if n.strip()]
    st.info(f"현재 총 인원: {len(name_list)}명")

st.divider()

# 2. 모둠 설정 섹션
col1, col2 = st.columns(2)

with col1:
    method = st.radio("🏠 구성 방식 선택", ["모둠 수 기준", "모둠당 인원 기준"])

with col2:
    if method == "모둠 수 기준":
        target_val = st.number_input("만들고 싶은 모둠 수", min_value=1, max_value=max(1, len(name_list)), value=2)
    else:
        target_val = st.number_input("한 모둠당 적정 인원", min_value=1, max_value=max(1, len(name_list)), value=4)

# 3. 실행 버튼 및 로직
if st.button("🎲 모둠 만들기", use_container_width=True):
    if not name_list:
        st.error("명단을 입력해 주세요!")
    else:
        # 무작위 섞기
        shuffled_names = name_list.copy()
        random.shuffle(shuffled_names)
        
        # 모둠 개수 계산
        if method == "모둠 수 기준":
            num_groups = target_val
        else:
            num_groups = math.ceil(len(shuffled_names) / target_val)
            
        # 빈 리스트 생성 후 배분
        groups = [[] for _ in range(num_groups)]
        for i, name in enumerate(shuffled_names):
            groups[i % num_groups].append(name)
            
        # 결과 화면 출력
        st.success(f"🎉 총 {num_groups}개의 모둠이 구성되었습니다!")
        st.snow()
        
        st.markdown("---")
        # 결과를 3열 그리드로 표시
        cols = st.columns(3)
        for idx, group in enumerate(groups):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.subheader(f"🚩 {idx + 1}모둠")
                    for member in group:
                        st.write(f"- {member}")
        
        # 텍스트로 복사하기 기능
        st.divider()
        result_text = ""
        for idx, group in enumerate(groups):
            result_text += f"{idx+1}모둠: {', '.join(group)}\n"
        st.text_area("결과 텍스트 복사하기", value=result_text, height=100)
