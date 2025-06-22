import streamlit as st
import pandas as pd
from datetime import date, datetime
import os

st.set_page_config(page_title="GICT設営ビルダー", layout="wide")
st.title("📅 第24回 日本消化管CT技術学会 - 設営ビルダー")
st.markdown("🗓️ 開催予定日：**2026年6月20日（土）**｜会場：順天堂大学（仮）")

# ログイン認証（ヒントなし）
st.subheader("🔒 ログイン認証")
password = st.text_input("パスコードを入力してください", type="password")
if password != "gict2026":
    st.warning("正しいパスコードを入力してください")
    st.stop()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file, category):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = uploaded_file.name.replace(" ", "_")
    save_name = f"{category}__{timestamp}__{filename}"
    filepath = os.path.join(UPLOAD_DIR, save_name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"{uploaded_file.name} を保存しました。")
    return save_name

def list_uploaded_files():
    files = sorted(os.listdir(UPLOAD_DIR))
    data = []
    for f in files:
        parts = f.split("__", 2)
        if len(parts) == 3:
            category, timestamp, filename = parts
            dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
            data.append({
                "カテゴリ": category,
                "ファイル名": filename,
                "アップロード日時": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "パス": f"{UPLOAD_DIR}/{f}"
            })
    return pd.DataFrame(data)

# タブ構成
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "基本情報", "プログラム構成", "役割分担", "登録・抄録",
    "会場詳細", "議事録/アップロード", "📂 アップロード一覧"
])

with tab1:
    st.subheader("📌 基本情報")
    col1, col2 = st.columns(2)
    with col1:
        date_input = st.date_input("開催予定日", date(2026, 6, 20))
        location = st.text_input("会場", "順天堂大学（仮）")
        chair = st.text_input("大会長（仮）", "未記載")
        vice_chair = st.text_input("副大会長")
    with col2:
        contact = st.text_area("事務局連絡先")
        zoom_link = st.text_input("最終会議Zoomリンク")
        notes = st.text_area("備考")

with tab2:
    st.subheader("🕒 プログラム構成")
    if "program_df" not in st.session_state:
        st.session_state["program_df"] = pd.DataFrame(columns=["時間", "セッション", "演者", "備考"])
    edited = st.data_editor(st.session_state["program_df"], num_rows="dynamic")
    st.session_state["program_df"] = edited
    st.download_button("📥 CSV出力", edited.to_csv(index=False).encode("utf-8"), "プログラム構成.csv", "text/csv")

with tab3:
    st.subheader("👥 役割分担")
    if "roles_df" not in st.session_state:
        st.session_state["roles_df"] = pd.DataFrame(columns=["氏名", "所属", "役割", "担当業務", "備考"])
    edited = st.data_editor(st.session_state["roles_df"], num_rows="dynamic")
    st.session_state["roles_df"] = edited
    st.download_button("📥 CSV出力", edited.to_csv(index=False).encode("utf-8"), "役割分担.csv", "text/csv")

with tab4:
    st.subheader("📝 登録・抄録管理")
    password_policy = st.text_input("抄録集パスワード配布方法", "別途メール送信")
    participant_fee = st.number_input("当日会員参加費（円）", 0, 10000, 3000)
    sponsor = st.text_area("協賛企業・進捗")
    abstract_note = st.text_area("抄録管理の備考")
    reg_df = pd.DataFrame({
        "抄録パスワード配布方法": [password_policy],
        "当日参加費": [participant_fee],
        "協賛企業進捗": [sponsor],
        "備考": [abstract_note]
    })
    st.download_button("📥 CSV出力", reg_df.to_csv(index=False).encode("utf-8"), "登録_抄録.csv", "text/csv")

with tab5:
    st.subheader("🏛️ 会場詳細・依頼書")
    venue_file = st.file_uploader("順天堂大学への依頼書", type=["pdf", "docx"], key="venue")
    if venue_file:
        save_uploaded_file(venue_file, "venue")
    map_file = st.file_uploader("構内図やアクセスマップ", type=["pdf", "png", "jpg"], key="map")
    if map_file:
        save_uploaded_file(map_file, "map")

with tab6:
    st.subheader("📎 会議資料・議事録")
    meeting_file = st.file_uploader("会議資料をアップロード", type=["pdf", "docx", "xlsx"], key="minutes")
    if meeting_file:
        save_uploaded_file(meeting_file, "minutes")
    memo = st.text_area("会議メモ", "・第1回準備会議予定：2025年10月")
    st.download_button("📥 メモCSV出力", pd.DataFrame({"共有メモ": [memo]}).to_csv(index=False).encode("utf-8"), "議事メモ.csv", "text/csv")

with tab7:
    st.subheader("📂 すべてのアップロードファイル一覧")
    df = list_uploaded_files()
    if not df.empty:
        for _, row in df.iterrows():
            st.markdown(
                f"📄 **{row['ファイル名']}**（{row['カテゴリ']} | {row['アップロード日時']}）  \n"
                f"[ダウンロード]({row['パス']})"
            )
    else:
        st.info("まだファイルはアップロードされていません。")
