from setuptools import setup
import setuptools

setup(
    name='cnsenti',     # 包名字
    version='0.0.4',   # 包版本
    description='中文情感分析库(Chinese Sentiment))可对文本进行情绪分析、正负情感分析。',   # 简单描述
    author='大邓',  # 作者
    author_email='thunderhit@qq.com',  # 邮箱
    url='https://github.com/thunderhit/eventextraction',      # 包的主页
    packages=setuptools.find_packages(),
    package_data = {'':['dictionary/hownet/*.pkl','dictionary/dutir/*.pkl']},  #所有目录下的pkl词典文件
    install_requires=['jieba', 'numpy'],
    python_requires='>=3.5',
    license="MIT",
    keywords=['chinese text analysis', 'text analysis', 'sentiment', 'sentiment analysis', 'natural language processing'],
    long_description=open('README.md').read(), # 读取的Readme文档内容
    long_description_content_type="text/markdown")  # 指定包文档格式为markdown
    #py_modules = ['eventextraction.py']
