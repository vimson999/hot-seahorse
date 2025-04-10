# server_whisper_test.py
import time
import os
import gc
import platform
import numpy as np
import torch

# --- 通过环境变量配置 ---
# 读取环境变量，提供默认值
MODEL_SIZE = os.environ.get("WHISPER_MODEL", "base") # 可选: tiny, base, small, medium, large-v3 等
# 允许强制指定设备，否则自动检测
_forced_device = os.environ.get("WHISPER_DEVICE")
if _forced_device and _forced_device in ["cpu", "cuda"]:
    DEVICE_TYPE = _forced_device
    print(f"[配置] 使用环境变量强制指定设备: {DEVICE_TYPE}")
else:
    DEVICE_TYPE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[配置] 自动检测到设备: {DEVICE_TYPE}")

# CPU 计算类型: 默认 int8 (服务器追求性能)，如果出问题可改为 float32
DEFAULT_CPU_COMPUTE = "int8"
CPU_COMPUTE_TYPE_OVERRIDE = os.environ.get("WHISPER_CPU_COMPUTE_TYPE")
# GPU 计算类型: 默认 float16
DEFAULT_GPU_COMPUTE = "float16"
GPU_COMPUTE_TYPE_OVERRIDE = os.environ.get("WHISPER_GPU_COMPUTE_TYPE")

if DEVICE_TYPE == "cpu":
    COMPUTE_TYPE_CONFIG = CPU_COMPUTE_TYPE_OVERRIDE or DEFAULT_CPU_COMPUTE
else: # cuda
    COMPUTE_TYPE_CONFIG = GPU_COMPUTE_TYPE_OVERRIDE or DEFAULT_GPU_COMPUTE
print(f"[配置] Faster-Whisper 计算类型: {COMPUTE_TYPE_CONFIG}")

# faster-whisper CPU 线程数: 默认核心数一半，最小为 1，可通过环境变量覆盖
DEFAULT_CPU_THREADS = max(1, (os.cpu_count() or 4) // 2)
try:
    # 读取环境变量并转换为整数
    _env_cpu_threads = os.environ.get("WHISPER_CPU_THREADS")
    CPU_THREADS_CONFIG = int(_env_cpu_threads) if _env_cpu_threads else DEFAULT_CPU_THREADS
    # 确保线程数至少为 1
    if CPU_THREADS_CONFIG <= 0: CPU_THREADS_CONFIG = DEFAULT_CPU_THREADS
except (ValueError, TypeError):
    print(f"[配置警告] WHISPER_CPU_THREADS 环境变量值 '{_env_cpu_threads}' 无效，使用默认值 {DEFAULT_CPU_THREADS}")
    CPU_THREADS_CONFIG = DEFAULT_CPU_THREADS
if DEVICE_TYPE == 'cpu':
    print(f"[配置] Faster-Whisper CPU 线程数 (WHISPER_CPU_THREADS): {CPU_THREADS_CONFIG}")


# 音频文件路径: 优先从环境变量读取，否则使用默认，如果最终文件不存在则报错退出
AUDIO_FILE = os.environ.get("WHISPER_AUDIO_FILE", "audio.mp3")
print(f"[配置] 使用音频文件 (WHISPER_AUDIO_FILE): {AUDIO_FILE}")
if not os.path.exists(AUDIO_FILE):
    print(f"错误：音频文件 '{AUDIO_FILE}' 不存在。请通过 WHISPER_AUDIO_FILE 环境变量指定有效路径，或确保 audio.mp3 在脚本运行目录。")
    exit(1) # 错误退出

# --- faster-whisper 测试函数 ---
def run_faster_whisper_test():
    print("\n" + "="*30)
    print("  Running faster-whisper Test")
    print("="*30)
    model = None
    segments = None
    info = None
    full_transcript_list = None
    full_text = "[未开始处理]"
    language = ""
    duration = 0.0
    language_probability = None

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("错误：'faster_whisper' 未安装。请运行 'pip install faster-whisper'")
        return False # 返回失败

    # 使用从环境变量或默认值确定的配置
    print(f"配置: model='{MODEL_SIZE}', device='{DEVICE_TYPE}', compute_type='{COMPUTE_TYPE_CONFIG}'")

    load_start_time = time.time()
    try:
        model_kwargs = {
            "device": DEVICE_TYPE,
            "compute_type": COMPUTE_TYPE_CONFIG,
        }
        if DEVICE_TYPE == "cpu":
            model_kwargs["cpu_threads"] = CPU_THREADS_CONFIG
            print(f"       (使用 cpu_threads: {CPU_THREADS_CONFIG})")

        model = WhisperModel(MODEL_SIZE, **model_kwargs)
    except Exception as e:
        print(f"加载 faster-whisper 模型 '{MODEL_SIZE}' 时出错: {e}")
        return False # 返回失败
    load_end_time = time.time()
    print(f"模型加载时间: {load_end_time - load_start_time:.2f} 秒")

    print("开始转录并获取完整文案...")
    overall_start_time = time.time()
    full_transcript_list = []
    try:
        segments, info = model.transcribe(AUDIO_FILE, beam_size=5, language="zh", task="transcribe", word_timestamps=False)
        for segment in segments:
            full_transcript_list.append(segment.text.strip())
        full_text = " ".join(full_transcript_list)
        if info:
            language = info.language
            duration = info.duration
            if hasattr(info, 'language_probability'): language_probability = info.language_probability
    except Exception as e:
        print(f"使用 faster-whisper 转录或处理时出错: {e}")
        full_text = "[转录或处理出错]"
        if info is None and 'info' in locals(): info = locals()['info']
        if info:
            language = info.language; duration = info.duration
            if hasattr(info, 'language_probability'): language_probability = info.language_probability
    finally:
        overall_end_time = time.time()
        overall_time = overall_end_time - overall_start_time
        print(f"获取完整文案总耗时: {overall_time:.2f} 秒")

    prob_output = 'N/A'
    if language_probability is not None:
        if isinstance(language_probability, (float, int)):
             try: prob_output = f"{float(language_probability):.2f}"
             except (ValueError, TypeError): prob_output = str(language_probability)
        else: prob_output = str(language_probability)

    if language: print(f"检测到语言: '{language}' (faster-whisper 报告概率: {prob_output})")
    if duration > 0: print(f"转录音频时长 (由 faster-whisper 报告): {duration:.2f} 秒")
    if not language and not duration > 0: print("未能获取语言和时长信息。")

    print("\n--- 完整文案 (faster-whisper) ---")
    print(full_text)
    print("--- faster-whisper 测试结束 ---")

    del model, segments, info, full_transcript_list, full_text, language, language_probability
    if torch.cuda.is_available(): torch.cuda.empty_cache()
    gc.collect()
    return True # 返回成功

# --- openai-whisper 测试函数 ---
def run_openai_whisper_test():
    print("\n" + "="*30)
    print("  Running openai-whisper Test")
    print("="*30)
    model = None
    result = None
    full_text = "[未开始处理]"
    language = ""
    try:
        import whisper
    except ImportError:
        print("错误：'openai-whisper' 未安装。")
        return False

    print(f"配置: model='{MODEL_SIZE}', device='{DEVICE_TYPE}'")
    print(f"音频文件: {AUDIO_FILE}")

    load_start_time = time.time()
    try:
        model = whisper.load_model(MODEL_SIZE, device=DEVICE_TYPE)
    except Exception as e:
        print(f"加载 openai-whisper 模型时出错: {e}")
        return False
    load_end_time = time.time()
    print(f"模型加载时间: {load_end_time - load_start_time:.2f} 秒")

    print("开始转录并获取完整文案...")
    overall_start_time = time.time()
    try:
        result = model.transcribe(AUDIO_FILE, language="zh")
        full_text = result.get("text", "").strip()
        language = result.get("language", "")
    except Exception as e:
        print(f"使用 openai-whisper 转录时出错: {e}")
        full_text = "[转录出错]"
    finally:
        overall_end_time = time.time()
        overall_time = overall_end_time - overall_start_time
        print(f"获取完整文案总耗时: {overall_time:.2f} 秒")

    if language: print(f"检测到语言: {language}")
    else:
         if result and 'language' in result: print(f"检测到语言: {result['language']}")
         else: print("未能检测到语言。")

    print("\n--- 完整文案 (openai-whisper) ---")
    print(full_text)
    print("--- openai-whisper 测试结束 ---")

    del model, result, full_text, language
    if torch.cuda.is_available(): torch.cuda.empty_cache()
    gc.collect()
    return True

# --- 主程序入口 ---
if __name__ == "__main__":
    print("开始 Whisper 库比较测试 (目标：最快获取完整文案 - faster-whisper vs openai-whisper)...")
    print(f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}") # 显示脚本运行时的本地时间及时区
    print(f"测试机器平台: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"CPU 核心数 (逻辑): {os.cpu_count()}")
    print("-" * 20) # 分隔符

    # 打印最终生效的配置
    print("--- 使用的配置 ---")
    print(f"  模型大小 (WHISPER_MODEL): {MODEL_SIZE}")
    print(f"  音频文件 (WHISPER_AUDIO_FILE): {AUDIO_FILE}")
    print(f"  目标设备 (WHISPER_DEVICE or auto): {DEVICE_TYPE}")
    print(f"  Faster-Whisper 计算类型: {COMPUTE_TYPE_CONFIG}")
    if DEVICE_TYPE == 'cpu':
        print(f"  Faster-Whisper CPU 线程数 (WHISPER_CPU_THREADS): {CPU_THREADS_CONFIG}")
    print("-" * 20 + "\n")

    print("提示：如果遇到稳定性问题 (崩溃/卡死)，尤其是在 Linux/macOS 上，")
    print("      请尝试在运行此脚本前设置 OMP 环境变量，例如:")
    print("      export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1\n")

    start_all = time.time()
    faster_success = False
    openai_success = False

    # 运行 faster-whisper 测试
    faster_success = run_faster_whisper_test()
    gc.collect()

    # 运行 openai-whisper 测试
    openai_success = run_openai_whisper_test()
    gc.collect()

    end_all = time.time()
    print("\n" + "="*40)
    print("所有测试完成。")
    print(f"总测试耗时: {end_all - start_all:.2f} 秒")
    print(f"Faster-Whisper 测试: {'成功' if faster_success else '失败'}")
    print(f"OpenAI-Whisper 测试: {'成功' if openai_success else '失败'}")
    print("="*40)