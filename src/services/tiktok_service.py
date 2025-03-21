import os
import sys
import asyncio
from typing import Optional, Dict, Any
from pathlib import Path


# 将 TikTokDownloader 添加到 Python 路径
BASE_DIR = Path(__file__).parent.parent
TK_DOWN_PATH = BASE_DIR / "libs" / "tiktok_downloader"
sys.path.append(str(TK_DOWN_PATH))


from src.utils.tiktok_exceptions import TikTokDownloadError
from TikTokDownloader import TikTokDownloader  # 假设的导入路径



class TikTokContentExtractor:
    @staticmethod
    async def extract_video_info(url: str) -> Optional[Dict[str, Any]]:
        """
        异步提取 TikTok 视频信息
        
        :param url: TikTok 视频链接
        :return: 视频详细信息字典
        """
        try:
            # 使用 TikTokDownloader 的同步方法
            downloader = TikTokDownloader()
            video_info = downloader.get_video_info(url)
            
            return {
                '视频ID': video_info.get('video_id', ''),
                '视频链接': url,
                '作者昵称': video_info.get('author_nickname', ''),
                '作者主页': video_info.get('author_url', ''),
                '视频标题': video_info.get('desc', ''),
                '点赞数': video_info.get('like_count', 0),
                '评论数': video_info.get('comment_count', 0),
                '分享数': video_info.get('share_count', 0),
                '下载地址': video_info.get('download_url', '')
            }
        
        except Exception as e:
            raise TikTokDownloadError(f"提取 TikTok 视频信息失败: {e}")

    @classmethod
    def sync_extract(cls, url: str) -> Optional[Dict[str, Any]]:
        """
        同步提取方法
        """
        return asyncio.run(cls.extract_video_info(url))

    @staticmethod
    async def download_video(url: str, save_path: str = './downloads') -> str:
        """
        异步下载 TikTok 视频
        
        :param url: TikTok 视频链接
        :param save_path: 保存路径
        :return: 下载后的文件路径
        """
        try:
            downloader = TikTokDownloader()
            return downloader.download_video(url, save_path)
        
        except Exception as e:
            raise TikTokDownloadError(f"下载 TikTok 视频失败: {e}")

# 便捷函数
def extract_tiktok_content(url: str) -> Optional[Dict[str, Any]]:
    return TikTokContentExtractor.sync_extract(url)

def download_tiktok_video(url: str, save_path: str = './downloads') -> str:
    return TikTokContentExtractor.download_video(url, save_path)