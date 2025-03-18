class XHSExtractError(Exception):
    """小红书内容提取异常"""
    def __init__(self, message, error_code=10001):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class ContentNotFoundError(XHSExtractError):
    """内容未找到异常"""
    def __init__(self, url):
        super().__init__(f"未能提取链接内容: {url}", error_code=10002)