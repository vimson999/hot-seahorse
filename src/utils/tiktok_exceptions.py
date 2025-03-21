class TikTokDownloadError(Exception):
    """TikTok 下载异常"""
    def __init__(self, message, error_code=20001):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class VideoNotFoundError(TikTokDownloadError):
    """视频未找到异常"""
    def __init__(self, url):
        super().__init__(f"未能下载指定链接的视频: {url}", error_code=20002)

class DownloadLimitError(TikTokDownloadError):
    """下载限制异常"""
    def __init__(self, reason):
        super().__init__(f"视频下载受限: {reason}", error_code=20003)