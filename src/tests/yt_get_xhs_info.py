import yt_dlp
import json
import os # 用于检查 cookie 文件是否存在

# 小红书笔记链接
note_url = 'https://www.xiaohongshu.com/explore/64674a91000000001301762e?xsec_token=ABAJcy_294mBZauFhAac6izmJvYB6yqm49MAtXSVU8XA4=&xsec_source=pc_feed'

# --- 配置 Cookies ---
# !!! 重要 !!!
# 1. 访问 www.xiaohongshu.com 并登录你的账号。
# 2. 使用浏览器扩展程序 (如 Get cookies.txt LOCALLY, EditThisCookie 等) 导出 cookies.txt 文件。
# 3. 将文件路径替换到下面的变量中。如果文件不存在或路径错误，将不使用 cookies。
cookie_file_path = 'src/xhs_cookies.txt' # <--- 在这里替换你的 cookies 文件路径

ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    # 'verbose': True, # 如果失败，取消注释以查看详细日志
}

# 检查 cookie 文件是否存在，如果存在则添加到选项中
if os.path.exists(cookie_file_path):
    print(f"正在使用 Cookies 文件: {cookie_file_path}")
    ydl_opts['cookiefile'] = cookie_file_path
else:
    print("警告: 未找到 Cookies 文件或路径无效。提取可能会失败或信息不完整。")
    print(f"期望路径: {os.path.abspath(cookie_file_path)}")


print(f"\n尝试提取小红书信息: {note_url}")

try:
    # 创建 YoutubeDL 对象
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 使用 extract_info 获取信息 (不下载)
        info_dict = ydl.extract_info(note_url, download=False)

        # 打印获取到的信息 (JSON 格式)
        print("\n--- 提取到的信息 ---")
        print(json.dumps(info_dict, indent=4, ensure_ascii=False))

        # 如果成功，你可以根据这里的字段调整或创建适用于小红书的转换函数
        # standard_format_info = convert_xhs_info_to_standard_format(info_dict)
        # print("\n--- 尝试转换为标准格式 ---")
        # print(json.dumps(standard_format_info, indent=4, ensure_ascii=False))


except yt_dlp.utils.DownloadError as e:
    print(f"\n提取信息时出错 (DownloadError): {e}")
    print("这非常可能是因为需要有效的登录 Cookies。请确保已登录小红书，")
    print("导出了正确的 cookies.txt 文件，并更新了脚本中的 `cookie_file_path`。")
    print("也可能是笔记不存在或提取器需要更新。")
except Exception as e:
    print(f"\n发生未知错误: {e}")