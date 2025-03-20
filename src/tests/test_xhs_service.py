import os
import sys
from pathlib import Path


# 设置项目根目录路径
ROOT_DIR = Path(__file__).parent.parent.parent
# 设置 NODE_PATH 指向子模块的 node_modules 目录
os.environ["NODE_PATH"] = str(ROOT_DIR / "src" / "libs" / "spider_xhs" / "node_modules")
print(f"NODE_PATH 环境变量已设置为: {os.environ['NODE_PATH']}")

# 添加源码路径
sys.path.insert(0, str(ROOT_DIR))

from src.services.xhs_service import XHSService


# 从根目录的cookies.txt获取Cookie
cookie_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "cookies.txt")

def test_get_note_info():
    service = XHSService(cookie_file)
    # 使用一个有效的笔记URL进行测试
    note_url = "https://www.xiaohongshu.com/explore/64674a91000000001301762e?xsec_token=ABAJcy_294mBZauFhAac6izmJvYB6yqm49MAtXSVU8XA4=&xsec_source=pc_feed"
    success, msg, note_info = service.get_note_info(note_url)
    
    assert success, f"获取笔记失败: {msg}"
    assert note_info is not None
    assert "title" in note_info
    assert "desc" in note_info
    assert "note_type" in note_info
    
    print(f"标题: {note_info['title']}")
    print(f"描述: {note_info['desc'][:50]}...")
    print(f"类型: {note_info['note_type']}")

def test_search_notes():
    service = XHSService(cookie_file)
    keyword = "旅行"
    success, msg, notes = service.search_notes(keyword, limit=5)
    
    assert success, f"搜索笔记失败: {msg}"
    assert notes is not None
    assert len(notes) > 0
    
    print(f"共搜索到 {len(notes)} 条结果")
    for i, note in enumerate(notes[:3]):
        print(f"{i+1}. {note.get('title', '无标题')}")
        


# 在测试函数开始之前添加
def verify_node_modules():
    import os
    node_path = os.environ.get("NODE_PATH", "未设置")
    print(f"NODE_PATH: {node_path}")
    
    # 检查目录是否存在
    if node_path != "未设置":
        jsdom_path = os.path.join(node_path, "jsdom")
        if os.path.exists(jsdom_path):
            print(f"jsdom 模块目录存在: {jsdom_path}")
        else:
            print(f"ERROR: jsdom 模块目录不存在: {jsdom_path}")
    
    # 尝试使用 Node.js 检查模块是否可用
    import subprocess
    try:
        result = subprocess.run(
            ["node", "-e", "try { require('jsdom'); console.log('jsdom module found'); } catch(e) { console.error(e.message); }"],
            capture_output=True, text=True, check=False
        )
        print(f"Node.js 检查结果: {result.stdout or result.stderr}")
    except Exception as e:
        print(f"执行 Node.js 检查时出错: {e}")



if __name__ == "__main__":
    verify_node_modules()

    # 直接运行测试
    print("测试获取笔记信息...")
    test_get_note_info()
    print("\n测试搜索笔记...")
    test_search_notes()


# 在测试前调用此函数
# verify_node_modules()









核心问题与解决方案
我们成功将 Spider_XHS 作为子模块集成到您的项目中，主要解决了以下几个关键问题：
1. 模块路径与导入问题

问题：Python 无法正确导入子模块中的代码
解决方案：使用动态路径计算，确保无论从项目的哪个位置调用，都能正确找到 Spider_XHS 的模块

2. Node.js 依赖问题

问题：PyExecJS 找不到 jsdom 模块
解决方案：设置 NODE_PATH 环境变量，明确指向 Spider_XHS 子模块的 node_modules 目录

3. JavaScript 依赖文件路径问题

问题：JavaScript 文件中的相对路径引用在不同执行环境下失效
解决方案：在 JS 代码中穷举可能的文件路径组合，通过多层 try-catch 确保至少一个路径能成功

关键实现细节
服务封装类设计
pythonCopy# src/services/xhs_service.py
class XHSService:
    def __init__(self, cookies_file=None):
        """初始化服务并加载配置"""
        # 加载依赖和配置...

    def get_note_info(self, note_url, proxies=None):
        """获取小红书笔记信息"""
        # 调用 Spider_XHS API...

    def search_notes(self, keyword, limit=5, proxies=None):
        """搜索小红书笔记"""
        # 调用 Spider_XHS 搜索功能...
环境变量设置
pythonCopy# 设置 NODE_PATH 环境变量指向正确的 node_modules 目录
os.environ["NODE_PATH"] = str(Path(__file__).parent.parent.parent / "src" / "libs" / "spider_xhs" / "node_modules")
JavaScript 文件路径解析
通过在 JavaScript 代码中使用多层 try-catch 穷举可能的路径：
javascriptCopytry {
    require('./xhs_xray_pack1.js');
} catch (e) {
    try {
        require('../static/xhs_xray_pack1.js');
    } catch (e) {
        // 更多路径尝试...
    }
}
优点与局限性
优点

松耦合集成：作为子模块集成，便于后续更新
保持原始功能：保留了 Spider_XHS 的全部功能
简单直接：解决方案直接明了，不需要复杂的抽象

局限性

依赖原始代码：与 Spider_XHS 项目紧密相关，如果原项目有重大更新可能需要调整
路径处理简单但不优雅：穷举路径的方法虽然有效，但未来可能需要更优雅的解决方案

后续建议

完善错误处理：为各种可能的异常添加更详细的处理和日志
增加功能覆盖：逐步封装 Spider_XHS 的更多功能
配置集中管理：将路径、Cookie等配置集中管理，提高可维护性
添加验证机制：增加 Cookie 有效性验证和自动重试功能
扩展测试覆盖：编写更多测试用例，覆盖各种场景和边界情况

这个集成方案成功地解决了最初的技术问题，使您能够在项目中利用 Spider_XHS 的功能获取小红书的数据。通过测试验证，集成后的功能可以正常工作。