import streamlit as st
import requests

st.title("The AI Business Insider")

# Get user input
topic = st.text_input("Enter a topic to analyze:", key="topic_input")

if st.button("Analyze"):
    if topic:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze",
                    json={"topic": topic}
                )
                response.raise_for_status()
                result = response.json()
                
                st.success("Analysis Complete!")
                
                # Display summary
                st.header("Summary")
                st.write(result["summary"])
                
                # Display individual task results
                st.header("Detailed Analysis")
                for task in result["tasks"]:
                    with st.expander(f"Task: {task['description']}", expanded=False):
                        st.write(task["output"])
                
            
                
            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with backend: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a topic to analyze")