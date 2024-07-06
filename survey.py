import streamlit as st
import pandas as pd
import numpy as np
import random
import os
from streamlit_player import st_player

def main():
    unique_id = f'{pd.Timestamp.now().strftime("%Y%m%d%H%M%S")}-{random.randint(1000, 9999)}'
    st.write(f"Session ID: {unique_id}")

    # Display static content only once
    if 'content_initialized' not in st.session_state:
        st_player("https://youtu.be/Q-Ev5tpapV4?si=Pj2W1EXmTefhpcDl")
        st.image("./survey.png")
        st.session_state['content_initialized'] = True

    # Random Assignment of Video with or without Rebuttal
    if 'video_assignment' not in st.session_state:
        video_source = random.randint(1000,9999)
        if video_source % 2 == 0:
            st.session_state['video_assignment'] = "https://www.youtube.com/embed/I5aiAsh79-E?si=QEMO9vHgBUNYKtHQ"
        else:
            st.session_state['video_assignment'] = "https://www.youtube.com/embed/g1Ul5tVRWYc?si=ouIAlF-Zcr1O3fs9"
        st.session_state['video_displayed'] = False

    # Initialize or load existing data frame
    csv_file_path = 'video_analysis_data.csv'
    if os.path.exists(csv_file_path):
        data = pd.read_csv(csv_file_path)
    else:
        data = pd.DataFrame(columns=['SessionID', 'Timestamp', 'Age', 'Citizen', 'Voter', 'Fair', 'Trust', 'Behavior', 'Emotion', 'Decision'])

    # Form for participant qualification
    with st.form("Qualification_Attitude"):
        age = st.radio("Are you over the age of 18?", ("Yes", "No"), key="q1")
        citizen = st.radio("Are you a Citizen of the United States?", ("Yes", "No"), key="q2")
        voter_registration = st.radio("Are you a registered voter, actual voter and/or resident of any U.S. state or territory for at least a year?", ("Yes", "No"), key="q3")
        fair = st.radio("Do you believe that the criminal justice system is fair?", ("Yes", "No"), key="q4")
        trust = st.radio("Do you trust police officers, lawyers and judges?", ("Yes", "No"), key="q5")
        submitted = st.form_submit_button("Submit")

    if submitted:
        if age == "Yes" and citizen == "Yes" and voter_registration == "Yes":
            st.session_state['form_submitted'] = True
            st.session_state['user_data'] = {
                'SessionID': unique_id,
                'Age': age,
                'Citizen': citizen,
                'Voter': voter_registration,
                'Fair': fair,
                'Trust': trust
            }
            st.session_state['video_displayed'] = True  # Ensure video is marked to be displayed
        else:
            st.error("Unfortunately, you do not meet the criteria for participation. Thank you for your interest.")
            st.stop()

    if 'video_displayed' not in st.session_state or st.session_state['video_displayed']:
        st_player(st.session_state['video_assignment'], key="video_player")

    if 'form_submitted' in st.session_state:
        # Slider interactions
        behavior = st.slider('Behavior (B)', -1.0, 1.0, 0.0, 0.1, key='behavior')
        emotion = st.slider('Emotion (E)', -1.0, 1.0, 0.0, 0.1, key='emotion')
        decision = st.slider('Decision (D)', -1.0, 1.0, 0.0, 0.1, key='decision')

        # Save data on finish
        if st.button('FINISH'):
            current_time = pd.Timestamp.now()
            slider_data = pd.DataFrame([{
                'SessionID': st.session_state['user_data']['SessionID'],
                'Timestamp': current_time,
                'Age': st.session_state['user_data']['Age'],
                'Citizen': st.session_state['user_data']['Citizen'],
                'Voter': st.session_state['user_data']['Voter'],
                'Fair': st.session_state['user_data']['Fair'],
                'Trust': st.session_state['user_data']['Trust'],
                'Behavior': behavior,
                'Emotion': emotion,
                'Decision': decision
            }])

            # Append to dataframe and save to CSV
            data = pd.concat([data, slider_data], ignore_index=True)
            data.to_csv(csv_file_path, mode='a', header=not os.path.exists(csv_file_path), index=False)
            st.success("Data saved successfully.")
            st.balloons()  # Optional: show celebration balloons on completing the data entry
            st.session_state.clear()  # Optionally clear session state
            st.write("Thank you for your participation. You may close this window.")

if __name__ == "__main__":
    main()


