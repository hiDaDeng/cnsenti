import jieba
import pickle
import pathlib
import re

class Emotion(object):
    """
    本代码将大连理工大学七大类情绪词典作为情绪分析的情绪词库，可对文本进行细粒度（相比于正负情感而言）情感分析。

    快速使用
        >>> from cnsenti import Emotion
        >>> emotion = Emotion()
        >>> test_text = '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心'
        >>> emotion.emotion_count(test_text)
        >>> {'words': 22, 'sentences': 2, '好': 0, '乐': 4, '哀': 0, '怒': 0, '惧': 0, '恶': 0, '惊': 0}
    """

    def __init__(self):
        self.Haos = self.read_dict('好.pkl')
        self.Les = self.read_dict('乐.pkl')
        self.Ais = self.read_dict('哀.pkl')
        self.Nus = self.read_dict('怒.pkl')
        self.Jus = self.read_dict('惧.pkl')
        self.Wus = self.read_dict('恶.pkl')
        self.Jings = self.read_dict('惊.pkl')

    def read_dict(self, file):
        pathchain = ['dictionary', 'dutir',file]
        mood_dict_filepath = pathlib.Path(__file__).parent.joinpath(*pathchain)
        dict_f = open(mood_dict_filepath, 'rb')
        words = pickle.load(dict_f)
        return words

    def emotion_count(self, text):
        """
        简单情感分析，未考虑强度副词、否定词对情感的复杂影响。仅仅计算各个情绪词出现次数(占比)
        :param text:  中文文本字符串
        :return: 返回文本情感统计信息，类似于这样{'words': 22, 'sentences': 2, '好': 0, '乐': 4, '哀': 0, '怒': 0, '惧': 0, '恶': 0, '惊': 0}
        """
        wordnum, sentences, hao, le, ai, nu, ju, wu, jing =0, 0, 0, 0, 0, 0, 0, 0, 0
        sentences = len(re.split('[\.。！!？\?\n;；]+', text))
        words = jieba.lcut(text)
        wordnum = len(words)
        for w in words:
            if w in self.Haos:
                hao += 1
            elif w in self.Les:
                le += 1
            elif w in self.Ais:
                ai += 1
            elif w in self.Nus:
                nu += 1
            elif w in self.Jus:
                ju += 1
            elif w in self.Wus:
                wu += 1
            elif w in self.Jings:
                jing += 1
            else:
                pass
        result = {'words':wordnum, 'sentences':sentences, '好':hao, '乐':le, '哀':ai, '怒':nu, '惧':ju, '恶': wu, '惊':jing}
        return result



