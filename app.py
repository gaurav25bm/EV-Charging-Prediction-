import streamlit as st
import pandas as pd
import numpy as np
import pickle

# --- 1. CONFIG & UI ---
st.set_page_config(page_title="EV Prediction Hub", layout="wide")

# Visual styling for a clean, professional dashboard
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #28a745;
    }
    h1 { color: #1e7e34; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource 
def load_assets():
    # Loading your local .pkl files from the 'models' folder
    with open('models/charger_clf_model.pkl', 'rb') as f:
        charger_model = pickle.load(f)
    with open('models/energy_reg_model.pkl', 'rb') as f:
        energy_model = pickle.load(f)
    with open('models/label_encoder.pkl', 'rb') as f:
        le = pickle.load(f)
    with open('models/feature_columns.pkl', 'rb') as f:
        feature_cols = pickle.load(f)
    return charger_model, energy_model, le, feature_cols

try:
    assets = load_assets()
    charger_model, energy_model, le, feature_cols = assets
except Exception as e:
    st.error(f"Error loading local models: {e}")
    st.stop()

# --- 2. UI INPUTS ---
st.title("⚡ Smart EV Charging Assistant")
st.write("Predict optimal charging and energy requirements using your custom ML models.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🔋 Vehicle Parameters")
    capacity = st.number_input("Battery Capacity (kWh)", 10.0, 250.0, 60.0, step=5.0)
    soc_start = st.slider("Current Charge (%)", 0, 100, 20)
    target_soc = st.slider("Target Charge (%)", soc_start + 1, 100, 80)
    temp = st.slider("Outside Temperature (°C)", -10, 50, 25)

with col2:
    st.subheader("⏰ Session Context")
    start_hour = st.slider("Start Hour (0-23)", 0, 23, 18)
    day_choice = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    utility_rate = st.selectbox("Rate Plan", ["Standard ($0.15/kWh)", "Peak ($0.30/kWh)", "Off-Peak ($0.08/kWh)"])

# --- 3. PREDICTION LOGIC ---
if st.button("Analyze Charging Session"):
    # Prepare ML Input Data
    input_df = pd.DataFrame([{'Battery Capacity (kWh)': capacity, 'State of Charge (Start %)': soc_start, 
                             'Temperature (°C)': temp, 'Charging Start Hour': start_hour}])
    
    # Handle One-Hot Encoding for the Day of Week
    for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        input_df[f"Day of Week_{d}"] = 1 if day_choice == d else 0
    
    # Align features with training columns and fill missing with 0
    final_input = pd.DataFrame(columns=feature_cols).fillna(0)
    final_input = pd.concat([final_input, input_df], axis=0).fillna(0)[feature_cols]

    # Run Predictions using your Pickle models
    type_idx = charger_model.predict(final_input)[0]
    recommended_type = le.inverse_transform([type_idx])[0]
    
    ml_energy = energy_model.predict(final_input)[0]
    theoretical_max = capacity * ((target_soc - soc_start) / 100)
    
    # Hybrid Energy Logic
    energy_pred = (theoretical_max * 0.7 + ml_energy * 0.3) if abs(ml_energy - theoretical_max) > 15 else ml_energy
    energy_pred = np.clip(energy_pred, 0.1, theoretical_max)
    
    # Calculate Cost based on selected rate plan
    rate_val = 0.30 if "Peak" in utility_rate else (0.08 if "Off-Peak" in utility_rate else 0.15)
    cost = energy_pred * rate_val

    # --- 4. DISPLAY RESULTS ---
    st.divider()
    res1, res2 = st.columns(2)
    with res1:
        st.metric("Optimal Charger", recommended_type)
        st.metric("Energy Required", f"{energy_pred:.2f} kWh")
    with res2:
        st.metric("Estimated Cost", f"${cost:.2f}")

    # Replacing failing AI with stable, static expert advice
    static_tip = "For optimal battery longevity, keep the state of charge between 20% and 80%. Charging beyond 80% is slower and generates more heat."
    st.info(f"💡 **Expert Advice:** {static_tip}")

    # --- 5. DOWNLOAD REPORT ---
    report_text = f"""EV CHARGING REPORT
    ------------------
    Battery Capacity: {capacity} kWh
    Current Charge: {soc_start}%
    Target Charge: {target_soc}%
    Outside Temperature: {temp}°C
    
    RECOMMENDATIONS:
    Optimal Charger: {recommended_type}
    Energy Required: {energy_pred:.2f} kWh
    Estimated Session Cost: ${cost:.2f}

    Note: {static_tip}
    """
    
    st.download_button(
        label="📩 Download Session Report",
        data=report_text,
        file_name="EV_Charging_Report.txt",
        mime="text/plain"
    )