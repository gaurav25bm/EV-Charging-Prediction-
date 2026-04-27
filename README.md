# ⚡ Smart EV Charging Assistant

> **Status:** Live and Operational 🟢  
> **[🚀 Click here to launch the Live Web App](https://8kfrqb6hehs5aglogefwkk.streamlit.app/)**

---

### 📊 Project Overview
This is a **Machine Learning-powered application** designed to help EV owners optimize their charging sessions. By analyzing vehicle and environmental data, the app predicts energy needs and suggests the most efficient equipment.

---

### 🤖 Machine Learning Implementation
I developed a robust multi-model pipeline to ensure high-accuracy results:

* **Random Forest Classifier:** Predicts the **Optimal Charger Type** (Level 1, Level 2, or DC Fast Charging). It was selected for its ability to handle non-linear relationships.
* **Random Forest Regressor:** Estimates the **Energy Required (kWh)**. This ensemble method provides stability by averaging multiple decision trees.
* **Gradient Boosting (CatBoost):** Used for precision-tuning. It minimizes the error rate for complex energy and cost estimations.

---

### 📊 Dataset Details
The models were trained on a specialized EV dataset including:
1. **Vehicle Specs:** Battery capacity and State of Charge (SOC).
2. **Environment:** Outside temperature and daily rate plans.
3. **Targets:** Optimal hardware selection and numerical energy requirements.

---

### 📈 Results & Performance
* **Classification:** High precision in charger selection (no under-powering).
* **Regression:** Low **Mean Absolute Error (MAE)**, ensuring reliable energy estimates.
* **Inference:** Optimized to provide results in **under 1 second**.

---

### 🛠️ Built With
* **Python** (Pandas, NumPy, Scikit-Learn, CatBoost)
* **Streamlit** (UI/UX)
* **GitHub** (Version Control & CI/CD)