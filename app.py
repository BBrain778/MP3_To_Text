import os, tempfile
from datetime import timedelta
import streamlit as st
from faster_whisper import WhisperModel

# ---- 基本設定 ----
MODEL_SIZE = os.environ.get("WHISPER_MODEL", "small")  # 可改 "base"/"tiny"/"medium"/"large-v3"
DEVICE = os.environ.get("WHISPER_DEVICE", "cpu")       # 有 NVIDIA 可設 "cuda"
COMPUTE = os.environ.get("WHISPER_COMPUTE", "int8")    # 有 NVIDIA 可設 "float16"

@st.cache_resource
def load_model(size, device, compute):
    return WhisperModel(size, device=device, compute_type=compute)

def fmt_ts(sec: float) -> str:
    ms = int((sec - int(sec)) * 1000)
    hh = int(sec) // 3600
    mm = (int(sec) % 3600) // 60
    ss = int(sec) % 60
    return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"

def seg_to_text_srt(segments):
    lines, srt_lines = [], []
    for i, seg in enumerate(segments, 1):
        text = seg.text.strip()
        lines.append(text)
        srt_lines.append(str(i))
        srt_lines.append(f"{fmt_ts(seg.start)} --> {fmt_ts(seg.end)}")
        srt_lines.append(text)
        srt_lines.append("")
    return "\n".join(lines).strip(), "\n".join(srt_lines).strip()

st.set_page_config(page_title="本機 MP3 語音轉文字 (Whisper)", layout="centered")
st.title("本機 MP3 語音轉文字（Whisper）")

with st.sidebar:
    st.markdown("### 轉寫設定")
    model_size = st.selectbox("模型大小", ["tiny","base","small","medium","large-v3"], index=["tiny","base","small","medium","large-v3"].index(MODEL_SIZE if MODEL_SIZE in ["tiny","base","small","medium","large-v3"] else "small"))
    lang = st.selectbox("語言（auto=自動偵測）", ["auto","zh","en","ja","ko","de","fr","es","ru","it","pt","vi"], index=0)
    beam_size = st.slider("Beam size（越大越準但越慢）", 1, 10, 5)
    enable_vad = st.checkbox("啟用 VAD（過濾靜音/噪音）", True)

model = load_model(model_size, DEVICE, COMPUTE)

up = st.file_uploader("上傳音訊（MP3/WAV/M4A/MP4…）", type=["mp3","wav","m4a","mp4","aac","flac","ogg"])
if up is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{up.name}") as tf:
        tf.write(up.getbuffer())
        audio_path = tf.name

    st.info("開始轉寫中…首次執行可能會下載/載入模型，請耐心等候。")
    language = None if lang == "auto" else lang
    segments, info = model.transcribe(audio_path, language=language, beam_size=beam_size, vad_filter=enable_vad)
    segs = list(segments)
    full_text, srt_text = seg_to_text_srt(segs)

    st.success(f"完成！偵測語言：{info.language}（prob={info.language_probability:.2f}）" if language is None else f"完成！語言固定為：{language}")

    st.subheader("轉換結果（純文字）")
    st.text_area("Text", full_text, height=250)

    # 下載檔
    base = os.path.splitext(os.path.basename(up.name))[0]
    txt_bytes = full_text.encode("utf-8")
    srt_bytes = srt_text.encode("utf-8")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("下載 TXT", data=txt_bytes, file_name=f"{base}.txt", mime="text/plain")
    with col2:
        st.download_button("下載 SRT", data=srt_bytes, file_name=f"{base}.srt", mime="application/x-subrip")

    # 清理暫存
    try:
        os.remove(audio_path)
    except Exception:
        pass
