import pickle
import numpy as np
import streamlit as st


def add_prediction(input_data):
    model = pickle.load(open("artifacts/model_trainer/model.pkl", "rb"))
    scaler = pickle.load(open("artifacts/model_trainer/scaler.pkl", "rb"))

    input_array = np.array(list(input_data.values())).reshape(1, -1)
    input_array_scaled = scaler.transform(input_array)

    prediction = model.predict(input_array_scaled)

    st.subheader("Cell cluster prediction")
    st.write("The cell cluster is:")

    if prediction[0] == 0:
        st.write("<span class='diagnosis benign'>Benign</span>",
                 unsafe_allow_html=True)
    else:
        st.write("<span class='diagnosis malicious'>Malicious</span>",
                 unsafe_allow_html=True)

    st.write("Probability of being benign: ",
             model.predict_proba(input_array_scaled)[0][0])
    st.write("Probability of being malicious: ",
             model.predict_proba(input_array_scaled)[0][1])

    st.write("This app can assist medical professionals in making a diagnosis, but should not be used as a substitute for a professional diagnosis.")
