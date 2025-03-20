import asyncio
import json
import os
import sys

# 确保可以导入XHSDownloader
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from xhs_downloader import XHSDownloader


        # "https://www.xiaohongshu.com/explore/64674a91000000001301762e?xsec_token=ABAJcy_294mBZauFhAac6izmJvYB6yqm49MAtXSVU8XA4=&xsec_source=pc_feed",

async def test_xhs_downloader():
    test_urls = [
        # 建议使用最新的有效链接
        # "https://www.xiaohongshu.com/explore/64674a91000000001301762e?xsec_token=ABAJcy_294mBZauFhAac6izmJvYB6yqm49MAtXSVU8XA4=&xsec_source=pc_feed",
        "https://www.xiaohongshu.com/explore/64674a91000000001301762e",
    ]


    # 初始化下载器
    downloader = XHSDownloader(
        # 如果需要代理，使用这种方式
        # proxy="http://127.0.0.1:7890"  # 取消注释并配置代理
    )

    # 创建下载目录
    download_dir = os.path.join(os.path.dirname(__file__), 'xhs_downloads')
    os.makedirs(download_dir, exist_ok=True)

    # 测试结果
    test_results = []

    # 逐个测试链接
    for url in test_urls:
        print(f"\n🔍 正在测试链接: {url}")
        
        test_result = {
            "url": url,
            "info_extracted": False,
            "images_downloaded": False,
            "video_downloaded": False,
            "error": None
        }
        
        try:
            # 提取作品信息
            note_info = await downloader.extract_note_info(url)
            
            if not note_info:
                print(f"❌ 无法提取 {url} 的信息")
                test_result["error"] = "无法提取作品信息"
                test_results.append(test_result)
                continue
            
            test_result["info_extracted"] = True
            
            # 打印提取的信息
            print("📋 作品信息:")
            print(json.dumps(note_info, ensure_ascii=False, indent=2))
            
            # 下载图片
            if note_info['images']:
                print("\n📸 正在下载图片...")
                image_paths = await downloader.download_images(
                    note_info['images'], 
                    save_path=os.path.join(download_dir, 'images')
                )
                print("已下载图片:", image_paths)
                test_result["images_downloaded"] = bool(image_paths)
            
            # 下载视频
            if note_info['video']:
                print("\n🎥 正在下载视频...")
                video_path = await downloader.download_video(
                    note_info['video'], 
                    save_path=os.path.join(download_dir, 'videos')
                )
                print("已下载视频:", video_path)
                test_result["video_downloaded"] = bool(video_path)
        
        except Exception as e:
            print(f"❌ 测试 {url} 时发生错误: {e}")
            test_result["error"] = str(e)
        
        test_results.append(test_result)

    # 打印测试总结
    print("\n🏁 测试总结:")
    for result in test_results:
        print(f"链接: {result['url']}")
        print(f"信息提取: {'✅ 成功' if result['info_extracted'] else '❌ 失败'}")
        print(f"图片下载: {'✅ 成功' if result['images_downloaded'] else '❌ 失败'}")
        print(f"视频下载: {'✅ 成功' if result['video_downloaded'] else '❌ 失败'}")
        if result['error']:
            print(f"错误信息: {result['error']}")
        print("---")

# 主测试入口
def main():
    print("🚀 XHS-Downloader 测试开始")
    asyncio.run(test_xhs_downloader())
    print("\n🏁 XHS-Downloader 测试结束")

if __name__ == "__main__":
    main()