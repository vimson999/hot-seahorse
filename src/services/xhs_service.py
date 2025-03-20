# src/services/xhs_service.py
import os
import sys
from pathlib import Path
from loguru import logger


# 确定项目根目录和Spider_XHS路径
BASE_DIR = Path(__file__).parent.parent
SPIDER_XHS_PATH = BASE_DIR / "libs" / "spider_xhs"
sys.path.append(str(SPIDER_XHS_PATH))

# 直接导入
from apis.pc_apis import XHS_Apis
from xhs_utils.data_util import handle_note_info, download_note
from xhs_utils.common_utils import init as xhs_init

class XHSService:
    def __init__(self, cookies_file=None):
        """
        初始化小红书服务
        
        Args:
            cookies_file: Cookie文件路径，如不提供则使用环境变量中的配置
        """
        self.xhs_apis = XHS_Apis()
        self.cookies_str = self._load_cookies(cookies_file)
        _, self.base_path = xhs_init()
        
    def _load_cookies(self, cookies_file):
        """加载Cookie"""
        if cookies_file and os.path.exists(cookies_file):
            with open(cookies_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        else:
            # 从环境变量加载Cookie
            from src.libs.spider_xhs.xhs_utils.common_utils import load_env
            return load_env()
    
    def get_note_info(self, note_url, proxies=None):
        """
        获取小红书笔记信息
        
        Args:
            note_url: 笔记URL
            proxies: 代理配置
            
        Returns:
            (success, msg, note_info): 成功状态、消息和笔记数据
        """
        try:
            success, msg, note_info = self.xhs_apis.get_note_info(note_url, self.cookies_str, proxies)
            if success:
                note_info = note_info['data']['items'][0]
                note_info['url'] = note_url
                note_info = handle_note_info(note_info)
                return True, "获取笔记成功", note_info
            return False, f"API调用失败: {msg}", None
        except Exception as e:
            logger.exception(f"获取笔记信息异常: {e}")
            return False, f"获取笔记异常: {str(e)}", None
    
    def download_note_media(self, note_url, save_path=None, proxies=None):
        """
        下载笔记的媒体文件(图片/视频)
        
        Args:
            note_url: 笔记URL
            save_path: 保存路径，默认使用系统路径
            proxies: 代理配置
            
        Returns:
            (success, msg, save_path): 成功状态、消息和保存路径
        """
        try:
            success, msg, note_info = self.get_note_info(note_url, proxies)
            if not success:
                return False, msg, None
                
            media_path = save_path if save_path else self.base_path['media']
            result_path = download_note(note_info, media_path)
            return True, "下载成功", result_path
        except Exception as e:
            logger.exception(f"下载笔记媒体异常: {e}")
            return False, f"下载异常: {str(e)}", None
    
    def search_notes(self, keyword, limit=10, sort="general", note_type=0, proxies=None):
        """
        搜索小红书笔记
        
        Args:
            keyword: 搜索关键词
            limit: 获取数量限制
            sort: 排序方式，general(综合排序)、time_descending(时间排序)、popularity_descending(热度排序)
            note_type: 笔记类型，0(全部)、1(视频)、2(图文)
            proxies: 代理配置
            
        Returns:
            (success, msg, notes): 成功状态、消息和笔记列表
        """
        try:
            success, msg, notes = self.xhs_apis.search_some_note(
                keyword, limit, self.cookies_str, sort, note_type, proxies
            )
            if success:
                return True, f"搜索成功，获取到{len(notes)}条结果", notes
            return False, f"搜索失败: {msg}", None
        except Exception as e:
            logger.exception(f"搜索笔记异常: {e}")
            return False, f"搜索异常: {str(e)}", None
    
    def get_user_notes(self, user_url, proxies=None):
        """
        获取用户的所有笔记
        
        Args:
            user_url: 用户主页URL
            proxies: 代理配置
            
        Returns:
            (success, msg, notes): 成功状态、消息和笔记列表
        """
        try:
            success, msg, notes = self.xhs_apis.get_user_all_notes(user_url, self.cookies_str, proxies)
            if success:
                return True, f"获取成功，该用户共有{len(notes)}条笔记", notes
            return False, f"获取用户笔记失败: {msg}", None
        except Exception as e:
            logger.exception(f"获取用户笔记异常: {e}")
            return False, f"获取异常: {str(e)}", None