import asyncio
import re
import json
import os
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union

import httpx
from httpx import AsyncClient, HTTPStatusError, RequestError

@dataclass
class XHSDownloader:
    """小红书内容下载器"""
    
    # 网络请求配置
    headers: Dict[str, str] = field(default_factory=dict)
    proxy: Optional[str] = None
    timeout: int = 10
    cookie: Optional[str] = None
    
    def __post_init__(self):
        """初始化headers和cookie"""
        default_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://www.xiaohongshu.com/explore",
            "Origin": "https://www.xiaohongshu.com",
            "Sec-Ch-Ua": '"Not_A_Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }
        
        # 合并用户自定义headers
        self.headers = {**default_headers, **self.headers}
        
        # 添加cookie
        if self.cookie:
            self.headers["Cookie"] = self.cookie

    async def _create_client(self) -> AsyncClient:
        """创建异步HTTP客户端"""
        transport = None
        if self.proxy:
            transport = httpx.AsyncHTTPTransport(
                proxy=httpx.Proxy(
                    url=self.proxy,
                    mode="TUNNEL"
                )
            )
        
        return AsyncClient(
            headers=self.headers,
            transport=transport,
            timeout=self.timeout,
            follow_redirects=True,
            verify=False
        )

    def _clean_url(self, url: str) -> str:
        """清理URL，移除token等参数"""
        return re.sub(r'\?.*', '', url)

    async def _request(self, url: str, method: str = 'GET') -> httpx.Response:
        """统一网络请求方法"""
        clean_url = self._clean_url(url)
        
        try:
            async with await self._create_client() as client:
                response = await client.request(method, clean_url)
                response.raise_for_status()
                return response
        except (HTTPStatusError, RequestError) as e:
            print(f"请求错误: {e}")
            # 打印响应内容以便调试
            if hasattr(e, 'response'):
                print(f"响应内容: {e.response.text}")
            raise

    async def extract_note_info(self, url: str) -> Dict[str, Any]:
        """提取作品详细信息"""
        try:
            response = await self._request(url)
            html = response.text
            
            # 打印HTML以便调试
            print("响应HTML长度:", len(html))
            
            # 使用正则提取JSON数据
            match = re.search(r'window\.__INITIAL_STATE__=({.*?});', html, re.DOTALL)
            if not match:
                # 如果没有匹配到，打印HTML内容
                print("未找到 __INITIAL_STATE__ 数据")
                print("HTML预览:", html[:1000])  # 打印前1000个字符
                raise ValueError("未找到作品数据")
            
            try:
                data = json.loads(match.group(1))
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                print("解析失败的JSON片段:", match.group(1)[:500])
                raise
            
            # 提取关键信息
            note_data = data.get('noteDetailMap', {}).get('note', {})
            
            # 如果note_data为空，打印调试信息
            if not note_data:
                print("note_data为空")
                print("noteDetailMap:", data.get('noteDetailMap', {}))
                raise ValueError("无法提取作品详细信息")
            
            # 提取图片链接
            images = []
            if note_data.get('imageList'):
                for img in note_data['imageList']:
                    # 获取高清大图链接
                    if img.get('urlDefault'):
                        image_url = img['urlDefault'].split('?')[0]
                        image_url = f"{image_url}?imageView2/format/png"
                        images.append(image_url)
            
            return {
                'id': note_data.get('noteId', ''),
                'title': note_data.get('title', ''),
                'desc': note_data.get('desc', ''),
                'type': '视频' if note_data.get('type') == 'video' else '图文',
                'author': {
                    'id': note_data.get('user', {}).get('userId', ''),
                    'name': note_data.get('user', {}).get('nickname', '')
                },
                'images': images,
                'video': self._extract_video_url(note_data),
                'stats': {
                    'like_count': note_data.get('interactInfo', {}).get('likedCount', 0),
                    'comment_count': note_data.get('interactInfo', {}).get('commentCount', 0),
                    'collect_count': note_data.get('interactInfo', {}).get('collectedCount', 0)
                }
            }
        except Exception as e:
            print(f"提取信息失败: {e}")
            return {}

    def _extract_video_url(self, note_data: Dict[str, Any]) -> Optional[str]:
        """提取视频下载地址"""
        # 尝试多种方式提取视频地址
        video_key_paths = [
            ('video', 'consumer', 'originVideoKey'),
            ('video', 'consumer', 'videoKey'),
            ('consumer', 'originVideoKey')
        ]
        
        for path in video_key_paths:
            try:
                video_key = note_data
                for key in path:
                    video_key = video_key.get(key, {})
                if isinstance(video_key, str):
                    return f"https://sns-video-bd.xhscdn.com/{video_key}"
            except Exception:
                continue
        
        return None

    async def download_images(
        self, 
        images: List[str], 
        save_path: str = './downloads', 
        max_concurrent: int = 5
    ) -> List[str]:
        """
        下载图片，支持并发下载
        
        :param images: 图片URL列表
        :param save_path: 保存路径
        :param max_concurrent: 最大并发数
        :return: 下载成功的图片路径列表
        """
        os.makedirs(save_path, exist_ok=True)
        
        async def download_single_image(url: str) -> Optional[str]:
            try:
                async with await self._create_client() as client:
                    response = await client.get(url)
                    response.raise_for_status()
                    
                    # 使用hash值作为文件名，避免重复
                    filename = os.path.join(save_path, f"{hash(url)}.png")
                    
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    
                    return filename
            except Exception as e:
                print(f"下载图片 {url} 失败: {e}")
                return None

        # 使用信号量控制并发
        sem = asyncio.Semaphore(max_concurrent)
        
        async def bounded_download(url):
            async with sem:
                return await download_single_image(url)
        
        # 并发下载
        tasks = [bounded_download(url) for url in images]
        results = await asyncio.gather(*tasks)
        
        # 过滤None值
        return [path for path in results if path]

    async def download_video(
        self, 
        video_url: str, 
        save_path: str = './downloads', 
        filename: Optional[str] = None
    ) -> Optional[str]:
        """
        下载视频
        
        :param video_url: 视频URL
        :param save_path: 保存路径
        :param filename: 自定义文件名
        :return: 下载成功的视频路径
        """
        os.makedirs(save_path, exist_ok=True)
        
        try:
            async with await self._create_client() as client:
                response = await client.get(video_url)
                response.raise_for_status()
                
                # 如果没有提供文件名，使用URL的hash值
                if not filename:
                    filename = f"{hash(video_url)}.mp4"
                
                filepath = os.path.join(save_path, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                return filepath
        except Exception as e:
            print(f"下载视频失败: {e}")
            return None

# 使用示例
async def main():
    # 初始化下载器
    downloader = XHSDownloader(
        # 可选：配置代理
        # proxy="http://127.0.0.1:7890",
        
        # 可选：配置Cookie
        # cookie="your_xiaohongshu_cookie"
    )
    
    # 替换为实际的小红书作品链接
    url = "https://www.xiaohongshu.com/explore/64674a91000000001301762e"
    
    try:
        # 提取作品信息
        note_info = await downloader.extract_note_info(url)
        
        if note_info:
            print("作品信息:")
            print(json.dumps(note_info, ensure_ascii=False, indent=2))
            
            # 下载图片
            if note_info['images']:
                image_paths = await downloader.download_images(note_info['images'])
                print("下载的图片:", image_paths)
            
            # 下载视频
            if note_info['video']:
                video_path = await downloader.download_video(note_info['video'])
                print("下载的视频:", video_path)
    
    except Exception as e:
        print(f"处理失败: {e}")

if __name__ == "__main__":
    asyncio.run(main())