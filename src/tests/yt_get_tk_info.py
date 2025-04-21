# import yt_dlp
# import json # 引入 json 模块，用于格式化输出

# # 视频 URL
# video_url = 'https://www.tiktok.com/@__maakun__official/video/7494234815709891858?is_from_webapp=1&sender_device=pc'

# # 配置 yt-dlp 选项
# # 'quiet': True         # 禁止 yt-dlp 打印信息到控制台
# # 'no_warnings': True   # 禁止 yt-dlp 打印警告信息
# # 更多选项可以参考 yt-dlp 的文档
# ydl_opts = {
#     'quiet': True,
#     'no_warnings': True,
# }

# # 创建 YoutubeDL 对象
# # 使用 with 语句确保资源被正确处理
# try:
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         # 使用 extract_info 方法获取信息
#         # download=False 表示只获取信息，不下载视频
#         info_dict = ydl.extract_info(video_url, download=False)

#         # 打印获取到的完整信息字典 (使用 json 格式化，更易读)
#         # ensure_ascii=False 保证中文等非 ASCII 字符能正确显示
#         print(json.dumps(info_dict, indent=4, ensure_ascii=False))

#         # 你也可以只提取和打印你感兴趣的特定信息，例如：
#         # print(f"视频标题: {info_dict.get('title')}")
#         # print(f"上传者: {info_dict.get('uploader')}")
#         # print(f"视频 ID: {info_dict.get('id')}")
#         # print(f"描述: {info_dict.get('description')}")
#         # print(f"时长 (秒): {info_dict.get('duration')}")
#         # print(f"观看次数: {info_dict.get('view_count')}")
#         # print(f"点赞数: {info_dict.get('like_count')}")
#         # print(f"评论数: {info_dict.get('comment_count')}")
#         # print(f"分享数: {info_dict.get('repost_count')}") # 注意：TikTok 可能叫 repost 或 share

# except yt_dlp.utils.DownloadError as e:
#     print(f"获取视频信息时出错: {e}")
# except Exception as e:
#     print(f"发生未知错误: {e}")



import yt_dlp
import json
import re # 用于提取 hashtags
from typing import Dict, Any, List # 引入类型提示，使代码更清晰
import time # 用于获取当前时间戳（如果需要）
# 注意：你可能需要根据你的项目结构调整 MediaType 的导入或定义
# 这里我先用简单的类来定义它，模拟你的环境
class MediaType:
    VIDEO = "video"
    IMAGE = "image"
    UNKNOWN = "unknown"

def extract_hashtags(text: str) -> List[str]:
    """从文本中提取 hashtags (例如 #tag)"""
    if not text:
        return []
    # 正则表达式查找 # 后跟至少一个非空格、非#号的字符
    # 这可以匹配中文、英文、数字等，但可能需要根据实际情况微调
    hashtags = re.findall(r"#([^\s#]+)", text)
    # 移除提取出的 tag 名本身，只保留 tag 内容
    return hashtags

def convert_tiktok_info_to_standard_format(info_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    将原始 yt-dlp TikTok 视频信息转换为标准格式

    Args:
        info_dict: 从 yt-dlp 获取的原始视频信息字典

    Returns:
        Dict[str, Any]: 标准格式的笔记数据
    """
    try:
        # --- 媒体信息 ---
        # yt-dlp 返回的顶层字段通常代表最佳或选定的格式信息
        media_info = {
            "cover_url": info_dict.get('thumbnail'), # 视频封面图
            "type": MediaType.VIDEO, # TikTok 内容是视频
            "video_url": info_dict.get('url'),      # 视频播放地址 (通常是选定的最佳格式)
            "duration": int(info_dict.get('duration', 0) or 0), # 视频时长 (秒)
            "width": int(info_dict.get('width', 0) or 0),       # 视频宽度
            "height": int(info_dict.get('height', 0) or 0)      # 视频高度
        }
        # 如果顶层没有 URL，尝试从 formats 列表获取 (备用方案)
        if not media_info["video_url"] and info_dict.get("formats"):
             # 选择一个格式，例如最后一个（通常质量较好）或根据需要选择
             selected_format = info_dict["formats"][-1]
             media_info["video_url"] = selected_format.get("url")
             if media_info["width"] == 0: media_info["width"] = int(selected_format.get("width", 0) or 0)
             if media_info["height"] == 0: media_info["height"] = int(selected_format.get("height", 0) or 0)

        # --- 统计数据 ---
        statistics = {
             # yt-dlp 返回的通常是整数，如果不是或为 None 则设为 0
            "like_count": int(info_dict.get('like_count', 0) or 0),
            "comment_count": int(info_dict.get('comment_count', 0) or 0),
            "share_count": int(info_dict.get('repost_count', 0) or 0), # TikTok 对应的是 repost_count
            "collected_count": 0, # yt-dlp 通常不提供收藏数，设为 0
            "view_count": int(info_dict.get('view_count', 0) or 0)
        }

        # --- 作者信息 ---
        author = {
            "id": info_dict.get('uploader_id', ''),        # 作者的用户 ID
            "nickname": info_dict.get('uploader', ''),      # 作者的昵称/用户名 ('channel' 字段有时是显示名)
            "avatar": "",                                   # yt-dlp 通常不单独提供作者头像 URL
            "signature": "",                                # 无此信息
            "verified": False,                              # 无此信息
            "follower_count": 0,                            # 无此信息
            "following_count": 0,                           # 无此信息
            "notes_count": 0,                               # 无此信息
            "location": ""                                  # 无地理位置信息
        }

        # --- 标签信息 ---
        # 从标题和描述中提取 hashtags
        description_text = info_dict.get('description', '')
        title_text = info_dict.get('title', '')
        combined_text_for_tags = f"{title_text} {description_text}"
        tags = extract_hashtags(combined_text_for_tags)

        # --- 时间信息 ---
        # yt-dlp 提供 'timestamp' (发布时间的 Unix 时间戳) 或 'upload_date' (YYYYMMDD)
        #优先使用 timestamp (epoch)
        create_timestamp = info_dict.get('timestamp', info_dict.get('epoch'))
        # 如果只有 upload_date，可以尝试转换，但 timestamp 更精确
        # if not create_timestamp and info_dict.get('upload_date'):
        #     try:
        #         # 注意：这只精确到天
        #         upload_dt = datetime.datetime.strptime(info_dict['upload_date'], '%Y%m%d')
        #         create_timestamp = int(upload_dt.timestamp())
        #     except (ValueError, TypeError):
        #         create_timestamp = None # 无法解析则留空


        # --- 构造最终结果 ---
        result = {
            "note_id": info_dict.get('id', ''),               # 视频 ID
            "title": info_dict.get('title', ''),              # 视频标题
            "desc": info_dict.get('description', ''),         # 视频描述
            "type": MediaType.VIDEO,                          # 类型为视频
            "author": author,                                 # 作者信息
            "statistics": statistics,                         # 统计数据
            "tags": tags,                                     # 提取的标签列表
            "media": media_info,                              # 媒体信息
            "images": [],                                     # 因为是视频，所以图片列表为空
            "original_url": info_dict.get('webpage_url', info_dict.get('original_url', '')), # 原始网页链接
            "create_time": create_timestamp,                  # 创建时间戳 (epoch)
            "last_update_time": create_timestamp              # 最后更新时间戳 (TikTok 无此信息，使用创建时间)
        }

        return result

    except Exception as e:
        # 在实际应用中，这里应该使用日志记录器 logger.error()
        print(f"转换 TikTok 视频信息时发生错误: {e}")
        # 返回一个基础结构，包含 ID 和 URL，避免后续流程完全失败
        return {
            "note_id": info_dict.get('id', ''),
            "title": info_dict.get('title', ''),
            "desc": info_dict.get('description', ''),
            "type": MediaType.UNKNOWN,
            "author": {"id": info_dict.get('uploader_id', ''), "nickname": info_dict.get('uploader', '')},
            "statistics": {},
            "tags": [],
            "media": {},
            "images": [],
            "original_url": info_dict.get('webpage_url', ''),
            "create_time": None,
            "last_update_time": None
        }

# --- 主程序部分 ---
if __name__ == "__main__":
    video_url = 'https://www.tiktok.com/@__maakun__official/video/7494234815709891858?is_from_webapp=1&sender_device=pc'

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        # 'forcejson': True, # 可以强制输出 JSON，但 extract_info 本身就返回字典
        # 'skip_download': True, # extract_info(download=False) 效果相同
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 1. 获取原始信息
            print("正在获取视频信息...")
            raw_info_dict = ydl.extract_info(video_url, download=False)
            # print("\n--- 原始 YT-DLP 输出 ---")
            # print(json.dumps(raw_info_dict, indent=4, ensure_ascii=False)) # 可以取消注释查看原始输出

            # 2. 转换为标准格式
            print("\n正在转换格式...")
            standard_format_info = convert_tiktok_info_to_standard_format(raw_info_dict)

            # 3. 打印标准格式的结果
            print("\n--- 标准格式输出 ---")
            print(json.dumps(standard_format_info, indent=4, ensure_ascii=False))

    except yt_dlp.utils.DownloadError as e:
        print(f"获取视频信息时出错: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")