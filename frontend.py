import streamlit as st
import requests
import time
from PIL import Image

API_URL    = "http://localhost:4706/kanzeon/summarize"
STATUS_URL = "http://localhost:4706/kanzeon/status"
favicon    = Image.open("./img/Kanzeon1x1-Erased.png")

st.set_page_config(page_title="Kanzeon Summarizer", page_icon=favicon)
st.title("🌸 Kanzeon")
st.caption("Clarity, among chaos.")

# Sidebar status panel with manual refresh
st.sidebar.header("Service Status")

# Initialize session state to hold the last status
if "status_data" not in st.session_state:
    st.session_state.status_data = None

# Button to refresh status
if st.sidebar.button("🔄 Refresh Status"):
    try:
        r = requests.get(STATUS_URL, timeout=2)
        r.raise_for_status()
        st.session_state.status_data = r.json()
    except Exception as e:
        st.session_state.status_data = {"error": str(e)}

# Display status (if any)
if st.session_state.status_data:
    if "error" in st.session_state.status_data:
        st.sidebar.error(f"Error: {st.session_state.status_data['error']}")
    else:
        st.sidebar.json(st.session_state.status_data)
else:
    st.sidebar.info("Click “Refresh Status” to check API health.")

# —— rest of your UI —— #

option = st.radio("Choose input type:", ["Text", "File"])

if option == "Text":
    text = st.text_area("Enter text here", height=300)
    if st.button("Summarize"):
        if text.strip():
            with st.spinner("Summarizing..."):
                start = time.time()
                res = requests.post(API_URL, json={"text": text})
                elapsed = round(time.time() - start, 2)
                if res.status_code == 200:
                    st.success("Summary:")
                    st.write(res.json()["summary"])
                    st.info(f"Took {elapsed} seconds.")
                else:
                    st.error(res.json().get("error", "Something went wrong."))
        else:
            st.warning("Please enter some text.")

elif option == "File":
    file = st.file_uploader("Upload a PDF or image",
                            type=["pdf","png","jpg","jpeg","bmp"])
    if file and st.button("Summarize File"):
        with st.spinner("Processing file..."):
            res = requests.post(API_URL, files={"file": (file.name, file, file.type)})
            if res.status_code == 200:
                st.success("Summary:")
                st.write(res.json()["summary"])
                st.info(f"Took {res.json().get('time_taken','N/A')}")
            else:
                st.error(res.json().get("error","Failed to summarize the file."))