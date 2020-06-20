#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append("../..")
sys.path.append("..")
import re                           # 正则表达式库
import jieba                        # 结巴分词
import jieba.posseg                 # 词性获取
import collections                  # 词频统计库
import numpy                        # numpy数据处理库
from PIL import Image               # 图像处理库
import wordcloud                    # 词云展示库
import matplotlib.pyplot as plt     # 图像展示库（这里以plt代表库的全称）
from jack_space.utils.common_variable import En2Cn_Pro

# 相关变量
Analysis_text = './file/分析文档.txt'        # 分析文档
userdict = 'file/用户词典.txt'             # 用户词典
StopWords = 'file/停用词库.txt'            # 停用词库
number = 100                              # 统计个数
Output = '词频.txt'                       # 输出文件
background = 'file/background.jpg'        # 词频背景

def read_and_cut_word(file):
    # 读取文件
    fn = open(file, 'r', encoding='UTF-8')  # 打开文件
    string_data = fn.read()                          # 读出整个文件
    fn.close()                                       # 关闭文件
    # 文本预处理
    pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式（空格等）
    string_data = re.sub(pattern, '', string_data)  # 将符合模式的字符去除
    # 动态调整词典
    jieba.suggest_freq('小小花', True)     #True表示该词不能被分割，False表示该词能被分割
    # 添加用户词典
    jieba.load_userdict(userdict)
    # 文本分词
    seg_list_exact = jieba.cut(string_data, cut_all=False, HMM=True)  # 精确模式分词+HMM
    object_list = []
    # 去除停用词（去掉一些意义不大的词，如标点符号、嗯、啊等）
    with open(StopWords, 'r', encoding='UTF-8') as meaninglessFile:
        stopwords = set(meaninglessFile.read().split('\n'))
    stopwords.add(' ')
    for word in seg_list_exact:  # 循环读出每个分词
        if word not in stopwords:  # 如果不在去除词库中
            object_list.append(word)  # 分词追加到列表
    return object_list

def word_frequency_count_and_output(object_list, number):
    # 词频统计
    word_counts = collections.Counter(object_list)  # 对分词做词频统计
    word_counts_top = word_counts.most_common(number)  # 获取前number个最高频的词
    # 输出至工作台，并导出“词频.txt”文件
    print ('\n词语\t词频')
    print ('——————————')
    fileOut = open(Output, 'w', encoding='UTF-8')  # 创建文本文件；若已存在，则进行覆盖
    # fileOut.write('词语\t词频\t词性\n')
    fileOut.write('词语\t词频\n')
    fileOut.write('——————————\n')
    count = 0
    for TopWord, Frequency in word_counts_top:  # 获取词语和词频
        for POS in jieba.posseg.cut(TopWord):  # 获取词性
            if count == number:
                break
            # print(TopWord + '\t', str(Frequency) + '\t',
            #       list(En2Cn_Pro.values())[list(En2Cn_Pro.keys()).index(POS.flag)])  # 逐行输出数据
            # fileOut.write(TopWord + '\t' + str(Frequency) + '\t' + list(En2Cn_Pro.values())[
            #     list(En2Cn_Pro.keys()).index(POS.flag)] + '\n')  # 逐行写入str格式数据
            if Frequency < number:
                break
            print(TopWord + '\t', str(Frequency))  # 逐行输出数据
            fileOut.write(TopWord + '\t' + str(Frequency) + '\n')  # 逐行写入str格式数据
            count += 1
    fileOut.close()  # 关闭文件

def make_word_cloud(object_list):
    # 词频展示
    print ('\n开始制作词云……')  # 提示当前状态
    word_counts = collections.Counter(object_list)
    mask = numpy.array(Image.open(background))  # 定义词频背景
    wc = wordcloud.WordCloud(
        font_path='file/simfang.ttf',  # 设置字体（这里选择“仿宋”）
        background_color='white',  # 背景颜色
        mask=mask,  # 文字颜色+形状（有mask参数再设定宽高是无效的）
        max_words=number,  # 显示词数
        max_font_size=150  # 最大字号
    )

    wc.generate_from_frequencies(word_counts)  # 从字典生成词云
    wc.recolor(color_func=wordcloud.ImageColorGenerator(mask))  # 将词云颜色设置为背景图方案
    plt.figure('词云')  # 弹框名称与大小
    plt.subplots_adjust(top=0.99, bottom=0.01, right=0.99, left=0.01, hspace=0, wspace=0)  # 调整边距
    plt.imshow(wc, cmap=plt.cm.gray, interpolation='bilinear')  # 处理词云
    plt.axis('off')  # 关闭坐标轴
    print ('制作完成！')  # 提示当前状态
    plt.show()

if __name__ == '__main__':

    file = 'file/file_1'
    number = 10 # top number
    word_lists = read_and_cut_word(file=file)
    word_frequency_count_and_output(word_lists, number)
    make_word_cloud(word_lists)