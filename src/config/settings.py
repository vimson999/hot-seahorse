from dataclasses import dataclass
from typing import Optional

@dataclass
class XHSConfig:
    """小红书内容提取配置"""
    cookie: Optional[str] = None
    timeout: int = 10
    log_level: str = 'INFO'