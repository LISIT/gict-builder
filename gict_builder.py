import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="GICT設営ビルダー", layout="wide")
st.title("📅 第24回 日本消化管CT技術学会 - 設営ビルダー")
st.markdown("🗓️ 開催予定日：**2026年6月20日（土）**｜会場：順天堂大学（仮）")

# パスワード認証（共通パスコード）
st.sidebar.title("🔒 ログイン認証")
password = st.sidebar.text_input("パスコードを入力してください", type="password")
if password != "gict2026":
    st.warning("正しいパスコードを入力してください")
    st.stop()

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
    st.file_uploader("順天堂大学への依頼書（PDFなど）", type=["pdf", "docx"])
    st.text_area("依頼書の補足説明", "例：2026年6月20日（土）講堂および展示ロビー使用希望")
    st.file_uploader("構内図/アクセスマップ（PDF/PNG/JPG）", type=["pdf", "jpg", "png"])
    st.number_input("使用予定電源容量（W）", 0, 10000, 2000, step=100)
    st.text_area("電子機器構成", "例：プロジェクター2台、スイッチャー等")
    st.text_area("照明リクエスト", "例：ステージ強調ライト")
    st.number_input("展示ブース数", 0, 30, 5)
    st.number_input("ポスター用パネル数", 0, 100, 20)
    st.text_area("展示備品・配置", "例：長机5台、電源タップなど")

with tab6:
    st.subheader("📎 会議資料とToDoメモ")
    st.file_uploader("会議資料アップロード", type=["pdf", "xlsx", "docx"])
    st.text_area("共有メモ", """・第1回準備会議予定：2025年10月
・備品リスト確認必要""")

st.success("情報は画面に保存されました。出力機能は今後実装予定です。")
