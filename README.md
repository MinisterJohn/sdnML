<<<<<<< HEAD
# SDN Attack Detection and Mitigation System

A machine learning-based system for detecting and mitigating attacks on Software Defined Networking (SDN) controllers. This application uses a Random Forest model to analyze network packet features and identify potential security threats.

## Features

- Real-time attack detection based on network packet features
- User-friendly web interface built with Streamlit
- Support for analyzing various network protocols (TCP, UDP, ICMP)
- Pre-trained model for immediate deployment

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone <your-repository-url>
cd sdnML
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run streamlit_app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Enter the following network packet features:
   - Source MAC Address
   - Destination MAC Address
   - Source IP Address
   - Destination IP Address
   - Protocol (TCP/UDP/ICMP)

4. Click the "Predict" button to get the prediction result

## Model Information

The system uses a pre-trained Random Forest model that has been trained on simulated network data. The model is stored in `RandomForest_best_model.pkl` along with the necessary preprocessing artifacts (`scaler.pkl` and `label_encoders.pkl`).

## Project Structure

- `streamlit_app.py` - Main application file
- `RandomForest_best_model.pkl` - Trained Random Forest model
- `scaler.pkl` - Feature scaler for preprocessing
- `label_encoders.pkl` - Label encoders for categorical features
- `simulated_dataset.csv` - Sample dataset used for training
- `requirements.txt` - Python package dependencies

## Deployment

This application can be deployed on Streamlit Cloud. Simply push your code to a GitHub repository and connect it to Streamlit Cloud using the provided interface.

## License

[Add your license information here]

## Contact

[Add your contact information here] 
=======
# sdnML
>>>>>>> 9751d1f675dc7543d9174e717694cc07b6f5c38d
