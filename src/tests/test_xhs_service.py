import pytest
from src.services.xhs_service import extract_xhs_content

def test_extract_xhs_content():
    # 替换为实际的小红书链接
    url = "https://www.xiaohongshu.com/explore/64674a91000000001301762e?xsec_token=ABAJcy_294mBZauFhAac6izmJvYB6yqm49MAtXSVU8XA4=&xsec_source=pc_feed"
    
    result = extract_xhs_content(url)
    
    assert result is not None
    assert '作品ID' in result
    assert '作品标题' in result
    print(result)