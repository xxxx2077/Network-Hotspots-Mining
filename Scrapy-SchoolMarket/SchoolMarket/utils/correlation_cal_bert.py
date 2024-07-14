'''
请先更新必要的库
pip install transformers
pip install torch
pip install jieba
'''
import os
import time

from transformers import BertTokenizer, BertModel
import torch
import jieba
import re
import numpy as np
from SchoolMarket.utils.database import MysqlOperator

'''
可选预训练模型有：
RoBERTa-wwm-ext：全称RoBERTa-wwm-ext（Whole Word Masking），在大规模中文语料上进行了更长时间的训练，效果优于BERT-base-chinese。
MacBERT：MacBERT是在BERT和RoBERTa的基础上进行改进的一个中文模型，在许多NLP任务上表现优异。
ERNIE：百度开发的ERNIE模型，通过引入知识图谱进一步增强了语义理解能力。
'''

# 1：

# # 加载预训练的ERNIE模型和分词器
# tokenizer = BertTokenizer.from_pretrained('nghuyong/ernie-1.0')
# model = BertModel.from_pretrained('nghuyong/ernie-1.0')

# 加载预训练的MacBERT模型和分词器
# tokenizer = BertTokenizer.from_pretrained('hfl/chinese-macbert-base')
# model = BertModel.from_pretrained('hfl/chinese-macbert-base')

# 用绝对路径不易出错
current_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(current_dir, 'tmp/MacBERT')

# 保存模型和分词器
# model.save_pretrained(model_dir)
# tokenizer.save_pretrained(model_dir)


# 2：
# 加载保存的模型和分词器

tokenizer = BertTokenizer.from_pretrained(model_dir)
model = BertModel.from_pretrained(model_dir)

# 3：
# 定义高校相关的词条集合
university_related_terms = [
    "榕园", "荔园", "瑾园",
    "食堂", "校门", "宿舍", "工地", "学院", "课程", "考试", "专业",
    "教授", "老师", "行政", "校长", "学校", "中山大学", "鸭大", "中大",
    "中珠", "珠海校区", "南校", "东校", "北校", "中深", "深圳校区",
    "医学院", "文学院", "理学院", "工学院", "数据科学与计算机学院", "新华学院", "传播与设计学院", "岭南学院",
    "国际经济贸易学院", "法学院", "商学院", "马克思主义学院", "国际学院", "旅游学院", "材料学院", "药学院",
    "生命科学学院", "环境与能源学院", "生物医学工程学院", "微电子学院", "软件学院", "公共卫生学院", "海洋学院",
    "社会科学院",
    "大学生活动中心", "体育馆", "图书馆", "科学会堂", "研究生院"
]


# 4：
# 获取词条集合的BERT嵌入
def get_embeddings(text_list, tokenizer, model):
    inputs = tokenizer(text_list, max_length=512, return_tensors='pt', padding=True, truncation=True)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings


# 获取相关词条的嵌入
related_terms_embeddings = get_embeddings(university_related_terms, tokenizer, model)

# 设置日志等级
jieba.setLogLevel(jieba.logging.INFO)
# 去除停用词的中文分词
def chinese_word_cut(mytext, stopwords="all"):
    # jieba.load_userdict('自定义词典.txt')  # 这里你可以添加jieba库识别不了的网络新词，避免将一些新词拆开

    # 文本预处理 ：去除一些无用的字符只提取出中文出来
    new_data = re.findall('[\u4e00-\u9fa5]+', mytext, re.S)
    new_data = " ".join(new_data)
    # 文本分词
    seg_list_exact = jieba.lcut(new_data)
    result_list = []
    # 读取停用词库
    stopwords_path = os.path.join(current_dir, "stopwords", f"stopwords_{stopwords}.txt")
    # print("path",stopwords_path)
    with open(stopwords_path, encoding='utf-8') as f:  # 可根据需要打开停用词库，然后加上不想显示的词语
        con = f.readlines()
        stop_words = set()
        for i in con:
            i = i.replace("\n", "")  # 去掉读取每一行数据的\n
            stop_words.add(i)
    # 去除停用词
    for word in seg_list_exact:
        if word not in stop_words:
            result_list.append(word)
    return result_list


# 5：
# 计算帖子内容与高校的相关程度
def calculate_relevance(post_content, related_terms_embeddings=related_terms_embeddings, tokenizer=tokenizer,
                        model=model):
    # 对帖子内容进行分词
    # tokens = jieba.lcut(post_content)
    # 去除停用词再分词
    tokens = chinese_word_cut(post_content)
    post_content = ' '.join(tokens)
    # print("token", tokens)
    # 获取帖子内容的BERT嵌入
    post_embedding = get_embeddings([post_content], tokenizer, model)
    # print(post_embedding)
    # 计算帖子内容嵌入与相关词条嵌入的余弦相似度
    similarities = torch.nn.functional.cosine_similarity(post_embedding, related_terms_embeddings)

    # 计算相似度的最大值作为相关程度
    # relevance = similarities.max().item()
    # print(relevance)
    relevance = similarities.mean().item()
    # print(relevance)
    return relevance


def update_relevance(db_opr: MysqlOperator):
    select_sql = "select id, title, content from post order by time desc limit 3500,3500;"
    rows = db_opr.query(select_sql)
    count = 0
    for row in rows:
        id, title, content = row
        relevance = calculate_relevance(title + content)
        update_sql = f" update post set correlation = {relevance} where id = {id};"
        db_opr.exec_sql(update_sql)
        count += 1
        if count % 100 == 0:
            print(count)

def update_null_relevance(db_opr: MysqlOperator):
    select_sql = "select id, title, content from post where correlation is null;"
    rows = db_opr.query(select_sql)
    for row in rows:
        id, title, content = row
        relevance = calculate_relevance(title + content)
        update_sql = f" update post set correlation = {relevance} where id = {id};"
        db_opr.exec_sql(update_sql)



def main():
    # 示例帖子内容
    post_content = "今天在学校的食堂吃到了特别好吃的饭菜。"
    #     post_content = """
    # 收纸箱📦，60x40x50
    #     """
    # post_content = ""
    print(post_content)
    # 计算帖子内容与高校的相关程度
    relevance_score = calculate_relevance(post_content, related_terms_embeddings, tokenizer, model)
    print(f"Relevance Score: {relevance_score}")

    # print(time.strftime("%Y-%m-%d %H:%M:%S"))
    # opr = MysqlOperator()
    # update_relevance(opr)
    # opr.close()
    # print(time.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main()
