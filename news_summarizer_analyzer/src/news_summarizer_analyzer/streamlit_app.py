import streamlit as st
import requests
import os

# Add development/production URL handling
is_production = os.getenv("ENVIRONMENT") == "production"
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://ai-business-insiderrr.onrender.com" if is_production else "http://localhost:8000"
)

st.title("The AI Business Insider")

st.sidebar.markdown("### System Status")

# SSL verification conditionally based on environment
verify_ssl = is_production

try:
    health_check = requests.get(
        f"{BACKEND_URL}/health", 
        timeout=5,
        verify=verify_ssl
    )
    if health_check.ok:
        st.sidebar.success("✅ Backend Connected")
        st.sidebar.info(f"Environment: {health_check.json().get('environment', 'unknown')}")
    else:
        st.sidebar.error("❌ Backend Error")
except requests.exceptions.SSLError:
    st.sidebar.error("❌ SSL Certificate Error")
except Exception as e:
    st.sidebar.error("❌ Backend Not Connected")
    st.sidebar.info(f"Backend URL: {BACKEND_URL}")

topic = st.text_input("Enter a topic to analyze:", key="topic_input")

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
