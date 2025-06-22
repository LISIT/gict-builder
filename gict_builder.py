import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import json

UPLOAD_DIR = "uploaded_files"
RECORD_FILE = "file_records.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_file_records():
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_file_records(records):
    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

if "file_records" not in st.session_state:
    st.session_state.file_records = load_file_records()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.set_page_config(page_title="第24回 日本消化管CT技術学会 - 設営ビルダー", layout="wide")
    st.title("🔐 第24回 日本消化管CT技術学会 - 設営ビルダー")
    password = st.text_input("パスワードを入力してください", type="password")
    if password == "gict2026":
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.error("パスワードが間違っています")
    st.stop()

if "program_df" not in st.session_state:
    st.session_state.program_df = pd.DataFrame(columns=["時間", "セッション", "演者", "備考"])

if "roles_df" not in st.session_state:
    st.session_state.roles_df = pd.DataFrame(columns=["氏名", "所属", "役割", "担当業務", "備考"])

if "abstracts_df" not in st.session_state:
    st.session_state.abstracts_df = pd.DataFrame(columns=["演題名", "演者", "所属", "抄録本文", "備考"])

if "venue_detail" not in st.session_state:
    st.session_state.venue_detail = {
        "map": "",
        "equipment": "",
        "booth": "",
        "memo": "",
        "facility_letter": ""
    }

st.set_page_config(page_title="第24回 日本消化管CT技術学会 - 設営ビルダー", layout="wide")
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
    st.session_state.venue_detail["map"] = st.text_area("会場地図URLまたは内容", value=st.session_state.venue_detail["map"])
    st.session_state.venue_detail["equipment"] = st.text_area("電子機器・音響・ライト系の確保", value=st.session_state.venue_detail["equipment"])
    st.session_state.venue_detail["booth"] = st.text_area("展示スペースの保持場所の情報", value=st.session_state.venue_detail["booth"])
    st.session_state.venue_detail["memo"] = st.text_area("会場偵察/注意点メモ", value=st.session_state.venue_detail["memo"])

    st.subheader("📨 順天堂大学への施設使用依頼書")
    facility_letter = st.file_uploader("依頼書ファイルアップロード（PDF / Word）", key="facility_letter")
    if facility_letter:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"facility_letter__{timestamp}__{facility_letter.name}"
        fpath = os.path.join(UPLOAD_DIR, fname)
        with open(fpath, "wb") as f:
            f.write(facility_letter.read())
        st.session_state.venue_detail["facility_letter"] = fname
        st.session_state.file_records.append({
            "ファイル名": fname,
            "カテゴリ": "順天堂大学依頼書",
            "アップロード日時": timestamp
        })
        save_file_records(st.session_state.file_records)
        st.success(f"依頼書「{facility_letter.name}」を保存しました。前回アップロードしたファイルは下記をご確認ください。")

    st.markdown("### 📂 アップロード済み依頼書一覧")
    updated_records = []
    for i, row in enumerate(st.session_state.file_records):
        if row['カテゴリ'] == "順天堂大学依頼書":
            filepath = os.path.join(UPLOAD_DIR, row['ファイル名'])
            if os.path.exists(filepath):
                cols = st.columns([6, 2])
                with cols[0]:
                    with open(filepath, "rb") as f:
                        st.download_button(
                            label=f"📄 {row['ファイル名']}（{row['アップロード日時']}）",
                            data=f,
                            file_name=row['ファイル名'],
                            mime="application/octet-stream",
                            key=f"facility_download_{i}"
                        )
                with cols[1]:
                    if st.button("削除", key=f"facility_delete_{i}"):
                        os.remove(filepath)
                        continue  # スキップして記録しない
                updated_records.append(row)
    st.session_state.file_records = [r for r in updated_records if os.path.exists(os.path.join(UPLOAD_DIR, r['ファイル名']))]
    save_file_records(st.session_state.file_records)

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
        save_file_records(st.session_state.file_records)
        st.success("アップロード完了")

    st.markdown("### 📂 アップロード済みファイル一覧")
    new_records = []
    for i, row in enumerate(st.session_state.file_records):
        filepath = os.path.join(UPLOAD_DIR, row['ファイル名'])
        if os.path.exists(filepath):
            cols = st.columns([6, 2])
            with cols[0]:
                with open(filepath, "rb") as f:
                    st.download_button(
                        label=f"📄 {row['ファイル名']}（{row['カテゴリ']} | {row['アップロード日時']}）",
                        data=f,
                        file_name=row['ファイル名'],
                        mime="application/octet-stream",
                        key=f"download_{i}"
                    )
            with cols[1]:
                if st.button("削除", key=f"delete_{i}"):
                    os.remove(filepath)
                    continue
            new_records.append(row)
    st.session_state.file_records = [r for r in new_records if os.path.exists(os.path.join(UPLOAD_DIR, r['ファイル名']))]
    save_file_records(st.session_state.file_records)
