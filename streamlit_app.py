import streamlit as st
import joblib
import numpy as np
import pandas as pd
from PIL import Image

@st.cache_resource
def load_artifacts(model_name):
    return {
        "model": joblib.load(model_name),
        "scaler": joblib.load("scaler.pkl"),
        "label_encoders": joblib.load("label_encoders.pkl")
    }

def get_mitigation_strategy(attack_type):
    strategies = {
        "normal traffic": "No mitigation required. Network traffic appears normal.",
        "DoS attack": """
        ### 🛡️ DoS Attack Mitigation Strategies:
        1. Implement rate limiting on the controller
        2. Deploy traffic filtering rules
        3. Use SYN cookies for TCP connections
        4. Enable flow table timeouts
        5. Deploy backup controllers
        """,
        "ARP spoofing": """
        ### 🛡️ ARP Spoofing Mitigation Strategies:
        1. Implement ARP inspection
        2. Use static ARP entries for critical devices
        3. Enable port security
        4. Deploy ARP monitoring tools
        5. Implement MAC address binding
        """,
        
        "flow_table_attack": """
        ### 🛡️ Flow Table Attack Mitigation Strategies:
        1. Implement flow table size limits per switch
        2. Enable flow table monitoring and alerts
        3. Deploy flow table cleanup policies
        4. Use flow table compression techniques
        5. Implement flow entry timeouts
        6. Deploy flow table backup mechanisms
        7. Use flow table aggregation where possible
        8. Implement flow table overflow protection
        9. Enable flow table statistics collection
        10. Deploy flow table load balancing
        """
    }
    return strategies.get(attack_type.lower(), "Unknown attack type. No specific mitigation strategy available.")

def preprocess_input(inputs, artifacts):
    # Create a DataFrame with the same structure as training data
    df = pd.DataFrame([inputs])
    
    # Apply label encoding to categorical features
    for feature in ["src_mac", "dst_mac", "src_ip", "dst_ip", "protocol"]:
        le = artifacts["label_encoders"][feature]
        df[feature] = le.transform(df[feature])
    
    # Scale the features
    feature_order = ["src_mac", "dst_mac", "src_ip", "dst_ip", "protocol"]
    scaled_features = artifacts["scaler"].transform(df[feature_order])
    
    return scaled_features

def main():
    # Set page config
    st.set_page_config(
        page_title="SDN Attack Detection",
        page_icon="🛡️",
        layout="wide"
    )

    # Load artifacts
    artifacts = load_artifacts("RandomForest_best_model.pkl")

    # Custom CSS
    st.markdown("""
        <style>
        .main {
            background-color: #f5f5f5;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .stTextInput>div>div>input {
            border-radius: 5px;
        }
        .css-1d391kg {
            padding: 1rem;
            border-radius: 5px;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .mitigation-box {
            background-color: #fff3cd;
            padding: 1rem;
            border-radius: 5px;
            margin-top: 1rem;
            border-left: 4px solid #ffc107;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.title("About")
        st.markdown("""
        This application uses machine learning to detect and mitigate attacks on SDN controllers.
        
        ### Features
        - Real-time attack detection
        - Multiple protocol support
        - Pre-trained model
        """)
        
        st.markdown("---")
        st.markdown("### Protocol Codes")
        st.markdown("""
        - 6: TCP
        - 1: ICMP
        - 17: UDP
        - ARP: Address Resolution Protocol
        """)

    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("🛡️ SDN Attack Detection System")
        st.markdown("### Enter Network Packet Features")
        
        # Create two columns for input fields
        col_a, col_b = st.columns(2)
        
        with col_a:
            src_mac = st.text_input("Source MAC Address", "00:1B:44:11:3A:B7")
            dst_mac = st.text_input("Destination MAC Address", "00:1B:44:11:3A:C8")
            protocol = st.selectbox("Protocol", ["6", "1", "17", "ARP"])
        
        with col_b:
            src_ip = st.text_input("Source IP Address", "192.168.1.2")
            dst_ip = st.text_input("Destination IP Address", "192.168.1.10")
        
        if st.button("🔍 Analyze Network Traffic"):
            inputs = {
                "src_mac": src_mac.strip(),
                "dst_mac": dst_mac.strip(),
                "src_ip": src_ip.strip(),
                "dst_ip": dst_ip.strip(),
                "protocol": protocol.strip()
            }

            try:
                # Preprocess the input features
                processed_input = preprocess_input(inputs, artifacts)
                
                # Make prediction
                prediction = artifacts["model"].predict(processed_input)
                predicted_label = artifacts["label_encoders"]["label"].inverse_transform(prediction)
                attack_type = predicted_label[0]

                # Display prediction with appropriate styling
                if "normal" in attack_type.lower():
                    st.success(f"✅ Status: {attack_type}")
                else:
                    st.error(f"⚠️ Warning: {attack_type} Detected!")
                
                # Add some visual feedback
                st.markdown("---")
                st.markdown("### Analysis Details")
                st.markdown(f"""
                - Source: {src_ip} ({src_mac})
                - Destination: {dst_ip} ({dst_mac})
                - Protocol: {protocol}
                """)
                
                # Display mitigation strategies
                st.markdown("---")
                st.markdown("### Mitigation Strategy")
                st.markdown(f'<div class="mitigation-box">{get_mitigation_strategy(attack_type)}</div>', unsafe_allow_html=True)
                
            except ValueError as e:
                st.error(f"❌ Error: {str(e)}")

    with col2:
        st.markdown("### Network Traffic Flow")
        st.markdown("""
        ```
        Source → Protocol → Destination
        {} → {} → {}
        ```
        """.format(src_ip, protocol, dst_ip))
        
        # Add a simple network diagram using markdown
        st.markdown("""
        <div style="text-align: center;">
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px;">
                <div style="width: 40px; height: 40px; background-color: #4CAF50; border-radius: 50%;"></div>
                <div style="width: 100px; height: 2px; background-color: #2196F3;"></div>
                <div style="width: 40px; height: 40px; background-color: #FF5252; border-radius: 50%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0 20px;">
                <span>Source</span>
                <span>Destination</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
