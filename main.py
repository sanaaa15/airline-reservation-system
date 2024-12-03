from pyngrok import ngrok
import os

# Run Streamlit app
def run_streamlit():
    os.system("streamlit run app.py --server.port 8501")

# Set up ngrok for the correct port
public_url = ngrok.connect(8501)  # Streamlit's default port
print(f"Access your app here: {public_url}")

# Start Streamlit app
run_streamlit()
