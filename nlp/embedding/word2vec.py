# coding: utf-8
import jieba
from gensim.models import word2vec


class GensimWord2VecModel:

    def __init__(self, train_file,
                 model_path,
                 user_dict=None,
                 stop_dict=None):
        """
        用gensim word2vec 训练词向量
        :param train_file: 分好词的文本
        :param model_path: 模型保存的路劲
        :param user_dict: 自定义词典
        :param stop_dict: 停用词表
        """
        self.train_file = train_file
        self.model_path = model_path
        self.user_dict = user_dict
        self.stop_dict = stop_dict
        self.model = self.load()
        if not self.model:
            self.model = self.train()
            self.save(self.model_path)

    def train(self):
        sentences = process_data(self.train_file, self.user_dict, self.stop_dict)
        model = word2vec.Word2Vec(sentences, min_count=2, window=3, size=300, workers=4)
        return model

    def vector(self, word):
        return self.model.wv.get_vector(word)

    def similar(self, word):
        return self.model.wv.similar_by_word(word, topn=10)

    def save(self, model_path):
        self.model.save(model_path)

    def load(self):
        # 加载模型文件
        try:
            model = word2vec.Word2Vec.load(self.model_path)
        except FileNotFoundError:
            model = None
        return model


def process_data(train_file, user_dict, stop_dict):
    # 结巴分词加载自定义词典(要符合jieba自定义词典规范)
    if user_dict:
        jieba.load_userdict(user_dict)

    # 加载停用词表(每行一个停用词)
    stop_words = []
    if stop_dict:
        with open(stop_dict, 'r', encoding='utf-8') as file:
            stop_words = [stop_word.strip() for stop_word in file.readlines()]

    # 读取文件内容并分词, 去掉停用词
    with open(train_file, 'r', encoding='utf-8') as file:
        sentences = file.readlines()
        sentences = [jieba.lcut(sentence.strip()) for sentence in sentences]
        sentences = [[s for s in sentence if s not in stop_words] for sentence in sentences]

    return sentences
