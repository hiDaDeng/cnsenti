import jieba
import numpy as np
import pickle
import pathlib
import re


class Sentiment(object):
    """
    文本情感计算类，支持导入自定义词典

    默认使用知网Hownet词典进行情感分析
        >>> from cnsenti import Sentiment
        >>> senti = Sentiment()

    统计文本中情感词个数，
    返回的pos和neg是词语个数
        >>>test_text= '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心'
        >>>senti.sentiment_count(test_text)
        >>>{'words': 24, 'sentences': 2, 'pos': 4, 'neg': 0}

    考虑强度副词(如"非常"，"差不多")对情感形容词的修饰作用，
    和否定词对情感意义的反转作用。
    返回的pos和neg是得分
        >>>senti.sentiment_calculate(test_text)
        >>>{'sentences': 2, 'words': 24, 'pos': 46.0, 'neg': 0.0}


    使用自定义txt词典(建议utf-8编码)，
    目前仅支持pos和neg两类词典，每行一个词语。
    merge=True，cnsenti会融合自带的词典和用户导入的自定义词典；merge=False，cnsenti只使导入的自定义词典
    其中pos和neg为txt词典文件路径，encoding为txt词典的编码方式
    这里是utf-8编码的文件，初始化方式
        >>>from cnsenti import Sentiment
        >>>senti = Sentiment(pos='正面词典.txt', neg='负面词典.txt', merge=True, encoding='utf-8')
    """

    def __init__(self, merge=True, pos=None, neg=None, encoding='utf-8'):
        """
        :pos 正面词典的txt文件
        :neg 负面词典的txt文件
        :merge 默认merge=True,即融合自带情感词典和自定义词典。merge=False，只使用自定义词典。
        :encoding 词典txt文件的编码，默认为utf-8。如果是其他编码，该参数必须使用
        """
        self.Poss = self.load_dict('pos.pkl')
        self.Negs = self.load_dict('neg.pkl')

        if pos:
            if merge:
                del self.Poss
                self.Poss = self.load_diydict(file=pos, encoding=encoding)+self.load_dict('pos.pkl')
                jieba.load_userdict(pos)

            else:
                del self.Poss
                self.Poss = self.load_diydict(file=pos, encoding=encoding)
                jieba.load_userdict(pos)


        if neg:
            if merge:
                del self.Negs
                self.Negs = self.load_diydict(file=neg, encoding=encoding)+self.load_dict('neg.pkl')
                jieba.load_userdict(neg)
            else:
                del self.Negs
                self.Negs = self.load_diydict(file=neg, encoding=encoding)
                jieba.load_userdict(neg)

        self.Denys = self.load_dict('deny.pkl')

        self.Extremes = self.load_dict('extreme.pkl')
        self.Verys = self.load_dict('very.pkl')
        self.Mores = self.load_dict('more.pkl')
        self.Ishs = self.load_dict('ish.pkl')

    def load_dict(self, file):
        """
        Sentiment内置的读取hownet自带pkl词典
        :param file:  词典pkl文件
        :return: 词语列表
        """
        pathchain = ['dictionary', 'hownet',file]
        mood_dict_filepath = pathlib.Path(__file__).parent.joinpath(*pathchain)
        dict_f = open(mood_dict_filepath, 'rb')
        words = pickle.load(dict_f)
        return words

    def load_diydict(self, file, encoding):
        """
        :param file:  自定义txt情感词典，其中txt文件每行只能放一个词
        :param encoding:  txt文件的编码方式
        :return:
        """
        text = open(file, encoding=encoding).read()
        words = text.split('\n')
        words = [w for w in words if w]
        return words


    def sentiment_count(self, text):
        """
        简单情感分析，未考虑强度副词、否定词对情感的复杂影响。仅仅计算各个情绪词出现次数(占比)
        :param text:  中文文本字符串
        :return: 返回情感信息，形如{'sentences': 2, 'words': 24, 'pos': 46.0, 'neg': 0.0}
        """
        length, sentences, pos, neg = 0, 0, 0, 0
        sentences = [s for s in re.split('[\.。！!？\?\n;；]+', text) if s]
        sentences = len(sentences)
        words = jieba.lcut(text)
        length = len(words)
        for w in words:
            if w in self.Poss:
                pos+=1
            elif w in self.Negs:
                neg+=1
            else:
                pass
        return {'words': length,  'sentences':sentences, 'pos':pos, 'neg':neg}



    def judgeodd(self, num):
        """
        判断奇数偶数。当情感词前方有偶数个否定词，情感极性方向不变。奇数会改变情感极性方向。
        """
        if (num % 2) == 0:
            return 'even'
        else:
            return 'odd'

    def sentiment_calculate(self, text):
        """
        考虑副词对情绪形容词的修饰作用和否定词的反转作用，
        其中副词对情感形容词的情感赋以权重，
        否定词确定情感值正负。

        :param text:  文本字符串
        :return: 返回情感信息，刑如{'sentences': 2, 'words': 24, 'pos': 46.0, 'neg': 0.0}
        """
        sentences = [s for s in re.split('[\.。！!？\?\n;；]+', text) if s]
        wordnum = len(jieba.lcut(text))
        count1 = []
        count2 = []
        for sen in sentences:
            segtmp = jieba.lcut(sen)
            i = 0  # 记录扫描到的词的位置
            a = 0  # 记录情感词的位置
            poscount = 0  # 积极词的第一次分值
            poscount2 = 0  # 积极词反转后的分值
            poscount3 = 0  # 积极词的最后分值（包括叹号的分值）
            negcount = 0
            negcount2 = 0
            negcount3 = 0
            for word in segtmp:
                if word in self.Poss:  # 判断词语是否是情感词
                    poscount += 1
                    c = 0
                    for w in segtmp[a:i]:  # 扫描情感词前的程度词
                        if w in self.Extremes:
                            poscount *= 4.0
                        elif w in self.Verys:
                            poscount *= 3.0
                        elif w in self.Mores:
                            poscount *= 2.0
                        elif w in self.Ishs:
                            poscount *= 0.5
                        elif w in self.Denys:
                            c += 1
                    if self.judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                        poscount *= -1.0
                        poscount2 += poscount
                        poscount = 0
                        poscount3 = poscount + poscount2 + poscount3
                        poscount2 = 0
                    else:
                        poscount3 = poscount + poscount2 + poscount3
                        poscount = 0
                    a = i + 1  # 情感词的位置变化

                elif word in self.Negs:  # 消极情感的分析，与上面一致
                    negcount += 1
                    d = 0
                    for w in segtmp[a:i]:
                        if w in self.Extremes:
                            negcount *= 4.0
                        elif w in self.Verys:
                            negcount *= 3.0
                        elif w in self.Mores:
                            negcount *= 2.0
                        elif w in self.Ishs:
                            negcount *= 0.5
                        elif w in self.Denys:
                            d += 1
                    if self.judgeodd(d) == 'odd':
                        negcount *= -1.0
                        negcount2 += negcount
                        negcount = 0
                        negcount3 = negcount + negcount2 + negcount3
                        negcount2 = 0
                    else:
                        negcount3 = negcount + negcount2 + negcount3
                        negcount = 0
                    a = i + 1
                elif word == '！' or word == '!':  ##判断句子是否有感叹号
                    for w2 in segtmp[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                        if w2 in self.Poss or self.Negs:
                            poscount3 += 2
                            negcount3 += 2
                            break
                i += 1  # 扫描词位置前移

                # 以下是防止出现负数的情况
                pos_count = 0
                neg_count = 0
                if poscount3 < 0 and negcount3 > 0:
                    neg_count += negcount3 - poscount3
                    pos_count = 0
                elif negcount3 < 0 and poscount3 > 0:
                    pos_count = poscount3 - negcount3
                    neg_count = 0
                elif poscount3 < 0 and negcount3 < 0:
                    neg_count = -poscount3
                    pos_count = -negcount3
                else:
                    pos_count = poscount3
                    neg_count = negcount3

                count1.append([pos_count, neg_count])
            count2.append(count1)
            count1 = []

        pos_result = []
        neg_result = []
        for sentence in count2:
            score_array = np.array(sentence)
            pos = np.sum(score_array[:, 0])
            neg = np.sum(score_array[:, 1])
            pos_result.append(pos)
            neg_result.append(neg)

        pos_score = np.sum(np.array(pos_result))
        neg_score = np.sum(np.array(neg_result))
        score = {'sentences': len(count2),
                 'words':wordnum,
                 'pos': pos_score,
                 'neg': neg_score}

        return score







