import streamlit as st
import folium
from streamlit_folium import st_folium
import random
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
from deep_translator import GoogleTranslator
# =========================================================
# ⚙️ PAGE CONFIG
# =========================================================
st.set_page_config(page_title="IndiSafe 🛡️", layout="wide")

# =========================================================
# 🔐 SESSION STATE
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "tourist_id" not in st.session_state:
    st.session_state.tourist_id = "IND-" + str(random.randint(1000, 9999))


# =========================================================
# 🔐 LOGIN / SIGNUP PAGE (ONLY THIS SHOWS FIRST)
# =========================================================
if not st.session_state.logged_in:

    st.markdown(
        "<h1 style='text-align:center;'>🛡️ IndiSafe</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center;'>AI Tourist Guardian System</p>",
        unsafe_allow_html=True
    )

    option = st.radio("Select Option", ["Login", "Sign Up"], horizontal=True)

    name = st.text_input("👤 Full Name")
    email = st.text_input("📧 Email")
    password = st.text_input("🔒 Password", type="password")

    if option == "Sign Up":
        country = st.text_input("🌍 Country")
        phone = st.text_input("📱 Phone Number")

        if st.button("🚀 Create Account"):
            if name and email and password:
                st.success("Account created successfully!")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Please fill all fields")

    else:
        if st.button("🔓 Login"):
            if email and password:
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Enter email & password")

    # 🚫 STOP HERE — DO NOT SHOW DASHBOARD
    st.stop()


st.set_page_config(page_title="IndiSafe CHAMPION", layout="wide")

# =============================
# 🔒 SESSION STATE
# =============================

if "tourist_id" not in st.session_state:
    st.session_state.tourist_id = "IND-" + str(random.randint(10000, 99999))

if "last_location" not in st.session_state:
    st.session_state.last_location = None

if "map_center" not in st.session_state:
    st.session_state.map_center = [26.9124, 75.7873]

if "map_zoom" not in st.session_state:
    st.session_state.map_zoom = 14

# =============================
# 🎨 HEADER
# =============================

st.markdown("""
<h1 style='text-align:center;'>🛡️ IndiSafe — Predictive Tourist Guardian</h1>
<p style='text-align:center;'>Powered by <b>IndiAI</b></p>
""", unsafe_allow_html=True)

# =============================
# 👥 TEAM
# =============================

st.sidebar.markdown("### 👥 Team Prefer_Not_To_Say")
st.sidebar.markdown("""
Team Lead and Full-Stack Developer-(AXAR TANDON)

Buisness Strategist and Pitch deck lead -(HIMANSHU BHARDWAJ)

Research Operations and Data Analyst- (SAMEER AKHTAR)

Product Concept and Creative Designer- (AKSHITA SINGH)
""")

# =============================
# 🌍 LANGUAGE
# =============================

languages = {
    "English":"en","Hindi":"hi","Spanish":"es",
    "French":"fr","German":"de","Arabic":"ar"
}

lang = st.sidebar.selectbox("🌍 Language", list(languages.keys()))
lang_code = languages[lang]

def T(text):
    if lang_code == "en":
        return text
    try:
        return GoogleTranslator(source='auto', target=lang_code).translate(text)
    except:
        return text

# =============================
# 👤 PROFILE
# =============================

st.sidebar.header("👤 Tourist Profile")

name = st.sidebar.text_input("Name", "John Doe")
st.sidebar.success(f"Digital ID: {st.session_state.tourist_id}")

night = st.sidebar.toggle("🌙 Night Travel")
offline = st.sidebar.toggle("📡 Offline Mode")
isolated = st.sidebar.toggle("🏞️ Isolated Area", value=True)

# =============================
# 📍 LOCATION
# =============================

lat = st.sidebar.slider("Latitude", 26.90, 26.95, 26.9124)
lon = st.sidebar.slider("Longitude", 75.77, 75.82, 75.7873)

# =============================
# 🏥 SERVICES
# =============================

services = {
    "Police Station": (26.918, 75.785),
    "Hospital": (26.922, 75.795)
}

def distance(lat1, lon1, lat2, lon2):
    r = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return r * 2 * asin(sqrt(a))

st.sidebar.subheader("🚓 Nearby Services")
for place, coord in services.items():
    d = distance(lat, lon, coord[0], coord[1])
    st.sidebar.write(f"{place}: {d:.2f} km")

# =============================
# 🗺️ STABLE MAP (NO REFRESH)
# =============================

st.session_state.map_center = [lat, lon]

m = folium.Map(
    location=st.session_state.map_center,
    zoom_start=st.session_state.map_zoom
)

# Tourist marker
folium.Marker(
    [lat, lon],
    tooltip=name,
    icon=folium.Icon(color="blue")
).add_to(m)

# 👥 Simulated tourists (fixed positions)
simulated_positions = [
    (26.915, 75.79),
    (26.905, 75.78),
    (26.92, 75.80),
    (26.91, 75.775),
    (26.93, 75.79)
]

for i, pos in enumerate(simulated_positions):
    folium.Marker(
        pos,
        icon=folium.Icon(color="green"),
        tooltip=f"Tourist {i+1}"
    ).add_to(m)

# 🔥 Risk zone
risk_zone = [[26.915, 75.78], [26.92, 75.79], [26.91, 75.80]]
folium.Polygon(
    risk_zone,
    color="red",
    fill=True,
    fill_opacity=0.3,
    tooltip="Crime Zone"
).add_to(m)

# Services markers
for k, v in services.items():
    folium.Marker(
        v,
        tooltip=k,
        icon=folium.Icon(color="darkblue")
    ).add_to(m)

st.subheader("📍 Live Tracking")

st_folium(
    m,
    width=900,
    height=500,
    returned_objects=[]
)

# =============================
# 🧠 RISK ENGINE
# =============================

risk = 10

if 26.91 < lat < 26.92 and 75.78 < lon < 75.80:
    risk += 40

if night:
    risk += 20

if isolated:
    risk += 20

if offline:
    risk += 15

# Movement anomaly
if st.session_state.last_location:
    prev_lat, prev_lon = st.session_state.last_location
    if abs(lat - prev_lat) > 0.02 or abs(lon - prev_lon) > 0.02:
        risk += 10
        st.warning(T("⚠️ Unusual movement detected"))

st.session_state.last_location = (lat, lon)

risk = min(risk, 100)

# =============================
# 🚦 STATUS
# =============================

if risk > 80:
    status = "🔴 EMERGENCY"
    st.error(T(f"{status} — Risk {risk}"))
elif risk > 50:
    status = "🟡 ALERT"
    st.warning(T(f"{status} — Risk {risk}"))
else:
    status = "🟢 SAFE"
    st.success(T(f"{status} — Risk {risk}"))

if risk > 60:
    st.warning(T("⚠️ Danger Ahead on your route"))

# =============================
# 📞 FAKE CALL
# =============================

if st.button("📞 Generate Fake Call"):
    st.info(T("Incoming call: Police Control Room"))

# =============================
# 👨‍👩‍👧 COMPANION MODE
# =============================

if st.checkbox("👨‍👩‍👧 Share location with family"):
    st.success(T("Live location shared"))

# =============================
# 🆘 SOS
# =============================

if st.button("🚨 ACTIVATE SOS"):
    st.error(T("Emergency Alert Sent"))
    st.write("📍 Location shared")
    st.write("📞 Calling 112")

# =============================
# 🖥️ AUTHORITY DASHBOARD
# =============================

st.subheader("🖥️ Authority Command Center")

st.table({
    "Tourist": [name],
    "ID": [st.session_state.tourist_id],
    "Status": [status],
    "Risk": [risk],
    "Location": [f"{lat:.4f}, {lon:.4f}"],
    "Time": [datetime.now().strftime("%H:%M:%S")]
})

# =============================
# 🤖 IndiAI ASSISTANT
# =============================

st.subheader("🤖 IndiAI Assistant")

q = st.text_input("Ask about safety or locality")

def indiAI(q):
    q = q.lower()
    if "safe" in q:
        return "Area is generally safe during daytime."
    elif "hotel" in q:
        return "Stay in central tourist areas."
    elif "police" in q:
        return "Police station nearby."
    elif "transport" in q:
        return "Use verified taxis."
    elif "emergency" in q:
        return "Dial 112."
    else:
        return "Stay alert and avoid isolated places."

if q:
    st.info(T(indiAI(q)))

# =============================
# FOOTER
# =============================

st.markdown("""
<hr>
<center>IndiSafe Guardian Active • Team Prefer_Not_To_Say</center>
""", unsafe_allow_html=True)
