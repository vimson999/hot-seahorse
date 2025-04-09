import time
import os

# --- 全局配置 ---
# 选择模型大小: "tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3"
# 对于 faster-whisper 和 openai-whisper 保持一致以便比较
MODEL_SIZE = "base"

# 指定设备: "cpu", "cuda" (如果 CUDA 可用且已安装相应库)
# 对于 faster-whisper 和 openai-whisper 保持一致以便比较
DEVICE_TYPE = "cpu"

# 指定 faster-whisper 的计算类型 (对 openai-whisper 无效)
# GPU 通常用 "float16" 或 "int8_float16"
# CPU 通常用 "int8" 或 "float32"
COMPUTE_TYPE_CONFIG = "int8" if DEVICE_TYPE == "cpu" else "float16"

# !!! 修改为你自己的音频文件路径 !!!
AUDIO_FILE = "audio.mp3" # <--- 替换成你的音频文件路径

# 检查音频文件是否存在
if not os.path.exists(AUDIO_FILE):
    print(f"错误：音频文件 '{AUDIO_FILE}' 不存在。请修改脚本中的 AUDIO_FILE 变量。")
    exit()

# --- faster-whisper 测试函数 ---
def run_faster_whisper_test():
    print("\n" + "="*30)
    print("  Running faster-whisper Test")
    print("="*30)
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("错误：'faster_whisper' 库未安装。请运行 'pip install faster-whisper'")
        return

    print(f"配置: model='{MODEL_SIZE}', device='{DEVICE_TYPE}', compute_type='{COMPUTE_TYPE_CONFIG}'")
    print(f"音频文件: {AUDIO_FILE}")

    load_start_time = time.time()
    try:
        model = WhisperModel(MODEL_SIZE, device=DEVICE_TYPE, compute_type=COMPUTE_TYPE_CONFIG)
    except Exception as e:
        print(f"加载 faster-whisper 模型时出错: {e}")
        print("请确保模型名称正确，并且如果使用 GPU，已正确安装 CTranslate2 和 CUDA。")
        return
    load_end_time = time.time()
    print(f"模型加载时间: {load_end_time - load_start_time:.2f} 秒")

    print("开始转录...")
    transcribe_start_time = time.time()
    try:
        # beam_size, vad_filter 等参数可以按需调整
        segments, info = model.transcribe(AUDIO_FILE, beam_size=5) #, vad_filter=True)
    except Exception as e:
        print(f"使用 faster-whisper 转录时出错: {e}")
        return
    transcribe_end_time = time.time()
    transcription_time = transcribe_end_time - transcribe_start_time

    print(f"转录完成。纯转录时间: {transcription_time:.2f} 秒")
    print(f"检测到语言: '{info.language}' (概率: {info.language_probability:.2f})")
    print(f"转录音频时长 (VAD后或原始): {info.duration_after_vad if info.duration_after_vad else info.duration:.2f} 秒")

    print("\n--- 转录结果 (faster-whisper) ---")
    full_transcript = []
    # segments 是生成器，需要迭代取出
    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        full_transcript.append(segment.text.strip())
    print("\n完整文本:")
    print(" ".join(full_transcript))
    print("--- faster-whisper 测试结束 ---")

# --- openai-whisper 测试函数 ---
def run_openai_whisper_test():
    print("\n" + "="*30)
    print("  Running openai-whisper Test")
    print("="*30)
    try:
        import whisper
    except ImportError:
        print("错误：'openai-whisper' 库未安装。请运行 'pip install -U openai-whisper'")
        return

    print(f"配置: model='{MODEL_SIZE}', device='{DEVICE_TYPE}'")
    print(f"音频文件: {AUDIO_FILE}")

    load_start_time = time.time()
    try:
        model = whisper.load_model(MODEL_SIZE, device=DEVICE_TYPE)
    except Exception as e:
        print(f"加载 openai-whisper 模型时出错: {e}")
        print("请确保模型名称正确，并且如果使用 GPU，已正确安装 PyTorch 和 CUDA。")
        return
    load_end_time = time.time()
    print(f"模型加载时间: {load_end_time - load_start_time:.2f} 秒")

    print("开始转录...")
    transcribe_start_time = time.time()
    try:
        # 可以添加其他参数，如 language='zh'
        result = model.transcribe(AUDIO_FILE)
    except Exception as e:
        print(f"使用 openai-whisper 转录时出错: {e}")
        return
    transcribe_end_time = time.time()
    transcription_time = transcribe_end_time - transcribe_start_time

    print(f"转录完成。纯转录时间: {transcription_time:.2f} 秒")
    print(f"检测到语言: {result['language']}")

    print("\n--- 转录结果 (openai-whisper) ---")
    print("Segments:")
    if 'segments' in result:
        for segment in result["segments"]:
             print(f"[{segment['start']:.2f}s -> {segment['end']:.2f}s] {segment['text']}")
    else:
        print("未找到 Segments 信息。")

    print("\n完整文本:")
    print(result.get("text", "未能提取完整文本。"))
    print("--- openai-whisper 测试结束 ---")

# --- 主程序入口 ---
if __name__ == "__main__":
    print("开始 Whisper 库比较测试...")
    print(f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 运行 faster-whisper 测试
    run_faster_whisper_test()

    # 运行 openai-whisper 测试
    run_openai_whisper_test()

    print("\n所有测试完成。")