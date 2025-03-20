import yt_dlp
import json
from datetime import datetime

def get_xhs_stats(url, cookie_file='cookies.txt'):
    ydl_opts = {
        'cookiefile': cookie_file,
        'quiet': True,
        'force_generic_extractor': True,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.xiaohongshu.com/',
            'X-Sign': 'X'  # 需要动态生成签名时可替换
        },
        # 增加视频信息提取配置
        'extract_flat': 'in_playlist',
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)
            
            # 调试时查看完整元数据（生产环境建议注释）
            print('完整元数据:\n' + json.dumps(meta, indent=2, ensure_ascii=False))
            
            # 转换时间戳格式
            timestamp = meta.get('timestamp')
            upload_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'N/A'

            # 小红书实际字段映射（根据最新调试结果）
            stats = {
                "标题": meta.get('title', 'N/A'),
                "视频ID": meta.get('id') or url.split('/')[-1].split('?')[0],
                "播放量": meta.get('view_count', 0),       # 实测字段为 view_count
                "点赞量": meta.get('like_count', 0),
                "收藏量": meta.get('favorite_count', 0),  # 实际字段可能不同
                "评论量": meta.get('comment_count', 0),
                "分享量": meta.get('share_count', 0),
                "作者": meta.get('uploader', 'N/A'),
                "发布时间": upload_time,
                "视频封面": meta.get('thumbnail', 'N/A')
            }

            return json.dumps(stats, ensure_ascii=False, indent=2)
    
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e).lower()
        if "login" in error_msg or "cookie" in error_msg:
            return "错误：需要有效的登录Cookie (HTTP 403)"
        elif "unable to download webpage" in error_msg:
            return "错误：页面不存在或URL无效"
        return f"请求失败: {str(e)}"
    except Exception as e:
        return f"解析失败: {type(e).__name__} - {str(e)}"

# 示例使用
url = "https://www.xiaohongshu.com/explore/64674a91000000001301762e?xsec_token=ABAJcy_294mBZauFhAac6izmJvYB6yqm49MAtXSVU8XA4=&xsec_source=pc_feed"
print(get_xhs_stats(url))