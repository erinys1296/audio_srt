import streamlit as st
import whisper
import os
from datetime import timedelta

# 設定 Streamlit 頁面
st.title("🎙️ Whisper 語音轉錄應用")
st.write("上傳音檔，Whisper 會轉錄文字並產生 SRT 字幕！")

# 上傳音檔
uploaded_file = st.file_uploader("請上傳音檔（MP3, WAV, MP4, M4A, FLAC）", type=["mp3", "wav", "mp4", "m4a", "flac"])

if uploaded_file is not None:
    # 儲存音檔
    audio_path = f"temp_audio.{uploaded_file.name.split('.')[-1]}"
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.read())

    # 加載 Whisper 模型
    st.write("🔄 轉錄中，請稍等...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    # 顯示轉錄結果
    st.subheader("📝 轉錄文字：")
    st.write(result["text"])

    # 產生 SRT 字幕
    srt_content = ""
    for i, segment in enumerate(result["segments"]):
        start = str(timedelta(seconds=int(segment["start"])))
        end = str(timedelta(seconds=int(segment["end"])))
        srt_content += f"{i+1}\n{start} --> {end}\n{segment['text']}\n\n"

    # 儲存 SRT 檔案
    srt_path = "transcription.srt"
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        srt_file.write(srt_content)

    # 提供下載 SRT 文件
    st.subheader("📥 下載 SRT 字幕檔")
    with open(srt_path, "rb") as file:
        st.download_button("下載 SRT", file, file_name="transcription.srt", mime="text/plain")

    # 刪除暫存檔案
    os.remove(audio_path)
    os.remove(srt_path)