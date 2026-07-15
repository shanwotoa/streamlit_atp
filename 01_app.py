import streamlit as st
import requests

st.set_page_config(
    page_title="오늘 뭐 먹지?",
    page_icon="🍽️",
    layout="centered"
)

API_KEY = st.secrets["OPENWEATHER_API_KEY"]

# 음식 데이터
foods = {
    "cold": {
        "name": "김치찌개",
        "image": "https://images.unsplash.com/photo-1604908176997-4313d1d6d7af",
        "calorie": "420 kcal",
        "carb": "28 g",
        "protein": "25 g",
        "fat": "20 g",
        "reason": "추운 날에는 따뜻한 국물이 최고!"
    },
    "hot": {
        "name": "냉면",
        "image": "https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56",
        "calorie": "510 kcal",
        "carb": "83 g",
        "protein": "18 g",
        "fat": "11 g",
        "reason": "더운 날 시원하게 즐기기 좋아요."
    },
    "rain": {
        "name": "파전",
        "image": "https://images.unsplash.com/photo-1627308595171-d1b5d67129c4",
        "calorie": "610 kcal",
        "carb": "50 g",
        "protein": "15 g",
        "fat": "38 g",
        "reason": "비 오는 날 생각나는 대표 음식!"
    },
    "normal": {
        "name": "비빔밥",
        "image": "https://images.unsplash.com/photo-1590301157890-4810ed352733",
        "calorie": "560 kcal",
        "carb": "68 g",
        "protein": "21 g",
        "fat": "18 g",
        "reason": "균형 잡힌 영양을 섭취할 수 있어요."
    }
}

st.title("🍽️ 오늘 날씨에 맞는 음식 추천")

city = st.text_input("도시를 입력하세요", "Seoul")

if st.button("추천받기"):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
        st.error("도시를 찾을 수 없습니다.")
        st.stop()

    data = response.json()

    temp = data["main"]["temp"]
    weather = data["weather"][0]["main"]

    st.subheader(f"📍 {city}")
    st.write(f"현재 기온 : **{temp:.1f}℃**")
    st.write(f"날씨 : **{weather}**")

    if weather in ["Rain", "Drizzle", "Thunderstorm"]:
        food = foods["rain"]

    elif temp >= 28:
        food = foods["hot"]

    elif temp <= 10:
        food = foods["cold"]

    else:
        food = foods["normal"]

    st.divider()

    st.header(f"🍴 추천 음식 : {food['name']}")

    st.image(food["image"], use_container_width=True)

    st.success(food["reason"])

    col1, col2 = st.columns(2)

    with col1:
        st.metric("칼로리", food["calorie"])
        st.metric("탄수화물", food["carb"])

    with col2:
        st.metric("단백질", food["protein"])
        st.metric("지방", food["fat"])
