import streamlit as st
import requests
import os

# Set backend URL to the Render-deployed FastAPI instance
BACKEND_URL = os.getenv("BACKEND_URL", "https://ai-business-insiderrr.onrender.com")

st.title("The AI Business Insider")

# System Status Section
st.sidebar.markdown("### System Status")
connection_status_placeholder = st.sidebar.empty()

try:
    # Attempt to connect to the backend
    health_check = requests.get(f"{BACKEND_URL}/health", timeout=5)
    if health_check.ok:
        connection_status_placeholder.success("✅ Backend Connected")
        st.sidebar.info(f"Environment: {health_check.json().get('environment', 'unknown')}")
    else:
        connection_status_placeholder.error("❌ Backend Error")
except Exception as e:
    # If connection fails, show only this error message
    connection_status_placeholder.error("❌ Backend Not Connected")
    st.sidebar.info(f"Backend URL: {BACKEND_URL}")

# Input Section
topic = st.text_input("Enter a topic to analyze:", key="topic_input")

# Analysis Button and Results
if st.button("Analyze"):
    if topic:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/analyze",
                    json={"topic": topic},
                    timeout=300  # 5 minute timeout
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
                
            except requests.exceptions.ConnectionError:
                st.error(f"Cannot connect to backend at {BACKEND_URL}. Please ensure the backend server is running.")
            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with backend: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a topic to analyze")
