# import yt_dlp
# import json

# # 这个 URL 格式不正确，很可能无法被 yt-dlp 处理
# video_url = 'https://www.youtube.com/watch?v=3B8Zy_jq3MA'

# ydl_opts = {
#     'quiet': True,
#     'no_warnings': True,
# }

# print(f"尝试提取信息: {video_url}")

# try:
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(video_url, download=False)
#         print("\n--- 提取到的信息 ---")
#         print(json.dumps(info_dict, indent=4, ensure_ascii=False))

# except yt_dlp.utils.DownloadError as e:
#     print(f"\n提取信息时出错 (DownloadError): {e}")
#     # 预期的错误输出会类似下面这样：
#     # ERROR: [generic] Unsupported URL: https://www.youtube.com/watch?v=3B8Zy_jq3MA这个版本的
#     print("错误信息表明该 URL 不被支持。请检查 URL 是否正确。")
# except Exception as e:
#     print(f"\n发生未知错误: {e}")



import yt_dlp
import json
import re
from typing import Dict, Any, List
import time # Although not strictly needed for conversion with epoch time available

# --- Assume MediaType and extract_hashtags are defined as before ---
class MediaType:
    VIDEO = "video"
    IMAGE = "image"
    UNKNOWN = "unknown"

def extract_hashtags(text: str) -> List[str]:
    """Extracts hashtags (#tag) from a string."""
    if not text:
        return []
    # Adjust regex if needed for different tag formats
    hashtags = re.findall(r"#([\w\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uff10-\uff19\uff21-\uff3a\uff41-\uff5a]+)", text)
    return hashtags

# --- Conversion Function (Adapted for YouTube fields) ---
def convert_youtube_info_to_standard_format(info_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts raw yt-dlp YouTube video info to a standard format.

    Args:
        info_dict: From yt-dlp containing YouTube video data.

    Returns:
        Dict[str, Any]: Standard format data.
    """
    try:
        # --- Media Info ---
        # Note: yt-dlp often selects separate video/audio streams for best quality ('format_id' like '616+251')
        # Getting a single direct URL for the combined best format can be tricky.
        # We'll prioritize metadata over a single playable URL here.
        # If a combined format like '22' (720p mp4) or '18' (360p mp4) exists in the full 'formats' list,
        # its URL could be used. Otherwise, video_url might remain None or point to a manifest.
        direct_video_url = None # Placeholder
        # Example: Look for a common MP4 format like 22 or 18 in the full formats list (not shown in user input snippet)
        # for fmt in info_dict.get('formats', []):
        #     if fmt.get('format_id') == '22' or fmt.get('format_id') == '18':
        #          if fmt.get('url'):
        #             direct_video_url = fmt['url']
        #             break

        media_info = {
            "cover_url": info_dict.get('thumbnail'), # Top-level thumbnail
            "type": MediaType.VIDEO,
            "video_url": direct_video_url, # May be None if only separate streams found
            "duration": int(info_dict.get('duration', 0) or 0),
            "width": int(info_dict.get('width', 0) or 0), # Width from best selected format
            "height": int(info_dict.get('height', 0) or 0) # Height from best selected format
        }

        # --- Statistics ---
        statistics = {
            "like_count": int(info_dict.get('like_count', 0) or 0),
            "comment_count": int(info_dict.get('comment_count', 0) or 0),
            "share_count": 0, # Not directly available via yt-dlp for YouTube
            "collected_count": 0, # Not applicable/available
            "view_count": int(info_dict.get('view_count', 0) or 0)
        }

        # --- Author Info ---
        author = {
            "id": info_dict.get('channel_id'), # Use channel_id if available
            "nickname": info_dict.get('uploader', info_dict.get('channel','')), # Uploader or channel name
            "avatar": "", # Usually no separate author avatar URL easily available
            "signature": "",
            "verified": info_dict.get('channel_is_verified', False),
            "follower_count": int(info_dict.get('channel_follower_count', 0) or 0),
            "following_count": 0,
            "notes_count": 0, # Not applicable to YouTube channels
            "location": ""
        }
        # Fallback for author ID if channel_id is missing
        if not author["id"]:
             author["id"] = info_dict.get('uploader_id','')

        # --- Tags ---
        # Use 'tags' list directly if present, otherwise try extracting from description/title
        tags = info_dict.get('tags')
        if tags is None: # Check if None explicitly
             description_text = info_dict.get('description', '')
             title_text = info_dict.get('title', '')
             combined_text_for_tags = f"{title_text} {description_text}"
             tags = extract_hashtags(combined_text_for_tags)
        elif not isinstance(tags, list): # Ensure it's a list
             tags = []


        # --- Construct Final Result ---
        result = {
            "note_id": info_dict.get('id', ''), # YouTube video ID (e.g., 3B8Zy_jq3MA)
            "title": info_dict.get('title', ''),
            "desc": info_dict.get('description', ''),
            "type": MediaType.VIDEO,
            "author": author,
            "statistics": statistics,
            "tags": tags, # Use the extracted list
            "media": media_info,
            "images": [], # It's a video
            "original_url": info_dict.get('original_url', info_dict.get('webpage_url', '')),
            "create_time": info_dict.get('timestamp'), # Use epoch timestamp directly
            "last_update_time": info_dict.get('timestamp') # YouTube doesn't provide separate update time via yt-dlp
        }
        # Ensure create_time is int or None
        if result["create_time"] is not None:
            result["create_time"] = int(result["create_time"])
        if result["last_update_time"] is not None:
            result["last_update_time"] = int(result["last_update_time"])


        return result

    except Exception as e:
        print(f"转换 YouTube 视频信息时发生错误: {e}")
        # Provide a minimal fallback
        return {
            "note_id": info_dict.get('id', ''),
            "title": info_dict.get('title', ''),
            "desc": info_dict.get('description', ''),
            "type": MediaType.UNKNOWN,
            "author": {"id": info_dict.get('channel_id', info_dict.get('uploader_id','')), "nickname": info_dict.get('uploader', '')},
            "statistics": {},
            "tags": [],
            "media": {},
            "images": [],
            "original_url": info_dict.get('original_url', info_dict.get('webpage_url', '')),
            "create_time": None,
            "last_update_time": None
        }

# --- Main Execution ---
if __name__ == "__main__":
    # Use the JSON data you provided as input
    raw_info_dict = {
        "id": "3B8Zy_jq3MA",
        "title": "I Asked AI To Make Me As Much Money As Possible",
        "formats": [], # Simplified for brevity, full list not needed for conversion logic shown
        "thumbnails": [ {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ9", "id": "0"} ], # Example thumbnail
        "thumbnail": "https://www.youtube.com/watch?v=dQw4w9WgXcQ9", # Example top-level thumbnail
        "description": "Want to make money with AI? I asked ChatGPT, Claude & Gemini to make me AS MUCH money as possible with $100.\n\nHere's what happened...\n\nThis is NOT financial advice. \n\nFREE NEWSLETTER: Get my frameworks for buying businesses, building wealth, and thinking bigger -> https://contrarianthinking.co\n\nMY COURSES: Want to buy a business? Learn how → https://codie-sanchez.com/yt/courses.html\n\nLISTEN TO MY PODCASTS:\n► The Contrarian Thinking Podcast: https://contrarianthinking.co/podcast\n► The Unconventional Acquisitions Podcast: https://podcasts.apple.com/us/podcast/the-unconventional-acquisitions-podcast/id1664 unconventionalacquisitions\n\nCOME SAY HI:\n► Twitter: https://twitter.com/Codie_Sanchez\n► Instagram: https://www.instagram.com/codiesanchez\n\n#ai #makemoney #chatgpt",
        "channel_id": "UCXJs-_M3FSts0G6q4gAJc_Q",
        "channel_url": "https://youtu.be/dQw4w9WgXcQ0",
        "duration": 699.156,
        "view_count": 316968,
        # ... (rest of the 'automatic_captions' and 'heatmap' data omitted for clarity) ...
        "automatic_captions": {
             # Data omitted, but present in original
        },
         "subtitles": {},
        "comment_count": 794,
        "chapters": None,
        "heatmap": [
            # Data omitted, but present in original
        ],
        "like_count": 15408,
        "channel": "Codie Sanchez",
        "channel_follower_count": 1750000,
        "channel_is_verified": True,
        "uploader": "Codie Sanchez",
        "uploader_id": "@CodieSanchezCT",
        "uploader_url": "https://www.youtube.com/@CodieSanchezCT",
        "upload_date": "20250228",
        "timestamp": 1740758405,
        "availability": "public",
        "original_url": "https://www.youtube.com/watch?v=3B8Zy_jq3MA", # The URL initially queried
        "webpage_url": "https://www.youtube.com/watch?v=VIDEO_ID", # Resolved video URL
        "webpage_url_basename": "watch",
        "webpage_url_domain": "youtube.com",
        "extractor": "youtube",
        "extractor_key": "Youtube",
        "playlist": None,
        "playlist_index": None,
        "display_id": "3B8Zy_jq3MA",
        "fulltitle": "I Asked AI To Make Me As Much Money As Possible",
        "duration_string": "11:39",
        "release_year": None,
        "is_live": False,
        "was_live": False,
        "requested_subtitles": None,
        "_has_drm": None,
        "epoch": 1745245109, # Time when yt-dlp ran
        "requested_formats": [ # Example format info
             { "format_id": "616", "width": 1920, "height": 1080, "vcodec": "vp09...", "acodec": "none"},
             { "format_id": "251", "width": None, "height": None, "vcodec": "none", "acodec": "opus", "url": "https://rr4---sn-ogul7n7z.googlevideo.com/..."}
         ],
        "format": "616 - 1920x1080 (Premium)+251 - audio only (medium)", # Combined format info
        "format_id": "616+251",
        "width": 1920, # From selected video format
        "height": 1080, # From selected video format
        "fps": 24.0,
        "vcodec": "vp09.00.40.08",
        "acodec": "opus",
        "abr": 122.571,
        "asr": 48000,
        "audio_channels": 2,
        "tags": ["ai", "makemoney", "chatgpt"] # Added example tags based on description
    }

    print("原始 YouTube 信息提取成功，现在转换为标准格式...")
    standard_format_info = convert_youtube_info_to_standard_format(raw_info_dict)

    print("\n--- 标准格式输出 ---")
    print(json.dumps(standard_format_info, indent=4, ensure_ascii=False))