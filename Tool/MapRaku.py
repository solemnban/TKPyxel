import streamlit as st
import folium
from folium import plugins
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

st.set_page_config(page_title="地理院マップツール", layout="wide")

st.title("🗾 地理院地図ビューア + 範囲選択ツール")

# 地名入力フォーム
keyword = st.text_input("📍 地名を検索", value="槍ヶ岳")

# 座標取得
geolocator = Nominatim(user_agent="mapapp")
location = geolocator.geocode(keyword)

if location:
    center = [location.latitude, location.longitude]
else:
    center = [36.25, 137.6]
    st.warning("地名が見つかりませんでした。デフォルト位置に移動します。")

# 地理院タイルURL
gsi_tile = "https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png"

# foliumマップ作成
m = folium.Map(location=center, zoom_start=13, tiles=None)

# 地理院タイル追加
folium.TileLayer(
    tiles=gsi_tile,
    name="地理院タイル",
    attr="地理院地図",
    overlay=False,
    control=True
).add_to(m)

# マーカー追加
folium.Marker(center, popup=keyword).add_to(m)

# Drawツール（範囲選択）
draw = plugins.Draw(
    export=True,
    draw_options={
        'rectangle': True,
        'polygon': False,
        'polyline': False,
        'circle': False,
        'circlemarker': False,
        'marker': False
    },
    edit_options={'edit': False}
)
draw.add_to(m)

# foliumマップをStreamlitに表示し、GeoJSONを取得
map_data = st_folium(m, width=1000, height=600)

# 範囲選択結果を表示（あれば）
if map_data and map_data.get("last_active_drawing"):
    st.subheader("🗂 選択範囲（GeoJSON）")
    st.json(map_data["last_active_drawing"])

