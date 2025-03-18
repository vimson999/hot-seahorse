import asyncio
import re
import json
from typing import Optional, Dict, Any
import httpx
from lxml import etree

class XHSContentExtractor:
    @staticmethod
    async def extract_content(url: str) -> Optional[Dict[str, Any]]:
        """
        异步提取小红书作品内容
        
        :param url: 小红书作品链接
        :return: 作品详细信息字典
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.xiaohongshu.com/explore',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
            }
            
            async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
                response = await client.get(url)
                html = response.text
                
                # 使用正则提取初始状态
                pattern = r'window\.__INITIAL_STATE__=(.*?)(?=\n|</script>)'
                match = re.search(pattern, html, re.DOTALL)
                
                if match:
                    # 解析 JSON 数据
                    initial_state_str = match.group(1).rstrip(';')
                    initial_state = json.loads(initial_state_str)
                    
                    # 提取作品信息
                    note_data = initial_state.get('noteDetailMap', {})
                    if not note_data:
                        return None
                    
                    note = list(note_data.values())[0].get('note', {})
                    user = note.get('user', {})
                    interact_info = note.get('interactInfo', {})
                    
                    return {
                        '作品ID': note.get('noteId', ''),
                        '作品链接': f"https://www.xiaohongshu.com/explore/{note.get('noteId', '')}",
                        '作品标题': note.get('title', ''),
                        '作品描述': note.get('desc', ''),
                        '作品类型': '视频' if note.get('type') == 'video' else '图文',
                        '发布时间': note.get('time', ''),
                        '最后更新时间': note.get('lastUpdateTime', ''),
                        '作者昵称': user.get('nickname', ''),
                        '作者ID': user.get('userId', ''),
                        '作者链接': f"https://www.xiaohongshu.com/user/profile/{user.get('userId', '')}",
                        '点赞数量': interact_info.get('likedCount', 0),
                        '收藏数量': interact_info.get('collectedCount', 0),
                        '评论数量': interact_info.get('commentCount', 0),
                        '分享数量': interact_info.get('shareCount', 0),
                        '作品标签': ' '.join([tag.get('name', '') for tag in note.get('tagList', [])])
                    }
                
                return None
        
        except Exception as e:
            print(f"提取内容失败: {e}")
            return None

    @classmethod
    def sync_extract(cls, url: str) -> Optional[Dict[str, Any]]:
        """
        同步提取方法
        """
        return asyncio.run(cls.extract_content(url))

# 便捷函数
def extract_xhs_content(url: str) -> Optional[Dict[str, Any]]:
    return XHSContentExtractor.sync_extract(url)