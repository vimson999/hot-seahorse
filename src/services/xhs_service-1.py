import requests
import re
import json
from typing import Optional, Dict, Any

class XHSContentExtractor:
    @staticmethod
    def extract_content(url: str) -> Optional[Dict[str, Any]]:
        """
        提取小红书作品内容
        
        :param url: 小红书作品链接
        :return: 作品详细信息字典
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
                'Referer': 'https://www.xiaohongshu.com/explore',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
            }
            
            response = requests.get(url, headers=headers)
            html = response.text
            
            # 使用更健壮的正则提取
            pattern = r'window\.__INITIAL_STATE__\s*=\s*({.*?})\s*(?:;|$)'
            match = re.search(pattern, html, re.DOTALL | re.MULTILINE)
            
            if match:
                # 尝试更安全的 JSON 解析
                initial_state_str = match.group(1)
                
                # 移除 JavaScript 特殊字符和转义
                initial_state_str = initial_state_str.replace('\n', '').replace('\r', '')
                
                try:
                    initial_state = json.loads(initial_state_str)
                except json.JSONDecodeError as e:
                    print(f"JSON解析错误: {e}")
                    print(f"出错的JSON片段: {initial_state_str[:500]}...")  # 打印前500字符
                    return None
                
                # 深度提取数据的更健壮方法
                note_map = initial_state.get('noteDetailMap', {})
                if not note_map:
                    print("未找到作品详细信息")
                    return None
                
                # 获取第一个作品的详细信息
                note_key = list(note_map.keys())[0]
                note_detail = note_map[note_key].get('note', {})
                user = note_detail.get('user', {})
                interact_info = note_detail.get('interactInfo', {})
                
                return {
                    '作品ID': note_detail.get('noteId', ''),
                    '作品链接': url,
                    '作品标题': note_detail.get('title', ''),
                    '作品描述': note_detail.get('desc', ''),
                    '作品类型': '视频' if note_detail.get('type') == 'video' else '图文',
                    '发布时间': note_detail.get('time', ''),
                    '作者昵称': user.get('nickname', ''),
                    '作者ID': user.get('userId', ''),
                    '点赞数量': interact_info.get('likedCount', 0),
                    '收藏数量': interact_info.get('collectedCount', 0),
                    '评论数量': interact_info.get('commentCount', 0)
                }
            
            print("未找到初始状态数据")
            return None
        
        except Exception as e:
            print(f"提取内容失败: {e}")
            return None

# 便捷函数
def extract_xhs_content(url: str) -> Optional[Dict[str, Any]]:
    return XHSContentExtractor.extract_content(url)