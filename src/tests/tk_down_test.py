import os
import sys
import pytest

# 添加项目根目录和 TikTokDownloader 目录到 Python 路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
tiktok_downloader_root = os.path.join(project_root, 'src', 'libs', 'tiktok_downloader')
sys.path.insert(0, project_root)
sys.path.insert(0, tiktok_downloader_root)

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(project_root, 'src'))

# 重新组织导入路径
from libs.tiktok_downloader.src.application.TikTokDownloader import TikTokDownloader

def test_tiktok_downloader_initialization():
    """测试 TikTokDownloader 初始化"""
    try:
        downloader = TikTokDownloader()
        assert downloader is not None, "TikTokDownloader 初始化失败"
    except Exception as e:
        pytest.fail(f"TikTokDownloader 初始化失败: {e}")

def test_extract_video_info():
    """测试视频信息提取"""
    # 注意：替换为一个真实的、公开的 TikTok 视频链接
    test_url = "https://www.douyin.com/video/7475254041207950642"
    
    downloader = TikTokDownloader()
    try:
        # 根据实际 TikTokDownloader 的 API 调整方法名
        video_info = downloader.get_video_info(test_url)
        
        assert video_info is not None, "未能获取视频信息"
        # 根据实际返回的字典结构调整断言
        assert isinstance(video_info, dict), "视频信息应该是一个字典"
        
        print("视频信息:", video_info)
    except Exception as e:
        pytest.fail(f"提取视频信息时发生错误: {e}")

def test_download_video():
    """测试视频下载功能"""
    # 注意：替换为一个真实的、公开的 TikTok 视频链接
    test_url = "https://www.douyin.com/video/7475254041207950642"
    download_path = "./test_downloads"
    
    # 确保下载目录存在
    os.makedirs(download_path, exist_ok=True)
    
    downloader = TikTokDownloader()
    downloaded_file = None
    try:
        # 根据实际 TikTokDownloader 的 API 调整方法名
        downloaded_file = downloader.download_video(test_url, download_path)
        
        assert downloaded_file is not None, "下载视频失败"
        assert os.path.exists(downloaded_file), "下载的文件不存在"
        assert os.path.getsize(downloaded_file) > 0, "下载的文件大小为零"
        
        print(f"视频已下载到: {downloaded_file}")
    except Exception as e:
        pytest.fail(f"下载视频时发生错误: {e}")
    finally:
        # 清理下载的文件
        if downloaded_file and os.path.exists(downloaded_file):
            os.remove(downloaded_file)

def test_video_metadata():
    """测试视频元数据提取"""
    # 注意：替换为一个真实的、公开的 TikTok 视频链接
    test_url = "https://www.douyin.com/video/7475254041207950642"
    
    downloader = TikTokDownloader()
    try:
        # 根据实际 TikTokDownloader 的 API 调整方法名
        metadata = downloader.get_video_metadata(test_url)
        
        assert metadata is not None, "未能获取视频元数据"
        # 根据实际返回的字典结构调整断言
        assert isinstance(metadata, dict), "元数据应该是一个字典"
        
        print("视频元数据:", metadata)
    except Exception as e:
        pytest.fail(f"提取视频元数据时发生错误: {e}")

if __name__ == "__main__":
    pytest.main([__file__])