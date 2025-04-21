# import yt_dlp
# import json
# from typing import Dict, Any # Optional: for type hints

# # 快手分享链接
# video_url = 'https://www.kuaishou.com/f/X4ELfTRWm7fZ1xx'

# # yt-dlp 选项
# ydl_opts = {
#     'quiet': True,
#     'no_warnings': True,
#     # 'verbose': True, # 如果遇到问题，可以取消注释此行查看详细日志
#     # 'dump_single_json': True, # 也可以用这个选项直接获取 JSON，但 extract_info 更灵活
#     # 'cookiefile': 'path/to/your/cookies.txt', # 如果遇到需要登录才能看的内容，可能需要提供 cookies 文件
# }

# print(f"尝试提取信息: {video_url}")

# try:
#     # 创建 YoutubeDL 对象
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         # 使用 extract_info 获取信息 (不下载)
#         info_dict = ydl.extract_info(video_url, download=False)

#         # 打印获取到的信息 (JSON 格式)
#         print("\n--- 提取到的信息 ---")
#         print(json.dumps(info_dict, indent=4, ensure_ascii=False))

#         # 你也可以尝试在这里调用之前的转换函数（如果字段大致匹配）
#         # standard_format_info = convert_tiktok_info_to_standard_format(info_dict) # 注意：字段名可能需要调整
#         # print("\n--- 尝试转换为标准格式 ---")
#         # print(json.dumps(standard_format_info, indent=4, ensure_ascii=False))


# except yt_dlp.utils.DownloadError as e:
#     print(f"\n提取信息时出错 (DownloadError): {e}")
#     print("这可能是因为视频不存在、需要登录、地区限制或网络问题。")
# except Exception as e:
#     print(f"\n发生未知错误: {e}")


import yt_dlp
import json
import re
from typing import Dict, Any, List
import time

# --- (假设 MediaType 和 extract_hashtags 函数已定义，同上) ---
class MediaType:
    VIDEO = "video"
    IMAGE = "image"
    UNKNOWN = "unknown"

def extract_hashtags(text: str) -> List[str]:
    if not text: return []
    return re.findall(r"#([^\s#]+)", text)

def convert_generic_info_to_standard_format(info_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    将 yt-dlp 'generic' 提取器的有限信息尝试转换为标准格式。
    结果会很不完整。
    """
    try:
        # 尝试从 webpage_url_basename 或 id 中提取干净的 ID
        note_id_raw = info_dict.get('webpage_url_basename', info_dict.get('id', ''))
        # 提取 ID 部分 (假设 ID 在查询参数 '?' 之前)
        note_id = note_id_raw.split('?')[0] if note_id_raw else ''

        # 因为是 generic 提取器，很多信息都没有
        media_info = {
            "cover_url": info_dict.get('thumbnail'), # 通常为 None
            "type": MediaType.UNKNOWN, # 无法确定类型
            "video_url": None, # 没有提取到视频 URL
            "duration": 0,
            "width": 0,
            "height": 0
        }

        statistics = {
            "like_count": 0,
            "comment_count": 0,
            "share_count": 0,
            "collected_count": 0,
            "view_count": 0
        }

        author = {
            "id": "",
            "nickname": "",
            "avatar": "",
            "signature": "",
            "verified": False,
            "follower_count": 0,
            "following_count": 0,
            "notes_count": 0,
            "location": ""
        }

        # 尝试从 title (如果它包含文本而非ID) 或 desc (如果存在) 提取 tags
        # 在这个例子中，title 只是 ID，所以 tags 很可能为空
        title_text = info_dict.get('title', '')
        # 如果 title 看起来像 ID，可能不适合提取标签
        tags = extract_hashtags(title_text) if title_text != note_id else []


        result = {
            "note_id": note_id,
            "title": "" if title_text == note_id else title_text, # 如果 title 只是 ID，则设为空
            "desc": info_dict.get('description', ''), # 通常为空
            "type": MediaType.UNKNOWN, # 无法确认
            "author": author,
            "statistics": statistics,
            "tags": tags,
            "media": media_info,
            "images": [],
            "original_url": info_dict.get('original_url', info_dict.get('webpage_url', '')),
            "create_time": info_dict.get('timestamp', info_dict.get('epoch')), # 可能为 None 或只有 epoch
            "last_update_time": info_dict.get('timestamp', info_dict.get('epoch'))
        }

        return result

    except Exception as e:
        print(f"转换 Generic 信息时发生错误: {e}")
        return {
            "note_id": info_dict.get('id', '').split('?')[0] if info_dict.get('id') else '',
            "title": "",
            "desc": "",
            "type": MediaType.UNKNOWN,
            "author": {},
            "statistics": {},
            "tags": [],
            "media": {},
            "images": [],
            "original_url": info_dict.get('original_url', info_dict.get('webpage_url', '')),
            "create_time": None,
            "last_update_time": None
        }

# --- 主程序部分 (使用你提供的 JSON 数据作为示例输入) ---
if __name__ == "__main__":
    # 使用你提供的 JSON 输出作为输入数据
    raw_info_dict = {
        "id": "3xhjfv22y5n5ccq?cc=share_copylink&kpf=PC_WEB&utm_campaign=pc_share&shareMethod=token&utm_medium=pc_share&kpn=KUAISHOU_VISION&subBiz=SINGLE_ROW_WEB&ztDid=web_171ce65d7b49fe4881bacf72a47d4590&shareId=18367120396075&shareToken=X4ELfTRWm7fZ1xx&shareMode=app&efid=0&shareObjectId=3xhjfv22y5n5ccq&utm_source=pc_share",
        "title": "3xhjfv22y5n5ccq", # 注意：这里的 title 只是 ID
        "timestamp": None,
        "direct": True,
        "url": "https://www.kuaishou.com/short-video/3xhjfv22y5n5ccq?cc=share_copylink&kpf=PC_WEB&utm_campaign=pc_share&shareMethod=token&utm_medium=pc_share&kpn=KUAISHOU_VISION&subBiz=SINGLE_ROW_WEB&ztDid=web_171ce65d7b49fe4881bacf72a47d4590&shareId=18367120396075&shareToken=X4ELfTRWm7fZ1xx&shareMode=app&efid=0&shareObjectId=3xhjfv22y5n5ccq&utm_source=pc_share",
        "ext": "unknown_video",
        "original_url": "https://www.kuaishou.com/f/X4ELfTRWm7fZ1xx",
        "webpage_url": "https://www.kuaishou.com/short-video/3xhjfv22y5n5ccq?cc=share_copylink&kpf=PC_WEB&utm_campaign=pc_share&shareMethod=token&utm_medium=pc_share&kpn=KUAISHOU_VISION&subBiz=SINGLE_ROW_WEB&ztDid=web_171ce65d7b49fe4881bacf72a47d4590&shareId=18367120396075&shareToken=X4ELfTRWm7fZ1xx&shareMode=app&efid=0&shareObjectId=3xhjfv22y5n5ccq&utm_source=pc_share",
        "webpage_url_basename": "3xhjfv22y5n5ccq", # 这个是干净的 ID
        "webpage_url_domain": "kuaishou.com",
        "extractor": "generic", # <--- 问题关键
        "extractor_key": "Generic",
        "playlist": None,
        "playlist_index": None,
        "display_id": "3xhjfv22y5n5ccq?cc=share_copylink&kpf=PC_WEB&utm_campaign=pc_share&shareMethod=token&utm_medium=pc_share&kpn=KUAISHOU_VISION&subBiz=SINGLE_ROW_WEB&ztDid=web_171ce65d7b49fe4881bacf72a47d4590&shareId=18367120396075&shareToken=X4ELfTRWm7fZ1xx&shareMode=app&efid=0&shareObjectId=3xhjfv22y5n5ccq&utm_source=pc_share",
        "fulltitle": "3xhjfv22y5n5ccq",
        "release_year": None,
        "requested_subtitles": None,
        "_has_drm": None,
        "protocol": "https",
        "video_ext": "unknown_video",
        "audio_ext": "none",
        "vbr": None,
        "abr": None,
        "tbr": None,
        "resolution": None,
        "dynamic_range": "SDR",
        "aspect_ratio": None,
        "filesize_approx": None,
        "cookies": "kpf=PC_WEB; Domain=.www.kuaishou.com; Path=/; Expires=1776780760; kpn=KUAISHOU_VISION; Domain=.www.kuaishou.com; Path=/; Expires=1776780760; clientid=3; Domain=.www.kuaishou.com; Path=/; Expires=1776780760; did=web_6af9df8428570cc4a7c0c8bf3020cd3c; Domain=.kuaishou.com; Path=/; Expires=1776780760",
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
        },
        "format_id": "0",
        "format": "0 - unknown",
        "epoch": 1745244760 # 这个 epoch 可能是提取网页的时间，不是视频发布时间
    }

    print("原始信息有限，尝试转换为标准格式...")
    standard_format_info = convert_generic_info_to_standard_format(raw_info_dict)

    print("\n--- 标准格式输出 (数据缺失较多) ---")
    print(json.dumps(standard_format_info, indent=4, ensure_ascii=False))

    print("\n--- 问题诊断 ---")
    print("注意: yt-dlp 使用了 'generic' 提取器，未能识别快手视频页面。")
    print("这导致缺少视频标题、作者、时长、统计数据、媒体 URL 等关键信息。")
    print("可能原因：快手网站更新、内容限制 (地区/登录)、反爬虫或 yt-dlp 版本过旧。")
    print("建议尝试：")
    print("1. 更新 yt-dlp: pip install -U yt-dlp")
    print("2. 检查网络或使用代理/VPN (如果怀疑地区限制)")
    print("3. 提供 cookies 文件 (如果怀疑需要登录): 在 ydl_opts 中设置 'cookiefile': 'path/to/cookies.txt'")
    print("4. 查看 yt-dlp 的 GitHub Issues 是否有关于快手提取器问题的报告。")