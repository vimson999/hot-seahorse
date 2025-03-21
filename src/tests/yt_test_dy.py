import json
import os
import yt_dlp

def extract_douyin_info(url, cookies_file=None):
    """
    使用 yt-dlp 提取抖音视频信息，并以美观格式打印 meta 信息
    
    Args:
        url: 抖音视频URL
        cookies_file: cookies文件路径
    """
    # 设置 yt-dlp 选项
    ydl_opts = {
        'quiet': True,  # 减少输出信息
        'no_warnings': True,  # 不显示警告
        'skip_download': True,  # 仅提取信息，不下载
        'nocheckcertificate': True,  # 不检查SSL证书
        # 'format': 'bestvideo+bestaudio/best',  # 选择最佳质量
    }
    
    # 添加cookies文件如果提供了
    if cookies_file and os.path.exists(cookies_file):
        ydl_opts['cookiefile'] = cookies_file
        print(f"使用 cookies 文件: {cookies_file}")
    
    try:
        # 创建 yt-dlp 下载对象
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 提取信息但不下载
            meta = ydl.extract_info(url, download=False)
            
            # 打印完整的 meta 数据结构
            print("=== 完整的 meta 数据结构 ===")
            print(json.dumps(meta, indent=4, ensure_ascii=False))
            
            # 提取并打印一些重要字段
            print("\n=== 重要字段摘要 ===")
            if meta:
                print(f"标题: {meta.get('title')}")
                print(f"上传者: {meta.get('uploader')}")
                print(f"视频ID: {meta.get('id')}")
                print(f"持续时间: {meta.get('duration')} 秒")
                
                # 格式信息
                print("\n可用的格式:")
                for fmt in meta.get('formats', []):
                    print(f"- 格式ID: {fmt.get('format_id')}, "
                          f"分辨率: {fmt.get('resolution', '未知')}, "
                          f"扩展名: {fmt.get('ext')}, "
                          f"文件大小: {fmt.get('filesize', '未知')} bytes")
                
                # 缩略图信息
                print("\n缩略图:")
                for thumb in meta.get('thumbnails', []):
                    print(f"- URL: {thumb.get('url')}")
                    print(f"  分辨率: {thumb.get('width')}x{thumb.get('height')}")
            
            return meta
    except Exception as e:
        print(f"提取信息时出错: {str(e)}")
        return None

def download_douyin_video(url, output_path=None, cookies_file=None):
    """
    下载抖音视频到指定路径
    
    Args:
        url: 抖音视频URL
        output_path: 输出文件路径模板
        cookies_file: cookies文件路径
    """
    # 设置下载选项
    ydl_opts = {
        'format': 'best',  # 选择最佳质量
        'outtmpl': output_path or '%(title)s-%(id)s.%(ext)s',  # 输出文件名模板
        'nocheckcertificate': True,
    }
    
    # 添加cookies文件如果提供了
    if cookies_file and os.path.exists(cookies_file):
        ydl_opts['cookiefile'] = cookies_file
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("视频下载完成!")
    except Exception as e:
        print(f"下载视频时出错: {str(e)}")

if __name__ == "__main__":
    # 替换为你要下载的抖音视频链接
    # 注意：如果是分享链接，yt-dlp 通常也可以处理（会自动跳转）
    douyin_url = "https://www.douyin.com/video/7475254041207950642"  # 看起来你已经有实际的视频ID
    
    # 查找当前项目中的 cookies 文件
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    possible_cookies = [
        os.path.join(base_dir, "cookies.txt"),
        os.path.join(base_dir, "cookies-yt copy.txt"),
        os.path.join(base_dir, "cookies copy.txt")
    ]
    
    # 找到第一个存在的 cookies 文件
    cookies_path = None
    for cookie_file in possible_cookies:
        if os.path.exists(cookie_file):
            cookies_path = cookie_file
            break
    
    if cookies_path:
        print(f"找到 cookies 文件: {cookies_path}")
    else:
        print("警告: 未找到 cookies 文件! 抖音需要 cookies 才能提取视频信息。")
        print("请确保有效的 cookies 文件存在，文件应包含抖音网站的 cookies。")
        print("可以使用浏览器扩展如 'Get cookies.txt' 或 'Cookie-Editor' 来导出 cookies。")
    
    # 提取信息
    meta_info = extract_douyin_info(douyin_url, cookies_path)
    
    # 如果你还想下载视频，取消下面这行的注释
    # download_douyin_video(douyin_url, "./downloaded_video.mp4", cookies_path)