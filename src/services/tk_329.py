import asyncio
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union, List

# 获取项目根目录路径
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parents[1]  # hot-seahorse 项目根目录
tiktok_root = project_root / "src" / "libs" / "tiktok_downloader"

# 将TikTokDownloader路径添加到系统路径
if str(tiktok_root) not in sys.path:
    sys.path.append(str(tiktok_root))
    
# 临时修改当前工作目录以便正确加载TikTokDownloader的模块
original_dir = os.getcwd()
os.chdir(str(tiktok_root))

# 导入TikTokDownloader模块
from src.config import Settings, Parameter
from src.custom import PROJECT_ROOT
from src.tools import ColorfulConsole
from src.module import Cookie
from src.interface import Detail, User
from src.link import Extractor
from src.extract import Extractor as DataExtractor
from src.record import BaseLogger

# 创建一个简单的伪记录器类，用于替代数据库记录器
class DummyRecorder:
    """
    伪记录器类，用于替代实际的数据库记录器
    实现一个空的save方法，避免NoneType错误
    """
    def __init__(self):
        self.field_keys = []
    
    async def save(self, *args, **kwargs):
        """空的保存方法，避免NoneType错误"""
        pass

# 恢复原始工作目录
os.chdir(original_dir)


class TikTokService:
    """
    TikTokDownloader服务类，提供简化的API来获取抖音视频详细信息
    不使用数据库功能，适用于直接运行测试
    """
    
    def __init__(self, cookie: Optional[str] = None):
        """
        初始化TikTokService
        
        Args:
            cookie: 抖音cookie字符串，可选
        """
        self.console = ColorfulConsole()
        self.settings = Settings(PROJECT_ROOT, self.console)
        self.cookie_object = Cookie(self.settings, self.console)
        self.parameters = None
        self.cookie = cookie
        
    async def __aenter__(self):
        """
        异步上下文管理器入口，初始化参数
        """
        # 获取设置
        settings_data = self.settings.read()
        
        # 如果提供了cookie，更新设置
        if self.cookie:
            cookie_dict = self.cookie_object.extract(self.cookie, write=False)
            settings_data["cookie"] = cookie_dict
        
        # 初始化参数
        self.parameters = Parameter(
            self.settings,
            self.cookie_object,
            logger=BaseLogger,  # 使用基础日志记录器
            console=self.console,
            recorder=None,      # 不使用记录器
            **settings_data
        )
        
        # 设置headers和cookie
        self.parameters.set_headers_cookie()
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        异步上下文管理器退出，关闭客户端
        """
        if self.parameters:
            await self.parameters.close_client()
    
    async def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """
        获取抖音视频的详细信息
        
        Args:
            url: 抖音视频链接
            
        Returns:
            包含视频详细信息的字典，如果获取失败则返回None
        """
        if not self.parameters:
            raise RuntimeError("服务未正确初始化，请使用async with语句")
        
        try:
            # 提取视频ID
            extractor = Extractor(self.parameters)
            video_ids = await extractor.run(url)
            
            if not video_ids:
                self.console.warning(f"无法从链接提取视频ID: {url}")
                return None
            
            video_id = video_ids[0]
            self.console.info(f"成功提取视频ID: {video_id}")
            
            # 获取视频详情
            detail = Detail(
                self.parameters,
                detail_id=video_id
            )
            
            video_data = await detail.run()
            if not video_data:
                self.console.warning(f"无法获取视频ID为 {video_id} 的详细信息")
                return None
            
            # 处理获取到的数据
            data_extractor = DataExtractor(self.parameters)
            # 使用伪记录器代替None
            dummy_recorder = DummyRecorder()
            processed_data = await data_extractor.run(
                [video_data], 
                dummy_recorder,  # 使用伪记录器
                tiktok=False
            )
            
            return processed_data[0] if processed_data else None
            
        except Exception as e:
            self.console.error(f"获取视频信息时发生异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
            
    async def get_user_info(self, sec_user_id: str) -> Optional[Dict[str, Any]]:
        """
        获取抖音用户的详细信息
        
        Args:
            sec_user_id: 抖音用户的sec_user_id
            
        Returns:
            包含用户详细信息的字典，如果获取失败则返回None
        """
        if not self.parameters:
            raise RuntimeError("服务未正确初始化，请使用async with语句")
        
        try:
            # 获取用户详情
            user = User(
                self.parameters,
                sec_user_id=sec_user_id
            )
            
            user_data = await user.run()
            if not user_data:
                self.console.warning(f"无法获取用户ID为 {sec_user_id} 的详细信息")
                return None
                
            # 使用伪记录器代替None
            dummy_recorder = DummyRecorder()
            data_extractor = DataExtractor(self.parameters)
            processed_data = await data_extractor.run(
                [user_data], 
                dummy_recorder,
                type_="user"
            )
            
            return processed_data[0] if processed_data else None
            
        except Exception as e:
            self.console.error(f"获取用户信息时发生异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    async def download_video(self, url: str, output_path: Optional[str] = None) -> Optional[str]:
        """
        下载抖音视频
        
        Args:
            url: 抖音视频链接
            output_path: 输出路径，可选，默认使用设置中的路径
            
        Returns:
            下载的文件路径，如果下载失败则返回None
        """
        # 该功能在后续实现
        raise NotImplementedError("下载功能尚未实现")


async def get_video_info(url: str, cookie: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    获取抖音视频的详细信息的便捷函数
    
    Args:
        url: 抖音视频链接
        cookie: 抖音cookie字符串，可选
        
    Returns:
        包含视频详细信息的字典，如果获取失败则返回None
    """
    async with TikTokService(cookie) as service:
        return await service.get_video_info(url)


async def get_user_info(sec_user_id: str, cookie: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    获取抖音用户的详细信息的便捷函数
    
    Args:
        sec_user_id: 抖音用户的sec_user_id
        cookie: 抖音cookie字符串，可选
        
    Returns:
        包含用户详细信息的字典，如果获取失败则返回None
    """
    async with TikTokService(cookie) as service:
        return await service.get_user_info(sec_user_id)


# 主函数示例，用于直接运行模块时进行测试
async def main():
    """
    测试函数，可以直接运行这个模块进行测试
    使用方法: python src/services/tk_329.py
    """
    # 测试URL
    test_url = "https://www.douyin.com/video/7481984316822555913"
    
    print(f"正在获取视频信息: {test_url}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python路径: {sys.path}")
    
    try:
        async with TikTokService() as service:
            # 获取视频信息
            print("\n===== 测试一: 获取视频信息 =====")
            info = await service.get_video_info(test_url)
            if info:
                print("\n成功获取视频信息:")
                print(f"标题: {info.get('desc', '无标题')}")
                print(f"作者: {info.get('nickname', '未知作者')}")
                print(f"作者ID: {info.get('sec_uid', '未知ID')}")
                print(f"创建时间: {info.get('create_time', '未知')}")
                print(f"点赞数: {info.get('digg_count', 0)}")
                print(f"评论数: {info.get('comment_count', 0)}")
                print(f"收藏数: {info.get('collect_count', 0)}")
                print(f"分享数: {info.get('share_count', 0)}")
                print(f"类型: {info.get('type', '未知')}")
                print(f"视频分辨率: {info.get('width', 0)}x{info.get('height', 0)}")
                print(f"下载地址: {info.get('downloads', '无下载地址')}")
                
                # 获取视频作者信息
                print("\n===== 测试二: 获取用户信息 =====")
                sec_user_id = info.get('sec_uid')
                if sec_user_id:
                    print(f"正在获取用户信息: {info.get('nickname')} (sec_user_id: {sec_user_id})")
                    user_info = await service.get_user_info(sec_user_id)
                    if user_info:
                        print("\n成功获取用户信息:")
                        print(f"昵称: {user_info.get('nickname', '未知')}")
                        print(f"签名: {user_info.get('signature', '无签名')}")
                        print(f"UID: {user_info.get('uid', '未知')}")
                        print(f"SEC_UID: {user_info.get('sec_uid', '未知')}")
                        print(f"抖音号: {user_info.get('unique_id', '未知')}")
                        print(f"粉丝数: {user_info.get('follower_count', 0)}")
                        print(f"关注数: {user_info.get('following_count', 0)}")
                        print(f"获赞数: {user_info.get('total_favorited', 0)}")
                        print(f"作品数: {user_info.get('aweme_count', 0)}")
                        print(f"头像: {user_info.get('avatar', '无头像')}")
                        print(f"主页背景: {user_info.get('cover', '无背景')}")
                    else:
                        print(f"无法获取用户 {sec_user_id} 的信息")
                else:
                    print("视频信息中没有提供作者ID，无法获取用户信息")
                
            else:
                print("获取视频信息失败")
    except Exception as e:
        print(f"运行测试时发生异常: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 运行测试函数
    asyncio.run(main())