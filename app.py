import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import date
from minwon import Minwon
from sheets_util import append_minwon_to_sheet, get_all_minwons

st.set_page_config(page_title="민원 신고 플랫폼", layout="wide")
st.title("📌 동네 민원 신고 플랫폼")

st.markdown("지도에서 위치를 선택하고, 작성자와 내용을 입력하여 민원을 등록하세요.")

# 민원 입력 영역
st.subheader("✍️ 민원 작성")

author = st.text_input("작성자 이름")
content = st.text_area("민원 내용")
created_date = st.date_input("작성 날짜", value=date.today())

lat = st.number_input("위도 입력", format="%.6f")
lon = st.number_input("경도 입력", format="%.6f")

if st.button("민원 제출"):
    if author and content and lat and lon:
        minwon = Minwon(author, content, lat, lon, created_date)
        append_minwon_to_sheet(minwon)
        st.success("민원이 등록되었습니다!")
        st.code(str(minwon), language='text')
    else:
        st.warning("모든 값을 입력해주세요.")

# 민원 목록 불러오기
st.subheader("📋 등록된 민원")
data = get_all_minwons()
if not data:
    st.info("아직 등록된 민원이 없습니다.")
else:
    df = pd.DataFrame(data)

    # 지도 위에 민원 표시
    st.subheader("🗺️ 민원 지도")
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v12",
        initial_view_state=pdk.ViewState(latitude=37.5665, longitude=126.9780, zoom=10),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position='[longitude, latitude]',
                get_radius=150,
                get_color='[255, 0, 0, 160]',
                pickable=True,
            ),
        ],
    ))

    # 작성자별 민원 검색
    st.subheader("🔎 작성자별 민원 조회")
    search_name = st.text_input("작성자 이름 입력")
    if st.button("조회"):
        if search_name:
            result = df[df['author'] == search_name]
            st.dataframe(result)
        else:
            st.warning("작성자 이름을 입력하세요.")

    # 날짜별 민원 수 통계
    st.subheader("📊 날짜별 민원 건수")
    df["created_date"] = pd.to_datetime(df["created_date"])
    count_by_date = df.groupby(df["created_date"].dt.date).size()
    st.bar_chart(count_by_date)

    st.subheader("📄 전체 민원 데이터")
    st.dataframe(df)
