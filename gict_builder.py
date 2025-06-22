import streamlit as st
import pandas as pd
import os
from datetime import datetime, date

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if "file_records" not in st.session_state:
    st.session_state.file_records = []

if "program_df" not in st.session_state:
    st.session_state.program_df = pd.DataFrame(columns=["時間", "セッション", "演者", "備考"])

if "roles_df" not in st.session_state:
    st.session_state.roles_df = pd.DataFrame(columns=["氏名", "所属", "役割", "担当業務", "備考"])

if "abstracts_df" not in st.session_state:
    st.session_state.abstracts_df = pd.DataFrame(columns=["演題名", "演者", "所属", "抄録本文", "備考"])

st.set_page_config(page_title="GICT設営ビルダー", layout="wide")
st.title("📅 第24回 日本消化管CT技術学会 - 設営ビルダー")
st.markdown("2026年6月20日（土曜日）｜会場：順天堂大学（予定）")

tabs = st.tabs([
    "基本情報",
    "プログラム構成",
    "役割分担",
    "登録・抄録",
    "会場詳細",
    "議事録/アップロード"
])

with tabs[0]:
    st.subheader("📌 基本情報")
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("開催予定日", date(2026, 6, 20))
        st.text_input("会場", "順天堂大学（予定）")
        st.text_input("副大会長")
    with col2:
        st.text_area("事務局連絡先")
        st.text_input("最終会議Zoomリンク")
        st.text_area("備考")

with tabs[1]:
    st.subheader("🕒 タイムテーブル構成")
    edited = st.data_editor(st.session_state.program_df, num_rows="dynamic")
    st.session_state.program_df = edited
    st.download_button("CSVとして保存", edited.to_csv(index=False).encode(), file_name="program.csv")

with tabs[2]:
    st.subheader("👥 理事・評議員 役割分担")
    edited = st.data_editor(st.session_state.roles_df, num_rows="dynamic")
    st.session_state.roles_df = edited
    st.download_button("CSVとして保存", edited.to_csv(index=False).encode(), file_name="roles.csv")

with tabs[3]:
    st.subheader("📝 参加登録・抄録管理")
    st.text_input("抄録集パスワード配布方法", "別途メール送信")
    st.number_input("当日会員参加費（円）", 0, 10000, 3000)
    st.text_area("協賛企業・進捗", "ブラッコ・ジャパンより協賛予定")
    st.text_area("抄録管理の備考")

    st.markdown("### 📋 抄録一覧")
    edited = st.data_editor(st.session_state.abstracts_df, num_rows="dynamic")
    st.session_state.abstracts_df = edited
    st.download_button("CSVとして保存", edited.to_csv(index=False).encode(), file_name="abstracts.csv")

with tabs[4]:
    st.subheader("🏢 会場詳細")
    st.text_area("会場地図URLまたは内容")
    st.text_area("電子機器・音響・ライト系の確保")
    st.text_area("展示スペースの保持場所の情報")
    st.text_area("会場偵察/注意点メモ")

with tabs[5]:
    st.subheader("✅ 議事録・アップロード")
    uploaded = st.file_uploader("ファイルをアップロード", accept_multiple_files=True)
    category = st.text_input("カテゴリ（例：議事録、会場情報など）")
    if st.button("アップロード") and uploaded:
        for f in uploaded:
            fname = f.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_fname = f"{timestamp}__{fname}"
            path = os.path.join(UPLOAD_DIR, new_fname)
            with open(path, "wb") as out:
                out.write(f.read())
            st.session_state.file_records.append({
                "ファイル名": new_fname,
                "カテゴリ": category,
                "アップロード日時": timestamp
            })
        st.success("アップロード完了")

    st.markdown("### 📂 アップロード済みファイル一覧")
    for row in st.session_state.file_records[::-1]:
        filepath = os.path.join(UPLOAD_DIR, row['ファイル名'])
        st.markdown(f"✅ **[{row['ファイル名']}]({filepath})**（{row['カテゴリ']} | {row['アップロード日時']}）")
