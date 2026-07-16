import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="주차장 정보", layout="wide")

st.title("🚗 주차장 정보 검색")

uploaded_file = st.file_uploader(
    "주차장 CSV 업로드", type="csv"
)

if uploaded_file:

    df = pd.read_csv(uploaded_file, encoding="cp949")

    st.success("데이터 업로드 완료!")

    # --------------------
    # 사이드바
    # --------------------

    gu = st.sidebar.selectbox(
        "자치구 선택",
        sorted(df["자치구"].unique())
    )

    parking_type = st.sidebar.selectbox(
        "주차장 종류",
        ["전체"] + sorted(df["주차장종류"].unique().tolist())
    )

    free_type = st.sidebar.selectbox(
        "무료 / 유료",
        ["전체", "무료", "유료"]
    )

    hour = st.sidebar.number_input(
        "예상 주차시간(시간)",
        min_value=1,
        max_value=24,
        value=1
    )

    result = df[df["자치구"] == gu]

    if parking_type != "전체":
        result = result[result["주차장종류"] == parking_type]

    if free_type != "전체":
        result = result[result["무료여부"] == free_type]

    result = result.copy()

    result["예상요금"] = result["주차요금(시간당)"] * hour

    st.subheader("주차장 목록")

    st.dataframe(
        result[
            [
                "주차장명",
                "자치구",
                "주차요금(시간당)",
                "무료여부",
                "주차장종류",
                "예상요금",
            ]
        ],
        use_container_width=True,
    )

    if len(result) > 0:

        cheapest = result.loc[
            result["예상요금"].idxmin()
        ]

        st.success(
            f"""
가장 저렴한 주차장

📍 {cheapest['주차장명']}

예상요금 : {cheapest['예상요금']:,}원
"""
        )

        st.subheader("주차장 위치")

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=result,
            get_position='[경도, 위도]',
            get_radius=50,
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=result["위도"].mean(),
            longitude=result["경도"].mean(),
            zoom=12,
        )

        st.pydeck_chart(
            pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={
                    "text": """
주차장명 : {주차장명}

시간당요금 : {주차요금(시간당)}원

무료여부 : {무료여부}
"""
                },
            )
        )

    else:
        st.warning("조건에 맞는 주차장이 없습니다.")
