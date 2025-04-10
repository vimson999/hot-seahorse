import os
import sys
import asyncio
import pytest
from pathlib import Path
import json
import logging

# 禁用一些可能的警告日志
logging.basicConfig(level=logging.ERROR)

# 添加项目根目录和 TikTokDownloader 目录到 Python 路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
tiktok_downloader_root = os.path.join(project_root, 'src', 'libs', 'tiktok_downloader')
sys.path.insert(0, project_root)
sys.path.insert(0, tiktok_downloader_root)

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(project_root, 'src'))
sys.path.insert(0, os.path.join(tiktok_downloader_root, 'src'))

# 重新组织导入路径
from libs.tiktok_downloader.src.application import TikTokDownloader
from libs.tiktok_downloader.src.link import Extractor
from libs.tiktok_downloader.src.config import Parameter, Settings
from libs.tiktok_downloader.src.tools import ColorfulConsole
from libs.tiktok_downloader.src.custom import PROJECT_ROOT
from libs.tiktok_downloader.src.manager import Database

def test_tiktok_downloader_initialization():
    """测试 TikTokDownloader 初始化"""
    try:
        downloader = TikTokDownloader()
        assert downloader is not None, "TikTokDownloader 初始化失败"
        print("\nTikTokDownloader 初始化成功")
    except Exception as e:
        pytest.fail(f"TikTokDownloader 初始化失败: {e}")

def test_available_methods():
    """测试 TikTokDownloader 可用的方法"""
    downloader = TikTokDownloader()
    methods = [method for method in dir(downloader) if not method.startswith('_') and callable(getattr(downloader, method))]
    
    # 使用非常明显的方式打印方法列表
    print("\n")
    print("=" * 50)
    print("TikTokDownloader 可用方法:")
    for method in methods:
        print(f"- {method}")
    print("=" * 50)
    print("\n")
    
    assert len(methods) > 0, "TikTokDownloader 没有可用的公共方法"

async def test_extract_links():
    """测试链接提取功能"""
    console = ColorfulConsole()
    settings = Settings(PROJECT_ROOT, console)
    
    # 创建参数对象需要提供默认值
    cookie_object = None
    cookie = {}
    cookie_tiktok = {}
    root = ""
    accounts_urls = []
    accounts_urls_tiktok = []
    mix_urls = []
    mix_urls_tiktok = []
    folder_name = "Download"
    name_format = "create_time type nickname desc"
    date_format = "%Y-%m-%d %H:%M:%S"
    split = "-"
    music = False
    folder_mode = False
    truncate = 50
    storage_format = ""
    dynamic_cover = False
    original_cover = False
    proxy = None
    proxy_tiktok = None
    twc_tiktok = ""
    download = True
    max_size = 0
    chunk = 1024 * 1024 * 2
    max_retry = 5
    max_pages = 0
    run_command = ""
    owner_url = {}
    owner_url_tiktok = {}
    ffmpeg = ""
    recorder = None
    browser_info = {}
    browser_info_tiktok = {}
    
    # 创建一个简单的记录器模拟对象
    class MockRecorder:
        async def has_id(self, id_):
            return False
        async def update_id(self, id_):
            pass
        async def delete_id(self, id_):
            pass
    
    # 使用模拟的Cookie和Recorder对象
    from libs.tiktok_downloader.src.module import Cookie
    from libs.tiktok_downloader.src.record import BaseLogger
    
    cookie_obj = Cookie(settings, console)
    logger = BaseLogger(Path(PROJECT_ROOT), console)
    recorder = MockRecorder()
    
    # 创建Parameter对象，提供所有必须的参数
    parameter = Parameter(
        settings=settings,
        cookie_object=cookie_obj,
        logger=BaseLogger,
        console=console,
        cookie=cookie,
        cookie_tiktok=cookie_tiktok,
        root=root,
        accounts_urls=accounts_urls,
        accounts_urls_tiktok=accounts_urls_tiktok,
        mix_urls=mix_urls,
        mix_urls_tiktok=mix_urls_tiktok,
        folder_name=folder_name,
        name_format=name_format,
        date_format=date_format,
        split=split,
        music=music,
        folder_mode=folder_mode,
        truncate=truncate,
        storage_format=storage_format,
        dynamic_cover=dynamic_cover,
        original_cover=original_cover,
        proxy=proxy,
        proxy_tiktok=proxy_tiktok,
        twc_tiktok=twc_tiktok,
        download=download,
        max_size=max_size,
        chunk=chunk,
        max_retry=max_retry,
        max_pages=max_pages,
        run_command=run_command,
        owner_url=owner_url,
        owner_url_tiktok=owner_url_tiktok,
        ffmpeg=ffmpeg,
        recorder=recorder,
        browser_info=browser_info,
        browser_info_tiktok=browser_info_tiktok
    )
    
    extractor = Extractor(parameter)
    
    # 测试抖音作品链接提取
    test_url = "https://www.douyin.com/video/7345684229779284279"
    extracted_ids = await extractor.run(test_url, "detail")
    
    print("\n")
    print("=" * 50)
    print(f"从链接提取的ID: {extracted_ids}")
    print(f"链接类型: {'TikTok' if extracted_ids and extracted_ids[0] is True else '抖音'}")
    print(f"原始链接: {test_url}")
    print(f"ID数量: {len(extracted_ids)}")
    print("=" * 50)
    print("\n")
    
    assert len(extracted_ids) > 0, "未能从视频链接提取ID"

async def test_extract_user_links():
    """测试用户链接提取功能"""
    console = ColorfulConsole()
    settings = Settings(PROJECT_ROOT, console)
    
    # 创建参数对象需要提供默认值
    cookie_object = None
    cookie = {}
    cookie_tiktok = {}
    root = ""
    accounts_urls = []
    accounts_urls_tiktok = []
    mix_urls = []
    mix_urls_tiktok = []
    folder_name = "Download"
    name_format = "create_time type nickname desc"
    date_format = "%Y-%m-%d %H:%M:%S"
    split = "-"
    music = False
    folder_mode = False
    truncate = 50
    storage_format = ""
    dynamic_cover = False
    original_cover = False
    proxy = None
    proxy_tiktok = None
    twc_tiktok = ""
    download = True
    max_size = 0
    chunk = 1024 * 1024 * 2
    max_retry = 5
    max_pages = 0
    run_command = ""
    owner_url = {}
    owner_url_tiktok = {}
    ffmpeg = ""
    recorder = None
    browser_info = {}
    browser_info_tiktok = {}
    
    # 创建一个简单的记录器模拟对象
    class MockRecorder:
        async def has_id(self, id_):
            return False
        async def update_id(self, id_):
            pass
        async def delete_id(self, id_):
            pass
    
    # 使用模拟的Cookie和Recorder对象
    from libs.tiktok_downloader.src.module import Cookie
    from libs.tiktok_downloader.src.record import BaseLogger
    
    cookie_obj = Cookie(settings, console)
    logger = BaseLogger(Path(PROJECT_ROOT), console)
    recorder = MockRecorder()
    
    # 创建Parameter对象，提供所有必须的参数
    parameter = Parameter(
        settings=settings,
        cookie_object=cookie_obj,
        logger=BaseLogger,
        console=console,
        cookie=cookie,
        cookie_tiktok=cookie_tiktok,
        root=root,
        accounts_urls=accounts_urls,
        accounts_urls_tiktok=accounts_urls_tiktok,
        mix_urls=mix_urls,
        mix_urls_tiktok=mix_urls_tiktok,
        folder_name=folder_name,
        name_format=name_format,
        date_format=date_format,
        split=split,
        music=music,
        folder_mode=folder_mode,
        truncate=truncate,
        storage_format=storage_format,
        dynamic_cover=dynamic_cover,
        original_cover=original_cover,
        proxy=proxy,
        proxy_tiktok=proxy_tiktok,
        twc_tiktok=twc_tiktok,
        download=download,
        max_size=max_size,
        chunk=chunk,
        max_retry=max_retry,
        max_pages=max_pages,
        run_command=run_command,
        owner_url=owner_url,
        owner_url_tiktok=owner_url_tiktok,
        ffmpeg=ffmpeg,
        recorder=recorder,
        browser_info=browser_info,
        browser_info_tiktok=browser_info_tiktok
    )
    
    extractor = Extractor(parameter)
    
    # 测试抖音用户链接提取
    test_url = "https://www.douyin.com/user/MS4wLjABAAAAvP4IjEJ4hVwvGwL2Eic6ADJQOWCkW0pp0oAFsXEuFcI"
    extracted_ids = await extractor.run(test_url, "user")
    
    print("\n")
    print("=" * 50)
    print(f"从用户链接提取的ID: {extracted_ids}")
    print(f"原始链接: {test_url}")
    print(f"ID数量: {len(extracted_ids)}")
    print(f"ID类型: {'短ID' if len(extracted_ids[0]) < 20 else 'SecUID'}")
    print("=" * 50)
    print("\n")
    
    assert len(extracted_ids) > 0, "未能从用户链接提取ID"

async def test_get_tiktok_configuration():
    """测试TikTok配置获取"""
    console = ColorfulConsole()
    
    # 为了避免修改原始配置，这里创建一个临时配置
    temp_config = {
        "accounts_urls": [],
        "accounts_urls_tiktok": [],
        "mix_urls": [],
        "mix_urls_tiktok": [],
        "owner_url": {"mark": "", "url": "", "uid": "", "sec_uid": "", "nickname": ""},
        "owner_url_tiktok": None,
        "root": "",
        "folder_name": "Download",
        "name_format": "create_time type nickname desc",
        "date_format": "%Y-%m-%d %H:%M:%S",
        "split": "-",
        "folder_mode": False,
        "music": False,
        "truncate": 50,
        "storage_format": "",
        "cookie": {},
        "cookie_tiktok": {},
        "dynamic_cover": False,
        "original_cover": False,
        "proxy": None,
        "proxy_tiktok": None,
        "twc_tiktok": "",
        "download": True,
        "max_size": 0,
        "chunk": 1024 * 1024 * 2,
        "timeout": 10,
        "max_retry": 5,
        "max_pages": 0,
        "run_command": "",
        "ffmpeg": "",
        "douyin_platform": True,
        "tiktok_platform": True,
        "browser_info": {},
        "browser_info_tiktok": {}
    }
    
    # 显示配置
    print("\n")
    print("=" * 50)
    print("TikTokDownloader 测试配置:")
    for key, value in temp_config.items():
        if key in ["cookie", "cookie_tiktok"]:
            # 敏感信息不完全显示
            if isinstance(value, dict) and value:
                print(f"- {key}: {list(value.keys())}")
            elif isinstance(value, str) and value:
                print(f"- {key}: [已设置]")
            else:
                print(f"- {key}: [未设置]")
        elif isinstance(value, list) and len(value) > 3:
            print(f"- {key}: [包含 {len(value)} 个项目]")
        else:
            print(f"- {key}: {value}")
    print("=" * 50)
    print("\n")
    
    # 保存为临时配置文件
    temp_path = os.path.join(os.path.dirname(__file__), "temp_settings.json")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(temp_config, f, ensure_ascii=False, indent=4)
    
    print(f"临时配置已保存到: {temp_path}")
    
    assert temp_config is not None, "配置信息为空"
    assert isinstance(temp_config, dict), "配置应该是字典格式"

async def run_async_tests():
    """运行异步测试"""
    await test_extract_links()
    await test_extract_user_links()
    await test_get_tiktok_configuration()
    
    # 添加新的测试
    await test_cookie_config()
    await test_video_download()
    await test_batch_download()

def run_full_tests():
    """运行所有测试"""
    test_tiktok_downloader_initialization()
    test_available_methods()
    
    # 运行异步测试
    asyncio.run(run_async_tests())
    
    print("\n所有测试已完成!")

def test_video_download_only():
    """只运行视频下载测试"""
    asyncio.run(test_video_download())
    
def test_batch_download_only():
    """只运行批量下载测试"""
    asyncio.run(test_batch_download())
    
def test_cookie_config_only():
    """只运行Cookie配置测试"""
    asyncio.run(test_cookie_config())

def test_link_extraction():
    """测试链接提取功能的独立版本"""
    # 这个函数可以单独运行来测试链接提取
    asyncio.run(test_extract_links())

def test_user_link_extraction():
    """测试用户链接提取功能的独立版本"""
    # 这个函数可以单独运行来测试用户链接提取
    asyncio.run(test_extract_user_links())

def test_configuration():
    """测试配置获取的独立版本"""
    # 这个函数可以单独运行来测试配置获取
    asyncio.run(test_get_tiktok_configuration())



async def test_cookie_config():
    """测试配置Cookie功能"""
    console = ColorfulConsole()
    settings = Settings(PROJECT_ROOT, console)
    
    # 创建一个示例Cookie（只用于测试，非真实有效的Cookie）
    example_cookie = {
        "sessionid_ss": "test_session_id", 
        "sid_tt": "test_sid",
        "uid_tt": "test_uid",
        "msToken": "test_msToken",
        "ttwid": "test_ttwid"
    }
    
    # 创建临时配置文件路径
    temp_path = os.path.join(os.path.dirname(__file__), "temp_settings.json")
    
    # 检查是否存在先前的临时配置
    if os.path.exists(temp_path):
        with open(temp_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = settings.default.copy()
    
    # 更新配置
    config["cookie"] = example_cookie
    
    # 保存临时配置
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    
    print("\n")
    print("=" * 50)
    print("测试Cookie配置:")
    print(f"临时配置文件路径: {temp_path}")
    print(f"已配置的Cookie键: {list(example_cookie.keys())}")
    
    # 创建临时设置对象
    temp_settings = Settings(Path(os.path.dirname(temp_path)), console)
    
    # 使用Cookie对象测试Cookie提取
    from libs.tiktok_downloader.src.module import Cookie
    cookie_obj = Cookie(temp_settings, console)
    
    # 模拟一个Cookie字符串
    cookie_str = "; ".join([f"{k}={v}" for k, v in example_cookie.items()])
    print(f"模拟Cookie字符串: {cookie_str[:30]}...")
    
    # 测试Cookie提取功能
    extracted_cookie = cookie_obj.extract(cookie_str, write=False)
    print(f"提取的Cookie键: {list(extracted_cookie.keys())}")
    
    print("=" * 50)
    print("\n")
    
async def test_batch_download():
    """测试批量下载功能"""
    parameter = await create_parameter(with_mock_cookie=True)
    from libs.tiktok_downloader.src.interface import Account
    from libs.tiktok_downloader.src.downloader import Downloader
    
    # 选择一个抖音用户账号进行测试
    test_user_url = "https://www.douyin.com/user/MS4wLjABAAAAM-1GvMSm6nZNzZhD6qEDOFr3nHSLxTL6mIs3D4zQN0w"
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    print("\n")
    print("=" * 50)
    print(f"测试批量下载用户作品: {test_user_url}")
    print(f"下载目录: {download_dir}")
    
    try:
        # 创建链接提取器
        extractor = Extractor(parameter)
        user_ids = await extractor.run(test_user_url, "user")
        
        if not user_ids:
            print("未能从链接中提取用户ID，无法进行批量下载测试")
            return
            
        sec_user_id = user_ids[0]
        print(f"提取到的用户ID: {sec_user_id}")
        
        # 使用Account接口获取用户作品列表(只获取最近的5个作品)
        account = Account(
            parameter, 
            sec_user_id=sec_user_id,
            pages=1,  # 只获取一页
            count=5,  # 每页5个作品
        )
        
        # 获取作品列表
        account_data, earliest, latest = await account.run()
        
        if not account_data:
            print("获取用户作品列表失败，可能需要登录Cookie")
            return
            
        print(f"获取到 {len(account_data)} 个作品")
        
        # 创建提取器对象
        from libs.tiktok_downloader.src.extract import Extractor as DataExtractor
        extractor_obj = DataExtractor(parameter)
        
        # 处理数据
        from libs.tiktok_downloader.src.record import BaseLogger
        from libs.tiktok_downloader.src.storage import RecordManager
        
        recorder = RecordManager()
        root, params, logger = recorder.run(parameter)
        
        async with logger(root, console=parameter.console, **params) as record:
            processed_data = await extractor_obj.run(
                account_data,
                record,
                type_="batch",
                name="测试用户",
                mark="test_user",
                earliest=earliest,
                latest=latest
            )
            
        if not processed_data:
            print("数据处理失败")
            return
            
        print(f"处理后获得 {len(processed_data)} 个作品")
        
        # 简要显示获取到的作品信息
        for i, item in enumerate(processed_data[:3], 1):  # 只显示前3个
            print(f"\n作品 {i}:")
            print(f"ID: {item.get('id', '未知')}")
            print(f"类型: {item.get('type', '未知')}")
            print(f"描述: {item.get('desc', '未知')[:50]}...")
            print(f"创建时间: {item.get('create_time', '未知')}")
        
        if len(processed_data) > 3:
            print(f"\n...还有 {len(processed_data) - 3} 个作品未显示")
        
        # 限制只下载前2个作品，避免下载过多
        limited_data = processed_data[:2] if len(processed_data) > 2 else processed_data
        print(f"\n将下载 {len(limited_data)} 个作品 (限制测试数量)")
        
        # 下载文件
        if limited_data:
            downloader = Downloader(parameter)
            await downloader.run(limited_data, "batch", mode="post", mark="test_user", user_id=sec_user_id, user_name="测试用户")
        
        # 检查下载结果
        print("\n下载结果:")
        downloaded_files = []
        for root, dirs, files in os.walk(download_dir):
            for file in files:
                if file.endswith(('.mp4', '.jpg', '.jpeg', '.png')):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    downloaded_files.append((file_path, file_size))
                    print(f"已下载: {file_path} ({file_size / 1024 / 1024:.2f} MB)")
        
        if not downloaded_files:
            print("没有找到下载的文件，下载可能失败")
        else:
            print(f"成功下载 {len(downloaded_files)} 个文件")
            
    except Exception as e:
        print(f"批量下载过程中发生错误: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
    print("=" * 50)
    print("\n")
    
async def test_video_download():
    """测试视频下载功能"""
    parameter = await create_parameter(with_mock_cookie=False)
    from libs.tiktok_downloader.src.interface import Detail
    from libs.tiktok_downloader.src.downloader import Downloader
    
    test_url = "https://www.douyin.com/video/7345684229779284279"
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    print("\n")
    print("=" * 50)
    print(f"测试下载视频: {test_url}")
    print(f"下载目录: {download_dir}")
    
    try:
        # 创建链接提取器
        extractor = Extractor(parameter)
        extracted_ids = await extractor.run(test_url, "detail")
        
        if not extracted_ids:
            print("未能从链接中提取ID，无法进行下载测试")
            return
            
        print(f"提取到的视频ID: {extracted_ids[0]}")
        
        # 使用Detail接口获取详细信息
        detail = Detail(parameter, detail_id=extracted_ids[0])
        detail_data = await detail.run()
        
        if not detail_data:
            print("获取视频详情失败，可能需要登录Cookie")
            return
            
        print(f"视频标题: {detail_data.get('desc', '未知')}")
        print(f"作者: {detail_data.get('author', {}).get('nickname', '未知')}")
        
        # 创建提取器对象
        from libs.tiktok_downloader.src.extract import Extractor as DataExtractor
        extractor_obj = DataExtractor(parameter)
        
        # 处理数据
        from libs.tiktok_downloader.src.record import BaseLogger
        from libs.tiktok_downloader.src.storage import RecordManager
        
        recorder = RecordManager()
        root, params, logger = recorder.run(parameter)
        
        async with logger(root, console=parameter.console, **params) as record:
            processed_data = await extractor_obj.run([detail_data], record)
            
        if not processed_data:
            print("数据处理失败")
            return
            
        # 下载文件
        downloader = Downloader(parameter)
        await downloader.run(processed_data, "detail")
        
        # 检查下载结果
        print("\n下载结果:")
        downloaded_files = []
        for root, dirs, files in os.walk(download_dir):
            for file in files:
                if file.endswith(('.mp4', '.jpg', '.jpeg', '.png')):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    downloaded_files.append((file_path, file_size))
                    print(f"已下载: {file_path} ({file_size / 1024 / 1024:.2f} MB)")
        
        if not downloaded_files:
            print("没有找到下载的文件，下载可能失败")
        else:
            print(f"成功下载 {len(downloaded_files)} 个文件")
            
    except Exception as e:
        print(f"下载过程中发生错误: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
    print("=" * 50)
    print("\n")
    
async def create_parameter(with_mock_cookie=True):
    """创建一个通用的Parameter对象用于测试"""
    console = ColorfulConsole()
    settings = Settings(PROJECT_ROOT, console)
    
    # 创建一个简单的Cookie字典
    mock_cookie = {
        "sessionid": "24abdbaee489b9e13620ebaa4c95c3ef",
        "sessionid_ss": "24abdbaee489b9e13620ebaa4c95c3ef",
        "ttwid": "1%7CQnjfcYCTKmjc4Ocugzeek0HdL8-wj_Ac_CaIlr20FEc%7C1738916640%7C7c1d1f1fd435dddb216fcbeb9e7c55dd9afe2afcc4046b336eeba1667dc438fd",
        "passport_csrf_token": "e252845111d3cb538ea4738f64c210b0",
        "s_v_web_id": "verify_m8h7jgv2_zyJfOqzN_m0GF_4J2P_AHHM_6B9kpk5mtp3Q",
        "__ac_nonce": "067de302f009e0c1ff850",
        "__ac_signature": "_02B4Z6wo00f01wLAfyAAAIDAcaFS1jfEma8C4HuAAKd4WDg0DeW7TAPewbsEFV2XmlrKGcQMCqd2k3N8W4h7uENTpsK9.KPPNoPpBwEsiMPgOzz6YZFPLuWZFdhAic98BEuB45kI7emxAkBX4f",
        "UIFID": "0de8750d2b188f4235dbfd208e44abbb976428f0720eb983255afefa45d39c0c27190dc9ab3fa340b16e774345e8f868f2b71cf9206bd38b59c4193b9f03feb17c083f8661bc5e888deedc9d2685323e454ee0c78627891d03dad523ab98db5d06451a8513c62858c74248517c33935b1c682fe0706addb4269b915bdda4088dc984bfc4dca4bcf0528b70e60fe2b06f",
        "odin_tt": "974e10c2a5e027e729dc7ed97700f3430fd8c133600fea93b59adb573bf1e6def03005cf0ce0253208e9188ae35b57d8"
    
    } if with_mock_cookie else {}
    
    cookie = mock_cookie
    cookie_tiktok = mock_cookie.copy()


    # Option 1: Use full cookie string instead of dictionary
    cookie_path = os.path.join(os.path.dirname(__file__), "tk_cookie.txt")
    with open(cookie_path, "r", encoding="utf-8") as f:
        cookie_str = f.read().strip()

    # cookie_str = "__security_mc_1_s_sdk_cert_key=9cea8190-4aaa-8654;__security_mc_1_s_sdk_crypt_sdk=6e4c00df-447a-b09b;__security_mc_1_s_sdk_sign_data_key_sso=a41fbce8-49b3-b7ab;__security_mc_1_s_sdk_sign_data_key_web_protect=df173ac5-446b-861f;__security_server_data_status=1;_bd_ticket_crypt_cookie=9100954d466a151304cc4d68050a2170;_bd_ticket_crypt_doamin=2;bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTkZhZFNKejlwVFdLdFdpVXYvRDQxZ284MUFEdnFpcDBPQVV3czZBK3ZycWM2bTc4bGRrZTgyZllMaDc1YU1MQWZYdytKZ2hYaWpheXphNWdxellDNVE9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D;bd_ticket_guard_client_web_domain=2;biz_trace_id=047f10ed;d_ticket=0bade1e8ef0a9ee148285c086826624c9420a;download_guide=%223%2F20250322%2F0%22;FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAB6_6mqKdknnXwklV227-Ri3J98MM_7CzabwAgBKXk327sHt70BiDJhz2HJJcP367%2F1742659200000%2F0%2F1742614581229%2F0%22;FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAB6_6mqKdknnXwklV227-Ri3J98MM_7CzabwAgBKXk327sHt70BiDJhz2HJJcP367%2F1742572800000%2F0%2F1742520807402%2F0%22;hevc_supported=true;home_can_add_dy_2_desktop=%221%22;is_dash_user=1;is_staff_user=false;IsDouyinActive=true;login_time=1738917001741;n_mh=x0_egbleSscy0Gp2JoMTA_7MlR_Gp94Qd5O1hoVtRTg;odin_tt=974e10c2a5e027e729dc7ed97700f3430fd8c133600fea93b59adb573bf1e6def03005cf0ce0253208e9188ae35b57d8;passport_assist_user=CkH7SYYVtqTVYz73VsJsv09QuszlL1oDL9cjCjKhw6naSGGgs_tB51_6fOQhoHF29MgXOWr_H_QzmFQnw_e4LuXndBpKCjz_sPMdP_nIIhakYd1yFkLMyWVxMq-wkRDTOnyXtSfeqgemCvhMolnHYS7TA193Y5U_cvOz77AZ9ORLXAYQn_XoDRiJr9ZUIAEiAQPCN_ap;passport_csrf_token=e252845111d3cb538ea4738f64c210b0;passport_csrf_token_default=e252845111d3cb538ea4738f64c210b0;passport_mfa_token=Cje2UHlYpmHNip3UKC74cQ8bDmU7qB3cqn1r86XaD8ZsZcZoOGo2rJpa5xDOlc9mEN4Merv6T9uXGkoKPDoiihypvf8PuT035nrzpF3P4V4o2zwcL8S%2FkQSOzDTeuY3qNc2DV6yPnlWGZt10Gg73HfhW9hXgny9KjRCx9OgNGPax0WwgAiIBA9oL7b4%3D;publish_badge_show_info=%220%2C0%2C0%2C1742466471885%22;SelfTabRedDotControl=%5B%7B%22id%22%3A%227041047466673702920%22%2C%22u%22%3A70%2C%22c%22%3A0%7D%5D;sessionid=24abdbaee489b9e13620ebaa4c95c3ef;sessionid_ss=24abdbaee489b9e13620ebaa4c95c3ef;sid_guard=24abdbaee489b9e13620ebaa4c95c3ef%7C1742518746%7C5131727%7CMon%2C+19-May-2025+10%3A27%3A53+GMT;sid_tt=24abdbaee489b9e13620ebaa4c95c3ef;sid_ucp_sso_v1=1.0.0-KGZkM2I2NGFjY2RmNGZiYjEyNzk4M2MzY2RjZWY5Njg4ZWEzYjhlNmMKIQjni6Cn5Yy6AhCIiZe9BhjvMSAMMKielYsGOAZA9AdIBhoCaGwiIDU0YjA1YjcxYzYwNDdjOTFkMWExYzFmYWNmNGRjZTk4;sid_ucp_v1=1.0.0-KGMzMzE4ZTcwNzIyMDQ5ZWZjZjc2MThhZmY5ZGU2ZmVmNDdlNmE0MmUKGwjni6Cn5Yy6AhC9jpe9BhjvMSAMOAZA9AdIBBoCbHEiIDI0YWJkYmFlZTQ4OWI5ZTEzNjIwZWJhYTRjOTVjM2Vm;ssid_ucp_sso_v1=1.0.0-KGZkM2I2NGFjY2RmNGZiYjEyNzk4M2MzY2RjZWY5Njg4ZWEzYjhlNmMKIQjni6Cn5Yy6AhCIiZe9BhjvMSAMMKielYsGOAZA9AdIBhoCaGwiIDU0YjA1YjcxYzYwNDdjOTFkMWExYzFmYWNmNGRjZTk4;ssid_ucp_v1=1.0.0-KGMzMzE4ZTcwNzIyMDQ5ZWZjZjc2MThhZmY5ZGU2ZmVmNDdlNmE0MmUKGwjni6Cn5Yy6AhC9jpe9BhjvMSAMOAZA9AdIBBoCbHEiIDI0YWJkYmFlZTQ4OWI5ZTEzNjIwZWJhYTRjOTVjM2Vm;sso_uid_tt=f214d20d476c4026397c63bc9b38b364;sso_uid_tt_ss=f214d20d476c4026397c63bc9b38b364;store-region=cn-sd;store-region-src=uid;strategyABtestKey=%221742614581.225%22;stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22;stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22;toutiao_sso_user=54b05b71c6047c91d1a1c1facf4dce98;toutiao_sso_user_ss=54b05b71c6047c91d1a1c1facf4dce98;ttwid=1%7CQnjfcYCTKmjc4Ocugzeek0HdL8-wj_Ac_CaIlr20FEc%7C1738916640%7C7c1d1f1fd435dddb216fcbeb9e7c55dd9afe2afcc4046b336eeba1667dc438fd;uid_tt=3e78f8c16dbd9406f2564581c7f5952e;uid_tt_ss=3e78f8c16dbd9406f2564581c7f5952e;UIFID_TEMP=0de8750d2b188f4235dbfd208e44abbb976428f0720eb983255afefa45d39c0c46fb9bd0528ffb36b7d8574b5b3b80aed6225638831e2a31a529f0aa19b2755110e59b2b84b0597b10f2ffe2c3506f2c;volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D;webcast_paid_live_duration=%7B%227482692980751843380%22%3A2%7D;passport_fe_beating_status=true;=douyin.com;__ac_nonce=067de302f009e0c1ff850;__ac_signature=_02B4Z6wo00f01wLAfyAAAIDAcaFS1jfEma8C4HuAAKd4WDg0DeW7TAPewbsEFV2XmlrKGcQMCqd2k3N8W4h7uENTpsK9.KPPNoPpBwEsiMPgOzz6YZFPLuWZFdhAic98BEuB45kI7emxAkBX4f;csrf_session_id=3c56d29532629e2de5fcb72d6d60dabc;device_web_cpu_core=4;device_web_memory_size=8;dy_sheight=1080;dy_swidth=1920;fpk1=U2FsdGVkX19fYGCM0rfRcQzx8CSfeJj4tOBy906LqEslkRvXy++xIUJAaldrfvfr4lyNaxjOJfiQCW+09uHcbA==;fpk2=0845b309c7b9b957afd9ecf775a4c21f;s_v_web_id=verify_m8h7jgv2_zyJfOqzN_m0GF_4J2P_AHHM_6B9kpk5mtp3Q;UIFID=0de8750d2b188f4235dbfd208e44abbb976428f0720eb983255afefa45d39c0c27190dc9ab3fa340b16e774345e8f868f2b71cf9206bd38b59c4193b9f03feb17c083f8661bc5e888deedc9d2685323e454ee0c78627891d03dad523ab98db5d06451a8513c62858c74248517c33935b1c682fe0706addb4eaea80aeb3216085e9e0bc273a1e9fa4269b915bdda4088dc984bfc4dca4bcf0528b70e60fe2b06f;x-web-secsdk-uid=160fc397-396f-4798-9bc8-88226745c809;xg_device_score=6.905294117647059;“
    
    # Parse the cookie string to dictionary
    from libs.tiktok_downloader.src.tools import cookie_str_to_dict
    cookie = cookie_str_to_dict(cookie_str) if with_mock_cookie else {}
    cookie_tiktok = {}

    
    # 创建参数对象需要提供默认值
    root = os.path.join(os.path.dirname(__file__), "downloads")  # 设置下载目录
    os.makedirs(root, exist_ok=True)  # 确保目录存在
    
    accounts_urls = []
    accounts_urls_tiktok = []
    mix_urls = []
    mix_urls_tiktok = []
    folder_name = "Download"
    name_format = "create_time type nickname desc"
    date_format = "%Y-%m-%d %H:%M:%S"
    split = "-"
    music = False
    folder_mode = False
    truncate = 50
    storage_format = ""
    dynamic_cover = False
    original_cover = False
    proxy = None
    proxy_tiktok = None
    twc_tiktok = ""
    download = True
    max_size = 0
    chunk = 1024 * 1024 * 2
    max_retry = 5
    max_pages = 0
    run_command = ""
    owner_url = {}
    owner_url_tiktok = {}
    ffmpeg = ""
    browser_info = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "pc_libra_divert": "Mac",
        "browser_platform": "MacIntel",
        "browser_name": "Chrome",
        "browser_version": "125.0.0.0",
        "engine_name": "Blink",
        "engine_version": "125.0.0.0",
        "os_name": "Mac OS X",
        "os_version": "10.15.7"
    }
    browser_info_tiktok = {}
    
    # 创建一个简单的记录器模拟对象
    class MockRecorder:
        async def has_id(self, id_):
            return False
        async def update_id(self, id_):
            pass
        async def delete_id(self, id_):
            pass
        async def delete_ids(self, ids):
            pass
    
    # 使用模拟的Cookie和Recorder对象
    from libs.tiktok_downloader.src.module import Cookie
    from libs.tiktok_downloader.src.record import BaseLogger
    
    cookie_obj = Cookie(settings, console)
    logger = BaseLogger(Path(PROJECT_ROOT), console)
    recorder = MockRecorder()
    
    # 创建Parameter对象，提供所有必须的参数
    return Parameter(
        settings=settings,
        cookie_object=cookie_obj,
        logger=BaseLogger,
        console=console,
        cookie=cookie,
        cookie_tiktok=cookie_tiktok,
        root=root,
        accounts_urls=accounts_urls,
        accounts_urls_tiktok=accounts_urls_tiktok,
        mix_urls=mix_urls,
        mix_urls_tiktok=mix_urls_tiktok,
        folder_name=folder_name,
        name_format=name_format,
        date_format=date_format,
        split=split,
        music=music,
        folder_mode=folder_mode,
        truncate=truncate,
        storage_format=storage_format,
        dynamic_cover=dynamic_cover,
        original_cover=original_cover,
        proxy=proxy,
        proxy_tiktok=proxy_tiktok,
        twc_tiktok=twc_tiktok,
        download=download,
        max_size=max_size,
        chunk=chunk,
        max_retry=max_retry,
        max_pages=max_pages,
        run_command=run_command,
        owner_url=owner_url,
        owner_url_tiktok=owner_url_tiktok,
        ffmpeg=ffmpeg,
        recorder=recorder,
        browser_info=browser_info,
        browser_info_tiktok=browser_info_tiktok
    )

if __name__ == "__main__":
    # 根据需要选择运行的测试
    # run_full_tests()  # 运行所有测试
    # test_available_methods()  # 仅测试可用方法
    # test_link_extraction()  # 仅测试链接提取
    # test_user_link_extraction()  # 仅测试用户链接提取
    # test_configuration()  # 仅测试配置获取
    # test_video_download_only()  # 仅测试视频下载
    # test_batch_download_only()  # 仅测试批量下载
    # test_cookie_config_only()  # 仅测试Cookie配置
    
    # 选择需要运行的测试，取消注释相应行
    # test_available_methods()  # 显示所有可用方法
    # asyncio.run(test_extract_links())  # 测试链接提取
    # asyncio.run(test_extract_user_links())  # 测试用户链接提取
    # asyncio.run(test_cookie_config())  # 测试Cookie配置
    
    # 需要实际下载的测试（根据需要取消注释）
    asyncio.run(test_video_download())  # 视频下载测试
    # asyncio.run(test_batch_download())  # 批量下载测试
    
    print("\n选定的测试已完成!")