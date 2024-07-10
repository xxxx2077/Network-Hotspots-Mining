import os
import sys
import jieba
import json
import numpy as np
from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Concat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models import Summary, PopRecord, Post
from app.util.util import querySet_to_list


class SinglePassCluster():
    def __init__(self, stopWords_path="app/data/stop_words.txt", my_stopwords=None,
                 max_df=0.5, max_features=1000,
                 simi_threshold=0.5, res_save_path1="app/result/res_cluster2idx.json",
                 res_save_path2="app/result/res_total.json", res_save_path3="app/result/res_cluster2hot.json",
                 res_save_path4="app/result/res_cluster2hot_perday.json"):
        self.stopwords = self.load_stopwords(stopWords_path)
        if isinstance(my_stopwords, list):
            self.stopwords += my_stopwords
        self.tfidf = TfidfVectorizer(stop_words=self.stopwords, max_df=max_df, max_features=max_features)
        self.simi_thr = simi_threshold
        self.cluster_center_vec = []  # [cluster_center_vec, ]
        self.idx_2_text = {}  # {文本id: text, }
        self.cluster_2_idx = {}  # {cluster_id: [text_id, ]}
        self.cluster_2_hot = {}  # {cluster_id: [hot]}
        self.cluster_2_hot_perday = {}  # {cluster_id: [hot]}
        self.res = {}  # {cluster_id: {text_id: text}}
        self.res_path1 = res_save_path1  # save self.cluster_2_idx
        self.res_path2 = res_save_path2  # save self.res
        self.res_path3 = res_save_path3  # save self.cluster_2_hot
        self.res_path4 = res_save_path4  # save self.cluster_2_hot

    def load_stopwords(self, path):
        stopwords = []
        with open(path, 'r', encoding="utf-8") as f:
            for line in f:
                stopwords.append(line.strip())
        return stopwords

    def cut_sentences(self, texts):
        if isinstance(texts, str):
            if not os.path.exists(texts):
                print("path: {} does not exist !!!".format(texts))
                sys.exit()
            else:
                _texts = []
                with open(texts, 'r', encoding="utf-8") as f:
                    for line in f:
                        _texts.append(line.strip())
                texts = _texts
        texts_cut = [" ".join(jieba.lcut(t)) for t in texts]
        self.idx_2_text = {idx: text for idx, text in enumerate(texts)}
        return texts_cut

    def get_tfidf(self, texts_cut):
        tfidf = self.tfidf.fit_transform(texts_cut)
        return tfidf.todense().tolist()

    def cosion_simi(self, vec):
        simi = cosine_similarity(np.array([vec]), np.array(self.cluster_center_vec))
        max_idx = np.argmax(simi, axis=1)[0]
        max_val = simi[0][max_idx]
        return max_val, max_idx

    def single_pass(self, texts, id_list, hot_value_list, hot_value_perday_list):
        # print('----------------------------')
        # print('single_pass is running.....')
        texts_cut = self.cut_sentences(texts)
        tfidf = self.get_tfidf(texts_cut)
        # print(len(tfidf), len(tfidf[0]))

        # Start clustering
        for idx, vec in enumerate(tfidf):
            # Initialize, no clusters exist
            if not self.cluster_center_vec:
                self.cluster_center_vec.append(vec)
                self.cluster_2_idx[0] = [id_list[idx]]
                Post.objects.filter(id=id_list[idx]).update(class_id=1)
                self.cluster_2_hot[0] = [hot_value_list[idx]]
                self.cluster_2_hot_perday[0] = [hot_value_perday_list[idx]]
                self.res[0] = {id_list[idx]: self.idx_2_text[idx]}
            # Clusters exist
            else:
                max_simi, max_idx = self.cosion_simi(vec)
                if max_simi >= self.simi_thr:
                    self.cluster_2_idx[max_idx].append(id_list[idx])
                    Post.objects.filter(id=id_list[idx]).update(class_id=(max_idx + 1))
                    self.cluster_2_hot[max_idx].append(hot_value_list[idx])
                    self.cluster_2_hot_perday[max_idx].append(hot_value_perday_list[idx])
                    self.res[max_idx][id_list[idx]] = self.idx_2_text[idx]
                else:
                    new_cluster_id = len(self.cluster_2_idx)
                    self.cluster_center_vec.append(vec)
                    self.cluster_2_idx[new_cluster_id] = [id_list[idx]]
                    Post.objects.filter(id=id_list[idx]).update(class_id=(new_cluster_id + 1))
                    self.cluster_2_hot[new_cluster_id] = [hot_value_list[idx]]
                    self.cluster_2_hot_perday[new_cluster_id] = [hot_value_perday_list[idx]]
                    self.res[new_cluster_id] = {id_list[idx]: self.idx_2_text[idx]}

        with open(self.res_path1, "w", encoding="utf-8") as f:
            json.dump(self.cluster_2_idx, f, ensure_ascii=False)

        with open(self.res_path2, "w", encoding="utf-8") as f:
            json.dump(self.res, f, ensure_ascii=False)

        with open(self.res_path3, "w", encoding="utf-8") as f:
            json.dump(self.cluster_2_hot, f, ensure_ascii=False)

        with open(self.res_path4, "w", encoding="utf-8") as f:
            json.dump(self.cluster_2_hot_perday, f, ensure_ascii=False)


def get_data():
    summary_subquery = Summary.objects.filter(
        is_abnormal=False,
        summary_id=OuterRef('id')
    ).values('summary')[:1]
    posts_querySet = Post.objects.filter(
        is_summaried=True
    ).annotate(
        summary=Subquery(summary_subquery),
        post = Concat('title', Value('。'), 'summary')
    ).values(
        'id',
        'post',
    )
    posts_id_list = querySet_to_list(posts_querySet, 'id')
    posts_list = querySet_to_list(posts_querySet, 'post')

    hot_value_list = []
    hot_value_rate_list = []
    for idx, summary_id in enumerate(posts_id_list):
        print(summary_id)
        hot_value_dic = PopRecord.objects.filter(pid=summary_id).all().order_by('-recordtime').values('hotval',
                                                                                                      'hotval_rate').first()
        hot_value_rate = 0
        hot_value = 0
        if hot_value_dic is not None:
            hot_value = hot_value_dic['hotval']
            hot_value_rate = hot_value_dic['hotval_rate']
        print(hot_value)
        print(hot_value_rate)
        hot_value_list.append(hot_value)
        hot_value_rate_list.append(hot_value_rate)
    return posts_id_list, posts_list, hot_value_list, hot_value_rate_list


def launch_single_pass():
    # test_data_file = "app/data/data1.txt"
    summary_id_list, summary_list, hot_value_list, hot_value_perday_list = get_data()
    cluster = SinglePassCluster(max_features=100, simi_threshold=0.1)
    cluster.single_pass(summary_list, summary_id_list, hot_value_list, hot_value_perday_list)

# if __name__ == "__main__":
#     test_data = "../data/data1.txt"
#     cluster = SinglePassCluster(max_features=100, simi_threshold=0.1)
#     cluster.single_pass(test_data)
