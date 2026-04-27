⚡ Smart EV Charging Assistant

🚀 [Click here to launch the Live Web App](https://8kfrqb6hehs5aglogefwkk.streamlit.app/)

A Machine Learning-powered application designed to help EV owners optimize their charging sessions by predicting energy needs, selecting the right equipment, and estimating costs.

📊 Dataset Overview
The project utilizes an EV charging dataset featuring:

Vehicle Specs: Battery capacity (kWh) and State of Charge (SOC).

Environmental Data: Temperature and time-based rate plans.

Targets: Optimal charger classification and numerical energy requirements.

🤖 Machine Learning Implementation
I developed a multi-model pipeline to handle both categorical and numerical predictions:

Random Forest Classifier: Predicts the Optimal Charger Type (Level 1, Level 2, or DC Fast Charging). It was chosen for its ability to handle non-linear relationships between battery size and charging speed.

Random Forest Regressor: Estimates the Energy Required (kWh). This model provides high stability by averaging multiple decision tree outputs to reduce variance.

Gradient Boosting (CatBoost): Used for precision-tuning the Cost and Energy estimates. Gradient boosting was particularly effective at minimizing the error rate for edge cases in the data.

📈 Results & Key Metrics
Accuracy: The Classifier handles charger selection with high precision, avoiding under-powering recommendations.

Low MAE: The Regressor achieved a low Mean Absolute Error, ensuring energy predictions stay within a reliable margin for real-world use.

Performance: Optimized for deployment, providing instant results upon input.

🛠️ Built With
Python: Pandas, NumPy, Scikit-Learn, CatBoost

Streamlit: Frontend Web Interface

GitHub: Version Control & CI/CD Deployment