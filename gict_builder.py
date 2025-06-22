import streamlit as st
import os
from datetime import datetime
import base64
import requests

GITHUB_USER = "LISIT"
GITHUB_REPO = "gict_builder"
GITHUB_BRANCH = "main"
GITHUB_TOKEN = st.secrets["github_token"]

def backup_to_github(local_path, github_path, commit_message):
    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{github_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None
    data = {
        "message": commit_message,
        "content": content,
        "branch": GITHUB_BRANCH
    }
    if sha:
        data["sha"] = sha
    res = requests.put(url, json=data, headers=headers)
    return res.status_code in [200, 201]

def save_uploaded_file(uploaded_file, category):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = uploaded_file.name.replace(" ", "_")
    save_name = f"{category}__{timestamp}__{filename}"
    filepath = os.path.join("uploaded_files", save_name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"{uploaded_file.name} を保存しました。")
    backup_to_github(filepath, f"uploaded_files/{save_name}", f"Upload {save_name}")
    return save_name
