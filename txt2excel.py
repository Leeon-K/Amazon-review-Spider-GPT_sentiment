import openpyxl
import re

# 打开txt文件
with open('C:\\Users\\Lick\\Desktop\\papers_900m\\nlp_textblob/missheart.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 创建Excel文件
wb = openpyxl.Workbook()
ws = wb.active

# 将句子和得分写入Excel
last_sentence = ''
last_score = ''
# 将句子和得分写入Excel
last_sentence = ''
for line in lines:
    if not line.strip():
        continue
    # 预处理句子，确保其被正确地保存
    sentence = line.strip()
    if not sentence.startswith('"'):
        sentence = '"' + sentence
    if not sentence.endswith('"'):
        sentence = sentence + '"'
    # 检查句子是否为得分数字
    if re.match(r'^\d+$', sentence):
        continue
    # 匹配得分，注意可能有多个得分
    score_match = re.findall(r'[\(\[]\s*(\d+)\s*[/|-]?\s*\d*\s*[\)\]]', sentence)
    score = '' if not score_match else score_match[-1]
    # 将得分从句子中删除
    sentence = re.sub(r'[\(\[]\s*\d+\s*[/|-]?\s*\d*\s*[\)\]]', '', sentence).strip()
    # 如果前后两个句子都没有得分，则将它们合并为一个句子
    if not sentence and not last_sentence:
        continue
    if not sentence and last_sentence:
        sentence = last_sentence
    ws.append([sentence, score])
    last_sentence = sentence




# 保存到当前目录
file_dst = 'C:\\Users\\Lick\\Desktop\\papers_900m\\nlp_textblob\\toexcel/m2.xlsx'

wb.save(file_dst)
import os
print("save excel file done!,saved in " + os.getcwd() + "/" + file_dst)
