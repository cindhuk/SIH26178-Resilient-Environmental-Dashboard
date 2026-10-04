import streamlit as st
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Resilient Environmental Intelligence Hub",
    page_icon="🌍",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "network_online" not in st.session_state:
    st.session_state.network_online = True

if "alerts" not in st.session_state:
    st.session_state.alerts = []

if "synced_alerts" not in st.session_state:
    st.session_state.synced_alerts = []

# ---------------- TITLE ----------------
st.title("🌍 Resilient Environmental Intelligence Hub")
st.caption(
    "SIH26178 | Edge-First Environmental Monitoring | "
    "Software Resilience Simulator"
)

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.header("🎛️ Sensor Simulation")

water_level = st.sidebar.slider(
    "Water Level (cm)", 0, 100, 30
)

rainfall = st.sidebar.slider(
    "Rainfall Intensity (mm/hr)", 0, 150, 20
)

pm25 = st.sidebar.slider(
    "PM2.5 (µg/m³)", 0, 300, 40
)

temperature = st.sidebar.slider(
    "Temperature (°C)", 15, 55, 30
)

# ---------------- RISK ENGINE ----------------
def flood_risk(water, rain):
    if water >= 80 or rain >= 100:
        return "HIGH"
    elif water >= 60 or rain >= 60:
        return "MEDIUM"
    else:
        return "LOW"


def air_risk(pm):
    if pm >= 150:
        return "HIGH"
    elif pm >= 80:
        return "MEDIUM"
    else:
        return "LOW"


flood = flood_risk(water_level, rainfall)
air = air_risk(pm25)

risk_order = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}

overall_risk = (
    "HIGH"
    if max(risk_order[flood], risk_order[air]) == 3
    else "MEDIUM"
    if max(risk_order[flood], risk_order[air]) == 2
    else "LOW"
)

# ---------------- NETWORK STATUS ----------------
st.subheader("📡 System Status")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Network",
        "ONLINE" if st.session_state.network_online else "OFFLINE"
    )

with c2:
    st.metric("Edge Intelligence", "ACTIVE")

with c3:
    st.metric("Overall Risk", overall_risk)

with c4:
    st.metric("Queued Alerts", len(st.session_state.alerts))

st.divider()

# ---------------- RESILIENCE CONTROL ----------------
st.subheader("🔄 Resilience Demonstration")

if st.session_state.network_online:
    if st.button("🔴 Simulate Network Failure", use_container_width=True):
        st.session_state.network_online = False
        st.rerun()
else:
    if st.button(
        "🟢 Restore Network & Synchronize",
        use_container_width=True
    ):
        st.session_state.network_online = True

        st.session_state.synced_alerts.extend(
            st.session_state.alerts
        )

        st.session_state.alerts = []

        st.rerun()

# ---------------- SENSOR DATA ----------------
st.subheader("🌡️ Live Environmental Readings")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Water Level", f"{water_level} cm")

with c2:
    st.metric("Rainfall", f"{rainfall} mm/hr")

with c3:
    st.metric("PM2.5", f"{pm25} µg/m³")

with c4:
    st.metric("Temperature", f"{temperature} °C")

# ---------------- RISK ANALYSIS ----------------
st.subheader("🧠 Edge Risk Analysis")

c1, c2 = st.columns(2)

with c1:
    st.write("### 🌊 Flood Risk")
    st.info(f"Risk Level: **{flood}**")

    if flood == "HIGH":
        st.error("⚠️ High flood-risk conditions detected.")
    elif flood == "MEDIUM":
        st.warning("⚠️ Moderate flood-risk conditions.")
    else:
        st.success("✅ Flood conditions currently normal.")

with c2:
    st.write("### 🌫️ Air / Smoke Risk")
    st.info(f"Risk Level: **{air}**")

    if air == "HIGH":
        st.error("⚠️ High particulate pollution detected.")
    elif air == "MEDIUM":
        st.warning("⚠️ Moderate particulate pollution.")
    else:
        st.success("✅ Air conditions currently normal.")

# ---------------- LOCAL ALERT ----------------
st.subheader("🚨 Local Alert")

if overall_risk == "HIGH":

    if st.button("🚨 Trigger High-Risk Alert", use_container_width=True):

        alert = {
            "id": len(st.session_state.alerts)
            + len(st.session_state.synced_alerts)
            + 1,
            "node": "N-01",
            "hazard": "Flood / Air",
            "risk": "HIGH",
            "time": datetime.now().strftime("%H:%M:%S"),
            "status": (
                "QUEUED"
                if not st.session_state.network_online
                else "SENT"
            )
        }

        if st.session_state.network_online:
            st.session_state.synced_alerts.append(alert)
            st.success("🚨 Alert transmitted to backend.")
        else:
            st.session_state.alerts.append(alert)
            st.warning(
                "📦 Network offline. Alert stored locally."
            )

else:
    st.success(
        "No high-risk condition detected. "
        "Local monitoring remains active."
    )

# ---------------- OFFLINE QUEUE ----------------
st.subheader("📦 Offline Alert Queue")

if st.session_state.alerts:

    for alert in st.session_state.alerts:

        st.warning(
            f"""
            **ALERT #{alert['id']}**

            Node: {alert['node']}

            Hazard: {alert['hazard']}

            Risk: {alert['risk']}

            Time: {alert['time']}

            Status: **{alert['status']}**
            """
        )

else:
    st.info("No alerts currently waiting for synchronization.")

# ---------------- SYNC HISTORY ----------------
st.subheader("☁️ Synchronized Alert History")

if st.session_state.synced_alerts:

    for alert in reversed(st.session_state.synced_alerts):

        st.success(
            f"Alert #{alert['id']} | "
            f"{alert['hazard']} | "
            f"{alert['risk']} | "
            f"{alert['time']} | SYNCHRONIZED"
        )

else:
    st.info("No synchronized alerts yet.")

# ---------------- SENSOR HEALTH ----------------
st.subheader("🔧 Node Health")

health_data = {
    "Component": [
        "Water Level Sensor",
        "Rain Sensor",
        "PM2.5 Sensor",
        "Temperature Sensor",
        "ESP32 Edge Controller",
        "Communication"
    ],
    "Status": [
        "ACTIVE",
        "ACTIVE",
        "ACTIVE",
        "ACTIVE",
        "EDGE PROCESSING",
        "ONLINE" if st.session_state.network_online else "OFFLINE"
    ]
}

st.table(health_data)

# ---------------- RESILIENCE FLOW ----------------
st.subheader("🔁 Resilience Workflow")

st.markdown(
    """
    **Normal Operation**

    Sensors → ESP32 → Data Validation → Edge Risk Analysis
    → Local Alert → Communication → Backend → Dashboard

    **During Network Failure**

    Sensors → ESP32 → Edge Risk Analysis
    → Local Alert → Critical Alert Stored Locally

    **After Network Recovery**

    Network Restored → Stored Alerts → Backend
    → Dashboard Synchronization
    """
)

# ---------------- IMPORTANT NOTE ----------------
st.divider()

st.caption(
    "Prototype note: This software prototype uses transparent "
    "demonstration risk logic to simulate the edge decision workflow. "
    "It is not a trained or validated ML model. The intended hardware "
    "implementation can replace this demonstration logic with a "
    "lightweight trained Edge-AI model."
)
