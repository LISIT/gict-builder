import streamlit as st
import os
from datetime import datetime

# 保存先ディレクトリの作成
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ファイル保存関数（GitHub連携なし、ローカル保存のみ）
def save_uploaded_file(uploaded_file, category):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = uploaded_file.name.replace(" ", "_")
    save_name = f"{category}__{timestamp}__{filename}"
    filepath = os.path.join(UPLOAD_DIR, save_name)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"{uploaded_file.name} を保存しました。")
    return save_name

# Streamlit UI（例：ファイルアップロードフォーム）
st.set_page_config(page_title="GICT学会設営ビルダー", layout="centered")
st.title("📁 GICT学会ファイルアップローダー（ローカル保存のみ）")

with st.form("upload_form"):
    uploaded_file = st.file_uploader("ファイルを選択してください", type=None)
    category = st.text_input("カテゴリ（例：議事録、会場詳細など）")
    submitted = st.form_submit_button("アップロード")

    if submitted and uploaded_file and category:
        save_uploaded_file(uploaded_file, category)

# 保存済みファイル一覧表示
if os.path.exists(UPLOAD_DIR):
    st.markdown("### 🔽 アップロード済みファイル一覧")
    for fname in sorted(os.listdir(UPLOAD_DIR), reverse=True):
        st.markdown(f"📄 **{fname}**")
