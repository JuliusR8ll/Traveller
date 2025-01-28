def get_travel_preferences(model, basic_prefs):
    """Get detailed travel preferences using Gemini."""
    
    prompt = f"""
    Based on these basic travel preferences:
    Destination: {basic_prefs['destination']}
    Duration: {basic_prefs['duration']} days
    Budget: {basic_prefs['budget']}
    Purpose: {basic_prefs['purpose']}

    Please ask the most important questions (maximum 6) to gather additional details for creating a personalized itinerary.
    Make sure to include a question about their preferred wake-up and bedtime schedule to plan activities accordingly.
    Format the questions as a numbered list.
    """
    
    response = model.generate_content(prompt)
    questions = response.text
    
    # Display questions and get user input
    import streamlit as st
    
    st.write("### Additional Information Needed")
    st.write(questions)
    
    detailed_prefs = {}
    with st.form("detailed_preferences"):
        answers = st.text_area("Please provide your answers to the questions above:", 
                             height=200,
                             help="Enter your answers, one per line")
        submit = st.form_submit_button("Generate Itinerary")
        
        if submit:
            detailed_prefs['additional_info'] = answers
            return detailed_prefs
    
    return None

def generate_itinerary(model, preferences):
    
    prompt = f"""
    Act as an excited expert travel planner and create a detailed day-by-day itinerary based on these preferences:
    Based on the location show the budget in the currency of the location.
    
    Destination: {preferences['destination']}
    Duration: {preferences['duration']} days
    Budget Level: {preferences['budget']}
    Purpose: {preferences['purpose']}
    Additional Information: {preferences.get('additional_info', 'None provided')}

    Important: Plan activities according to the user's sleep schedule mentioned in their additional information.
    Avoid scheduling activities during their preferred sleep times and account for jet lag if traveling across time zones.

    Please provide:
    1. A day-by-day breakdown of activities
    2. Suggested times for each activity (aligned with their wake/sleep schedule)
    3. Estimated costs where relevant
    4. Travel tips and recommendations
    5. Dining suggestions that match the budget level

    Format the itinerary in a clear, readable way using markdown.
    Include emoji icons where appropriate, add sarcasm to make it visually engaging.
    """
    
    response = model.generate_content(prompt)
    return response.text 