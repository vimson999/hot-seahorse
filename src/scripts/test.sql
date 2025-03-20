
pip install -e .

pytest src/tests/test_xhs_service.py




请你仔细阅读这个项目代码
我需要你以首席研发测试专家的身份 分析提炼这个项目代码
将根据url提取信息的代码继承进我自己的项目
不要使用安装依赖的方式

这是我目前用来测试功能的项目结构


    url = "https://www.xiaohongshu.com/explore/64674a91000000001301762e?xsec_token=ABAJcy_294mBZauFhAac6izmJvYB6yqm49MAtXSVU8XA4=&xsec_source=pc_feed"


1. 添加子模块

# 在您的项目根目录执行
mkdir -p src/libs
git submodule add https://github.com/cv-cat/Spider_XHS.git src/libs/spider_xhs
git submodule update --init --recursive

2. 处理依赖关系
# 将Spider_XHS的需求添加到您的项目
cat src/libs/spider_xhs/requirements.txt >> requirements.txt
pip install -r requirements.txt


 tree -L 7 -I 'venv|node_modules'



cd src/libs/spider_xhs
npm install
