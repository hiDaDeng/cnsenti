[toc]

# 一、cnsenti

中文情感分析库(Chinese Sentiment))可对文本进行情绪分析、正负情感分析。

- [github地址]()

- [pypi地址](https://pypi.org/project/cnsenti/)



### 特性

- 情感分析默认使用的知网Hownet
- 情感分析可支持导入自定义txt情感词典(pos和neg)
- 情绪分析使用大连理工大学情感本体库，可以计算文本中的七大情绪词分布



### 安装

#### 方法一

```
pip install cnsenti
```

#### 方法二

```
pip install cnsenti -i https://pypi.tuna.tsinghua.edu.cn/simple/
```





# 二、快速上手

中文文本情感词正负情感词统计

```python
from cnsenti import Sentiment

senti = Sentiment()
test_text= '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心'
result = senti.sentiment_count(test_text)
print(result)
```

Run

```
{'words': 24, 
'sentences': 2, 
'pos': 4, 
'neg': 0}
```



中文文本情绪统计

```python
from cnsenti import Emotion

emotion = Emotion()
test_text = '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心'
result = emotion.emotion_count(test_text)
print(result)
```

Run

```
{'words': 22, 
'sentences': 2, 
'好': 0, 
'乐': 4, 
'哀': 0, 
'怒': 0, 
'惧': 0, 
'恶': 0, 
'惊': 0}
```



#  三、文档

cnsenti包括Emotion和Sentiment两大类，其中

- **Emotion** 情绪计算类,包括**emotion_count(text)**方法
- **Sentiment** 正负情感计算类，包括**sentiment_count(text)**和**sentiment_calculate(text)**两种方法



### 3.1 emotion_count(text)

emotion_count(text)y用于统计文本中各种情绪形容词出现的词语数。使用大连理工大学情感本体库词典，支持**七种情绪统计(好、乐、哀、怒、惧、恶、惊)**。

```python
from cnsenti import Emotion

emotion = Emotion()
test_text = '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心'
result = emotion.emotion_count(test_text)
print(result)
```

返回

```
{'words': 22, 
'sentences': 2, 
'好': 0, 
'乐': 4, 
'哀': 0, 
'怒': 0, 
'惧': 0, 
'恶': 0, 
'惊': 0}
```

其中

- **words** 中文文本的词语数
- **sentences** 中文文本的句子数
- **好、乐、哀、怒、惧、恶、惊**  text中各自情绪出现的词语数



### 3.2 sentiment_count(text)

隶属于Sentiment类，可对文本text中的正、负面词进行统计。默认使用Hownet词典，后面会讲到如何导入自定义正、负情感txt词典文件。这里以默认hownet词典进行统计。

```python
from cnsenti import Sentiment

senti = Sentiment()
test_text = '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心'
result = senti.sentiment_count(test_text)
print(result)
```

Run

```
{'words': 24, 
'sentences': 2, 
'pos': 4, 
'neg': 0}
```

其中

- words 文本中词语数
- sentences 文本中句子数
- pos 文本中正面词总个数
- neg 文本中负面词总个数



### 3.3 sentiment_calculate(text)

隶属于Sentiment类，可更加精准的计算文本的情感信息。相比于sentiment_count只统计文本正负情感词个数，sentiment_calculate还考虑了

- 情感词前是否有强度副词的修饰作用
- 情感词前是否有否定词的情感语义反转作用

比如

```python
from cnsenti import Sentiment

senti = Sentiment()
test_text = '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心'
result1 = senti.sentiment_count(test_text)
result2 = senti.sentiment_calculate(test_text)
print('sentiment_count',result1)
print('sentiment_calculate',result2)
```

Run

```
sentiment_count 
{'words': 22, 
'sentences': 2, 
'pos': 4, 
'neg': 0}

sentiment_calculate 
{'sentences': 2, 
'words': 22, 
'pos': 27.0, 
'neg': 0.0}
```



### 3.4 自定义词典



cnsenti中只有Sentiment类支持正负情感词典自定义，自定义词典需要满足

- 必须为txt文件
- 原则上建议encoding为utf-8
- txt文件每行只有一个词

这部分我放到test文件夹内,代码和自定义词典均在test内，所以我使用相对路径设定自定义词典的路径

```terminal
|test
   |---代码.py
   |---正面词自定义.txt
   |---负面词自定义.txt
```

代码.py文件内

```python
from cnsenti import Sentiment

senti = Sentiment(pos='正面词自定义.txt',  #正面词典txt文件相对路径
                  neg='负面词自定义.txt',  #负面词典txt文件相对路径
                  encoding='utf-8')      #两txt均为utf-8编码
```

经过上面的设置就可以使用自定义词典。



**补充：**

我设计的这个库目前仅能支持两类型pos和neg，如果你的研究问题是两分类问题，如好坏、美丑、善恶、正邪、友好敌对，你就可以定义两个txt文件，分别赋值给pos和neg，就可以使用cnsenti库。



# 四、关于词典

目前比较有可解释性的文本分析方法是词典法，算法逻辑都很清晰。词典的好坏决定了情感分析的好坏。如果没有词典，也就限制了你进行文本情感计算。

目前大多数人使用的是形容词情感词典，如大连理工大学情感本体库和知网Hownet，优点是直接拿来用，缺点也很明显，对于很多带情感却无形容词的文本无能为力。如**这手机很耐摔**， 使用形容词情感词典计算得分pos和neg均为0。类似问题在不同研究对象的文本数据应该都是挺普遍的，所以人工构建情感词典还是很有必要的。

我封装了刘焕勇基于so_pmi算法的新词发现代码，将该库其命名为**wordexpansion**。wordexpansion可以极大的提高提高自定义词典的构建速度，感兴趣的童鞋详情可以访问[wordexpansion项目地址](https://github.com/thunderhit/wordexpansion)





# 如果

如果您是经管人文社科专业背景，编程小白，面临海量文本数据采集和处理分析艰巨任务，个人建议学习[《python网络爬虫与文本数据分析》](https://ke.qq.com/course/482241?tuin=163164df)视频课。作为文科生，一样也是从两眼一抹黑开始，这门课程是用五年时间凝缩出来的。自认为讲的很通俗易懂o(*￣︶￣*)o，

- python入门
- 网络爬虫
- 数据读取
- 文本分析入门
- 机器学习与文本分析
- 文本分析在经管研究中的应用

感兴趣的童鞋不妨 戳一下[《python网络爬虫与文本数据分析》](https://ke.qq.com/course/482241?tuin=163164df)进来看看~



# 更多

- [B站:大邓和他的python](https://space.bilibili.com/122592901/channel/detail?cid=66008)

- 公众号：大邓和他的python

- [知乎专栏：数据科学家](https://zhuanlan.zhihu.com/dadeng)

    
