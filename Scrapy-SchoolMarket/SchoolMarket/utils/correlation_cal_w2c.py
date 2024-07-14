# 备用

#1.
#请先安装必要的库
# pip install gensim
# pip install nltk


#2.
# 下载并预训练的Word2Vec模型并加载
# 或自行下载：https://www.jianshu.com/p/ae5b45e96dbf

# import gensim.downloader as api

# model = api.load("")
# model.save("")



#3.
#加载模型
#该模型中文无法使用请通过推荐链接下载或自行搜索
from gensim.models import KeyedVectors

# model = KeyedVectors.load_word2vec_format('word2vec-google-300.model', binary=True)

model = KeyedVectors.load('word2vec-google-300.model', mmap='r')


#4.
# 定义目标单位相关的词条集合
university_related_terms = ["食堂", "校门", "宿舍", "学院", "课程", "教授", "校长"]



#5.
# 定义一个函数计算帖子内容与高校的相关程度
import numpy as np
import jieba


# 计算帖子内容与高校的相关程度
def calculate_relevance(post_content, related_terms, model):
    # 对帖子内容进行分词
    tokens = jieba.lcut(post_content)
    print(tokens)
    
    # 计算每个词与相关词条集合中每个词的相似度
    similarities = []
    for token in tokens:
        if token in model:
            token_similarities = [model.similarity(token, term) for term in related_terms if term in model]
            print("text")
            print(token_similarities)
            if token_similarities:
                similarities.append(max(token_similarities))  # 取最大相似度
    
    # 如果没有找到相似的词，返回0
    if not similarities:
        return 0.0
    
    # 计算相似度的平均值作为相关程度
    relevance = np.mean(similarities)
    return relevance


def main():
    # 示例帖子内容
    post_content = "i love u my school 嘿嘿"

    # 计算帖子内容与高校的相关程度
    relevance_score = calculate_relevance(post_content, university_related_terms, model)
    print(f"Relevance Score: {relevance_score}")

if __name__ == "__main__":
    main()