import streamlit as st
import joblib
import numpy as np

@st.cache_resource
def load_artifacts(model_name):
    return {
        "model": joblib.load(model_name),
        "scaler": joblib.load("scaler.pkl"),
        "label_encoders": joblib.load("label_encoders.pkl")
    }

def main():
    st.title("📡 Machine Learning-Based Detection and Mitigation of Attacks on Software Defined Networking (SDN) Controllers")

    artifacts = load_artifacts("RandomForest_best_model.pkl")

    st.subheader("Enter Network Packet Features:")

    src_mac = st.text_input("Source MAC Address", "00:1B:44:11:3A:B7")
    dst_mac = st.text_input("Destination MAC Address", "00:1B:44:11:3A:C8")
    src_ip = st.text_input("Source IP Address", "192.168.1.2")
    dst_ip = st.text_input("Destination IP Address", "192.168.1.10")
    protocol = st.selectbox("Protocol", ["6", "1", "17", "ARP"])

    if st.button("Predict"):
        inputs = {
            "src_mac": src_mac.strip(),
            "dst_mac": dst_mac.strip(),
            "src_ip": src_ip.strip(),
            "dst_ip": dst_ip.strip(),
            "protocol": protocol.strip()
        }

        try:
            for key in ["src_mac", "dst_mac", "src_ip", "dst_ip", "protocol"]:
                le = artifacts["label_encoders"][key]
                inputs[key] = le.transform([inputs[key]])[0]

            # Prepare and scale input
            feature_order = ["src_mac", "dst_mac", "src_ip", "dst_ip", "protocol"]
            user_input = np.array([[inputs[feat] for feat in feature_order]])
            user_input_scaled = artifacts["scaler"].transform(user_input)

            # Predict
            prediction = artifacts["model"].predict(user_input_scaled)
            predicted_label = artifacts["label_encoders"]["label"].inverse_transform(prediction)

            st.success(f"✅ Predicted Label: {predicted_label[0]}")
        except ValueError as e:
            st.error(f"❌ Invalid input: {e}")

if __name__ == "__main__":
    main()
