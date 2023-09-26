# 亚马逊评论爬取工具

## 功能
爬取亚马逊评论，基于百度翻译接口把英文评论翻译成中文，输出excel.使用chatGPT分析Review情感色彩并返回。
- 使用说明
在输入信息/商品地址文件.txt 输入要爬取的亚马逊网站的地址，每行一个地址

## 更新说明
- 修复了由于网页源码版本更迭导致的部分bug，修正爬取规则。
- 整理好文本数据excel后，填入自己的OPENAI key，运行chatreview_sentiment.py即可得到ChatGPT（基于GPT3）对Review的情感色彩得分。
