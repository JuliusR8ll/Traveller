import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils import get_travel_preferences, generate_itinerary
from pathlib import Path
# Load environment variables with explicit path

load_dotenv()

# Debug print to check if API key is loaded and print current working directory
api_key = os.getenv("GOOGLE_API_KEY")
print(api_key)


print(f"Current working directory: {os.getcwd()}")
# print(f"Looking for .env file at: {env_path.absolute()}")
print(f"API Key loaded: {api_key is not None}")  # Don't print the actual key for security
if api_key is None:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def main():
    st.title("AI Travel Planner 🌎✈️")
    
    # Initialize session state
    if 'stage' not in st.session_state:
        st.session_state.stage = 'initial'
        st.session_state.preferences = {}
        st.session_state.itinerary = None

    if st.session_state.stage == 'initial':
        # Basic information form
        with st.form("travel_form"):
            destination = st.text_input("Where would you like to go?")
            duration = st.number_input("How many days is your trip?", min_value=1, max_value=30, value=3)
            budget = st.selectbox("What's your budget level?", 
                                ["Budget", "Moderate", "Luxury"])
            purpose = st.text_input("What's the main purpose of your trip? (e.g., adventure, relaxation, culture)")
            
            submit = st.form_submit_button("Next")
            
            if submit and destination and duration and budget and purpose:
                st.session_state.preferences = {
                    "destination": destination,
                    "duration": duration,
                    "budget": budget,
                    "purpose": purpose
                }
                st.session_state.stage = 'detailed'
                st.rerun()

    elif st.session_state.stage == 'detailed':
        # Show current preferences
        st.write("### Your Travel Preferences")
        for key, value in st.session_state.preferences.items():
            st.write(f"**{key.title()}:** {value}")
            
        # Get detailed preferences
        detailed_prefs = get_travel_preferences(model, st.session_state.preferences)
        
        if detailed_prefs:
            st.session_state.preferences.update(detailed_prefs)
            st.session_state.stage = 'generate'
            st.rerun()

    elif st.session_state.stage == 'generate':
        if st.session_state.itinerary is None:
            with st.spinner("Generating your personalized itinerary..."):
                itinerary = generate_itinerary(model, st.session_state.preferences)
                st.session_state.itinerary = itinerary

        st.write("### Your Personalized Itinerary")
        st.markdown(st.session_state.itinerary)
        
        if st.button("Start Over"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main() 