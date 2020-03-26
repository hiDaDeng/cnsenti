from setuptools import setup
import setuptools

setup(
    name='cnsenti',     # 包名字
    version='0.0.1',   # 包版本
    description='中文复合事件抽取，可以用来识别文本的模式，包括条件事件、因果事件、顺承事件、反转事件。代码为刘焕勇原创设计,项目地址https://github.com/liuhuanyong/ComplexEventExtraction 项目介绍很详细，感兴趣的一定要去原项目看一下。我仅仅是对代码做了简单的修改，增加了函数说明注释和stats函数，可以用于统计文本中各种模式的分布(数量)情况。',   # 简单描述
    author='大邓',  # 作者
    author_email='thunderhit@qq.com',  # 邮箱
    url='https://github.com/thunderhit/eventextraction',      # 包的主页
    packages=setuptools.find_packages(),
    package_data = {'':['dictionary/hownet/*.pkl','dictionary/dutir/*.pkl']},  #所有目录下的pkl词典文件
    install_requires=['jieba', 'numpy'],
    python_requires='>=3.5',
    license="MIT",
    keywords=['knowledge graph', 'text analysis', 'event extraction'],
    long_description=open('README.md').read(), # 读取的Readme文档内容
    long_description_content_type="text/markdown")  # 指定包文档格式为markdown
    #py_modules = ['eventextraction.py']
