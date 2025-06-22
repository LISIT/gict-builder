
import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="GICT設営ビルダー", layout="wide")
st.title("📅 第24回 日本消化管CT技術学会 - 設営ビルダー")
st.markdown("🗓️ 開催予定日：**2026年6月20日（土）**｜会場：順天堂大学（仮）")

# 認証
st.subheader("🔒 ログイン認証")
password = st.text_input("パスコードを入力してください", type="password")
if password != "gict2026":
    st.warning("正しいパスコードを入力してください")
    st.stop()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file, category):
    filepath = os.path.join(UPLOAD_DIR, f"{category}__{uploaded_file.name}")
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"{uploaded_file.name} を保存しました。")
    return filepath

def list_uploaded_files(category):
    files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(f"{category}__")]
    return files

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "基本情報", "プログラム構成", "役割分担", "登録・抄録", "会場詳細", "議事録/アップロード"
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
    st.subheader("🕒 タイムテーブル構成")
    if "program_df" not in st.session_state:
        st.session_state["program_df"] = pd.DataFrame(columns=["時間", "セッション", "演者", "備考"])
    edited = st.data_editor(st.session_state["program_df"], num_rows="dynamic")
    st.session_state["program_df"] = edited

with tab3:
    st.subheader("👥 理事・評議員 役割分担")
    if "roles_df" not in st.session_state:
        st.session_state["roles_df"] = pd.DataFrame(columns=["氏名", "所属", "役割", "担当業務", "備考"])
    edited = st.data_editor(st.session_state["roles_df"], num_rows="dynamic")
    st.session_state["roles_df"] = edited

with tab4:
    st.subheader("📝 参加登録・抄録管理")
    password_policy = st.text_input("抄録集パスワード配布方法", "別途メール送信")
    participant_fee = st.number_input("当日会員参加費（円）", 0, 10000, 3000)
    sponsor = st.text_area("協賛企業・進捗", "例：ブラッコ・ジャパンより協賛予定")
    abstract_note = st.text_area("抄録管理の備考")

with tab5:
    st.subheader("🏛️ 会場使用依頼・設備")
    file1 = st.file_uploader("順天堂大学への依頼書（PDFなど）", type=["pdf", "docx"], key="venue_request")
    if file1:
        save_uploaded_file(file1, "venue_request")
    for f in list_uploaded_files("venue_request"):
        st.markdown(f"📄 [ダウンロード]({UPLOAD_DIR}/{f})")

    st.text_area("依頼書の補足説明", "例：2026年6月20日（土）講堂および展示ロビー使用希望")

    file2 = st.file_uploader("構内図/アクセスマップ（PDF/PNG/JPG）", type=["pdf", "jpg", "png"], key="campus_map")
    if file2:
        save_uploaded_file(file2, "campus_map")
    for f in list_uploaded_files("campus_map"):
        st.markdown(f"🗺️ [ダウンロード]({UPLOAD_DIR}/{f})")

    st.number_input("使用予定電源容量（W）", 0, 10000, 2000, step=100)
    st.text_area("電子機器構成", "例：プロジェクター2台、スイッチャー等")
    st.text_area("照明リクエスト", "例：ステージ強調ライト")
    st.number_input("展示ブース数", 0, 30, 5)
    st.number_input("ポスター用パネル数", 0, 100, 20)
    st.text_area("展示備品・配置", "例：長机5台、電源タップなど")

with tab6:
    st.subheader("📎 会議資料とToDoメモ")
    file3 = st.file_uploader("会議資料アップロード", type=["pdf", "xlsx", "docx"], key="meeting_file")
    if file3:
        save_uploaded_file(file3, "meeting_file")
    for f in list_uploaded_files("meeting_file"):
        st.markdown(f"📘 [ダウンロード]({UPLOAD_DIR}/{f})")

    st.text_area("共有メモ", "・第1回準備会議予定：2025年10月\n・備品リスト確認必要")

st.success("ファイルは保存されており、再読込後も表示されます。")

# ⬇️ データのエクスポート機能
import io

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

with tab1:
    st.download_button(
        "📥 基本情報CSV出力（ダミー）", 
        data="項目,値\n開催日,{}\n会場,{}\n大会長,{}\n副大会長,{}".format(date_input, location, chair, vice_chair).encode("utf-8"), 
        file_name="基本情報.csv",
        mime="text/csv"
    )

with tab2:
    csv = convert_df_to_csv(st.session_state["program_df"])
    st.download_button("📥 プログラム構成をCSVで保存", csv, "プログラム構成.csv", "text/csv")

with tab3:
    csv = convert_df_to_csv(st.session_state["roles_df"])
    st.download_button("📥 役割分担をCSVで保存", csv, "役割分担.csv", "text/csv")

with tab4:
    reg_data = pd.DataFrame({
        "抄録パスワード配布方法": [password_policy],
        "当日会員参加費": [participant_fee],
        "協賛企業進捗": [sponsor],
        "備考": [abstract_note]
    })
    csv = convert_df_to_csv(reg_data)
    st.download_button("📥 登録・抄録設定をCSVで保存", csv, "登録_抄録管理.csv", "text/csv")

with tab6:
    memo_data = pd.DataFrame({
        "共有メモ": [st.session_state.get("共有メモ", "・第1回準備会議予定：2025年10月\n・備品リスト確認必要")]
    })
    csv = convert_df_to_csv(memo_data)
    st.download_button("📥 議事録/メモをCSVで保存", csv, "議事録_メモ.csv", "text/csv")
