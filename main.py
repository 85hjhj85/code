import streamlit as st
import random
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(page_title="랜덤 자리 바꾸기", page_icon="🪑")

st.title("🪑 랜덤 자리 바꾸기 프로그램")
st.markdown("명단을 입력하고 좌석 배치를 확인하세요!")

# 사이드바 설정
st.sidebar.header("⚙️ 설정")

# 1. 명단 입력
names_input = st.sidebar.text_area(
    "참석자 명단 입력 (줄바꿈 또는 쉼표로 구분)",
    "철수, 영희, 민수, 수지, 정국, 지민, 뷔, 제니, 리사, 로제",
    height=200
)

# 명단 가공
name_list = [n.strip() for n in names_input.replace(',', '\n').split('\n') if n.strip()]

# 2. 좌석 구조 설정
st.sidebar.subheader("좌석 배치")
cols = st.sidebar.number_input("가로 좌석 수 (열)", min_value=1, value=5)
rows = st.sidebar.number_input("세로 좌석 수 (행)", min_value=1, value=2)

total_seats = rows * cols

# 실행 버튼
if st.button("🔀 자리 섞기"):
    if len(name_list) > total_seats:
        st.error(f"인원 수({len(name_list)}명)가 좌석 수({total_seats}개)보다 많습니다. 행 또는 열을 늘려주세요.")
    else:
        # 무작위 섞기
        shuffled_names = name_list.copy()
        random.shuffle(shuffled_names)
        
        # 빈자리 채우기
        empty_seats = total_seats - len(shuffled_names)
        shuffled_names.extend(["(빈자리)"] * empty_seats)
        
        # 2차원 배열로 변환
        seats_array = np.array(shuffled_names).reshape(rows, cols)
        
        # 데이터프레임 생성 (시각화용)
        df = pd.DataFrame(seats_array, columns=[f"{i+1}열" for i in range(cols)])
        df.index = [f"{i+1}행" for i in range(rows)]
        
        # 결과 출력
        st.success("🎉 배치가 완료되었습니다!")
        
        # 표 형식으로 출력
        st.table(df)
        
        # 카드 형식 시각화 (더 보기 좋게)
        st.markdown("### 🖥️ 칠판/앞쪽")
        st.divider()
        
        for r in range(rows):
            grid_cols = st.columns(cols)
            for c in range(cols):
                name = seats_array[r][c]
                if name == "(빈자리)":
                    grid_cols[c].info(name)
                else:
                    grid_cols[c].success(f"**{name}**")
        
        st.balloons()

else:
    st.info("왼쪽 사이드바에서 명단을 확인한 후 '자리 섞기' 버튼을 눌러주세요.")

# 하단 안내
st.markdown("---")
st.caption("Tip: 결과 표를 드래그해서 복사하거나 엑셀에 붙여넣을 수 있습니다.")
