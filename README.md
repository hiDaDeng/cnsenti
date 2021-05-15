
![wbt5's GitHub stats](https://github-readme-stats.vercel.app/api?username=hidadeng&show_icons=true&theme=default&include_all_commits=true&count_private=true)

# 一、cnsenti

中文情感分析库(Chinese Sentiment))可对文本进行情绪分析、正负情感分析。

- [github地址](https://github.com/hidadeng/cnsenti) ``https://github.com/thunderhit/cnsenti``

- [pypi地址](https://pypi.org/project/cnsenti/)  ``https://pypi.org/project/cnsenti/``

- [视频课-**Python网络爬虫与文本数据分析**](https://ke.qq.com/course/482241?tuin=163164df)


### 特性

- 情感分析默认使用的知网Hownet
- 情感分析可支持导入自定义txt情感词典(pos和neg)
- 情绪分析使用大连理工大学情感本体库，可以计算文本中的七大情绪词分布

### 注意
代码中情绪分析使用的大连理工大学情感本体库，如发表论文，请注意用户许可协议
1. 该情感词汇本体由大连理工大学信息检索研究室独立整理标注完成，可供国内外大学、科研院所及个人用于学术研究目的。 
2. 如任何单位和个人需将其用于商业目的，请发送邮件至 irlab@dlut.edu.cn 进行协商。 
3. 使用过程中如发现该资源中有任何错误或不妥之处，欢迎用户将您的宝贵意见发送至邮箱 irlab@dlut.edu.cn ，我们 将以最快的速度为您解决。 
4. 如果用户使用该资源发表论文或取得科研成果，请在论文中添加诸如“使用了大连理工大学信息检索研究室的情感词汇本体” 字样加以声明。
5. 参考文献中加入引文“徐琳宏,林鸿飞,潘宇,等.情感词汇本体的构造[J]. 情报学报, 2008, 27(2): 180-185.” 
6. 任何通过拷贝及其他非正式下载方式获得该资源的用户也应遵守该许可协议，大连理工大学信息检索研究室拥有该许可协议 最终的解释权和修改权。


### 安装

#### 方法一

```
pip install cnsenti
```

#### 方法二

```
pip install cnsenti -i https://pypi.tuna.tsinghua.edu.cn/simple/
```


<br>


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

<br>

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



我们先看看没有情感形容词的情形

```python
from cnsenti import Sentiment
senti = Sentiment()      #两txt均为utf-8编码
test_text = '这家公司是行业的引领者，是中流砥柱。'
result1 = senti.sentiment_count(test_text)
result2 = senti.sentiment_calculate(test_text)
print('sentiment_count',result1)
print('sentiment_calculate',result2)
```

Run

```
sentiment_count {'words': 10, 'sentences': 1, 'pos': 0, 'neg': 0}
sentiment_calculate {'sentences': 1, 'words': 10, 'pos': 0, 'neg': 0}
```

如我所料，虽然句子是正面的，但是因为cnsenti自带的情感词典仅仅是形容词情感词典，对于很多场景而言，适用性有限，所以pos=0。

#### 3.4.1 自定词典格式

好在cnsenti支持导入自定义词典，但目前**只有Sentiment类支持导入自定义正负情感词典**，自定义词典需要满足

- 必须为txt文件
- 原则上建议encoding为utf-8
- txt文件每行只有一个词

#### 3.4.2 Sentiment自定义词典参数

```python
senti = Sentiment(pos='正面词自定义.txt',  
                  neg='负面词自定义.txt', 
                  merge=True,  
                  encoding='utf-8')
```

- pos 正面情感词典txt文件路径
- neg 负面情感词典txt文件路径
- merge 布尔值；merge=True，cnsenti会融合自定义词典和cnsenti自带词典；merge=False，cnsenti只使用自定义词典
- encoding  两txt均为utf-8编码

#### 3.4.3 自定义词典使用案例

这部分我放到test文件夹内,代码和自定义词典均在test内，所以我使用相对路径设定自定义词典的路径

```terminal
|test
   |---代码.py
   |---正面词自定义.txt
   |---负面词自定义.txt
```

**正面词自定义.txt**  

```
中流砥柱
引领者
```



```python
from cnsenti import Sentiment

senti = Sentiment(pos='正面词自定义.txt',  #正面词典txt文件相对路径
                  neg='负面词自定义.txt',  #负面词典txt文件相对路径
                  merge=True,             #融合cnsenti自带词典和用户导入的自定义词典
                  encoding='utf-8')      #两txt均为utf-8编码

test_text = '这家公司是行业的引领者，是中流砥柱。今年的业绩非常好。'
result1 = senti.sentiment_count(test_text)
result2 = senti.sentiment_calculate(test_text)
print('sentiment_count',result1)
print('sentiment_calculate',result2)
```

Run

```
sentiment_count {'words': 16, 'sentences': 2, 'pos': 2, 'neg': 0}
sentiment_calculate {'sentences': 2, 'words': 16, 'pos': 5, 'neg': 0}
```

上面参数我们传入了正面自定义词典和负面自定义词典，并且使用了融合模式（merge=True），可以利用cnsenti自带的词典和刚刚导入的自定义词典进行情感计算。



**补充：**

我设计的这个库目前仅能支持两类型pos和neg，如果你的研究问题是两分类问题，如好坏、美丑、善恶、正邪、友好敌对，你就可以定义两个txt文件，分别赋值给pos和neg，就可以使用cnsenti库。

<br>

# 四、关于词典

目前比较有可解释性的文本分析方法是词典法，算法逻辑都很清晰。词典的好坏决定了情感分析的好坏。如果没有词典，也就限制了你进行文本情感计算。

目前大多数人使用的是形容词情感词典，如大连理工大学情感本体库和知网Hownet，优点是直接拿来用，缺点也很明显，对于很多带情感却无形容词的文本无能为力。如**这手机很耐摔**， 使用形容词情感词典计算得分pos和neg均为0。类似问题在不同研究对象的文本数据应该都是挺普遍的，所以人工构建情感词典还是很有必要的。

我封装了刘焕勇基于so_pmi算法的新词发现代码，将该库其命名为**wordexpansion**。wordexpansion可以极大的提高提高自定义词典的构建速度，感兴趣的童鞋详情可以访问[wordexpansion项目地址](https://github.com/thunderhit/wordexpansion)


<br>


# 如果

如果您是经管人文社科专业背景，编程小白，面临海量文本数据采集和处理分析艰巨任务，可以参看[《python网络爬虫与文本数据分析》](https://ke.qq.com/course/482241?tuin=163164df)视频课。作为文科生，一样也是从两眼一抹黑开始，这门课程是用五年时间凝缩出来的。自认为讲的很通俗易懂o(*￣︶￣*)o，

- python入门
- 网络爬虫
- 数据读取
- 文本分析入门
- 机器学习与文本分析
- 文本分析在经管研究中的应用

感兴趣的童鞋不妨 戳一下[《python网络爬虫与文本数据分析》](https://ke.qq.com/course/482241?tuin=163164df)进来看看~

[![](img/课程.png)](https://ke.qq.com/course/482241?tuin=163164df)



# 更多

- [B站:大邓和他的python](https://space.bilibili.com/122592901/channel/detail?cid=66008)

- 公众号：大邓和他的python

- [知乎专栏：数据科学家](https://zhuanlan.zhihu.com/dadeng)


![](img/大邓和他的Python.png)
