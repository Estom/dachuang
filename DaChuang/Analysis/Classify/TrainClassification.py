#coding=utf-8

"""
脚本名称 : TrainClassification.py
脚本作用 : 构建分类器
"""

import sys
import MySQLdb
import FormatData
import cPickle as pickle
from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB  # 导入多项式贝叶斯算法

# 配置utf-8输出环境
reload(sys)
sys.setdefaultencoding('utf-8')

# ###################基础常量###################################
catelist = (unicode('学科竞赛') , unicode('科研信息') , unicode('行政信息') , unicode('招生信息') , unicode('招聘就业') , unicode('校园活动') , unicode('升学留学') , unicode('生活娱乐'));
wordbag_path = "./train_word_bag_my/train_set_my.dat"
stopword_path = "./train_word_bag_my/hlt_stop_words.txt"
classification_path = "./train_word_bag_my/classification_NB.dat"
###############################################################

conn = MySQLdb.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = 'ykl123',
    db = 'dcdata',
    charset = "utf8",
)
cur = conn.cursor()
cur.execute("SET NAMES utf8")
aa = cur.execute("select * from train")

info = cur.fetchmany(aa)

TrainData = list(info)

# 开始分词
for ii in TrainData:
    ii1 = list(ii)
    ii1[1] = FormatData.TextCut(ii1[1]);
# 分词结束

# 建立Bounch数据
bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
bunch.target_name.extend(catelist)
for ii in TrainData:
    bunch.label.append(ii[2])
    bunch.filenames.append(ii[0])
    bunch.contents.append(ii[1])

'''''
with open(wordbag_path, "wb") as file_obj:
    pickle.dump(bunch, file_obj)
# 建立Bounch数据结束
'''

# 建立词向量空间
stpwrdlst = FormatData._readfile(stopword_path).splitlines()  # 读取停用词
# bunch = FormatData._writebunchobj(wordbag_path)

# 构建tf-idf词向量空间对象
train_tfidfspace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[],
                   vocabulary={})
# 构建使用TfidfVectorizer初始化向量空间模型
# 这里面有TF-IDF权重矩阵还有我们要的词向量空间坐标轴信息vocabulary_
train_vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.5)
''''' 
关于参数，你只需要了解这么几个就可以了： 
stop_words: 
传入停用词，以后我们获得vocabulary_的时候，就会根据文本信息去掉停用词得到 
vocabulary: 
之前说过，不再解释。 
sublinear_tf: 
计算tf值采用亚线性策略。比如，我们以前算tf是词频，现在用1+log(tf)来充当词频。 
smooth_idf: 
计算idf的时候log(分子/分母)分母有可能是0，smooth_idf会采用log(分子/(1+分母))的方式解决。默认已经开启，无需关心。 
norm: 
归一化，我们计算TF-IDF的时候，是用TF*IDF，TF可以是归一化的，也可以是没有归一化的，一般都是采用归一化的方法，默认开启. 
max_df: 
有些词，他们的文档频率太高了（一个词如果每篇文档都出现，那还有必要用它来区分文本类别吗？当然不用了呀），所以，我们可以 
设定一个阈值，比如float类型0.5（取值范围[0.0,1.0]）,表示这个词如果在整个数据集中超过50%的文本都出现了，那么我们也把它列 
为临时停用词。当然你也可以设定为int型，例如max_df=10,表示这个词如果在整个数据集中超过10的文本都出现了，那么我们也把它列 
为临时停用词。 
min_df: 
与max_df相反，虽然文档频率越低，似乎越能区分文本，可是如果太低，例如10000篇文本中只有1篇文本出现过这个词，仅仅因为这1篇 
文本，就增加了词向量空间的维度，太不划算。 
当然，max_df和min_df在给定vocabulary参数时，就失效了。 
'''

# 此时tdm里面存储的就是if-idf权值矩阵
train_tfidfspace.tdm = train_vectorizer.fit_transform(bunch.contents)
train_tfidfspace.vocabulary = train_vectorizer.vocabulary_
FormatData._writebunchobj(wordbag_path , train_tfidfspace);

# 训练分类器：输入词袋向量和分类标签，alpha:0.001 alpha越小，迭代次数越多，精度越高
clf = MultinomialNB(alpha=0.001).fit(train_tfidfspace.tdm, train_tfidfspace.label)

FormatData._writebunchobj(classification_path , clf);

predicted = clf.predict(train_tfidfspace.tdm)

cur.close()
conn.commit()
conn.close()

