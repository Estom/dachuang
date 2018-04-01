# encoding=utf-8

import jieba
from networkx import from_scipy_sparse_matrix, pagerank
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import SQLconfig
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def cut_sentence(sentence):
    """ 
    分句 
    :param sentence: 
    :return: 
    """
    if not isinstance(sentence, unicode):
        sentence = sentence.decode('utf-8')
    delimiters = frozenset(u'。！？')
    buf = []
    for ch in sentence:
        buf.append(ch)
        if delimiters.__contains__(ch):
            yield ''.join(buf)
            buf = []
    if buf:
        yield ''.join(buf)

def load_stopwords(path='stop_words.txt'):
    """ 
    加载停用词 
    :param path: 
    :return: 
    """
    with open(path) as f:
        stopwords = f.readlines()
    stopwrdlist = []
    for i in stopwords:
        i1 = i.decode('gbk')
        i1 = i1.strip("\r\n")
        stopwrdlist.append(i1)
    return frozenset(stopwrdlist)

def cut_words(sentence):
    """ 
    分词 
    :param sentence: 
    :return: 
    """
    stopwords = load_stopwords()
    return filter(lambda x: not stopwords.__contains__(x), jieba.cut(sentence))


def get_abstract(content, size=3):
    """ 
    利用textrank提取摘要 
    :param content: 
    :param size: 
    :return: 
    """
    docs = list(cut_sentence(content))
    tfidf_model = TfidfVectorizer(tokenizer=jieba.cut, stop_words=load_stopwords())
    tfidf_matrix = tfidf_model.fit_transform(docs)
    normalized_matrix = TfidfTransformer().fit_transform(tfidf_matrix)
    similarity = from_scipy_sparse_matrix(normalized_matrix * normalized_matrix.T)
    scores = pagerank(similarity)
    tops = sorted(scores.iteritems(), key=lambda x: x[1], reverse=True)
    size = min(size, len(docs))
    indices = map(lambda x: x[0], tops)[:size]
    return map(lambda idx: docs[idx], indices)

i = -1
while True:
    i += 1
    state = SQLconfig.sql0.select('article', ['id', 'process_state'], None, 0, i)
    if len(state) == 0:
        break
    if (state[1] % 2**3)/(2**1) % 2 == 1:
        print "%d : id = %d文章已完成摘要" % (i, state[0])
        continue
    else:
        SQLconfig.sql0.update('article', {'process_state': state[1] % 2**3 + 2**1}, 'id = %d' % state[0])
        a = SQLconfig.sql0.select('article', ['article.desc'], None, 1, i)
        if a[0] is not None and len(a[0]) > 4: # 在微信中有一些文章是有摘要的，不需要重新生成摘要
            print "%d ：id = %d 文章来源存在摘要" % (i, state[0])
        else:
            info = SQLconfig.sql0.select('article', ['id', 'content'], None, 1, i)
            if len(info[1]) < 2:
                print "%d ：id = %d 文章太短不必要摘要" % (i, state[0])
                continue
            s = get_abstract(info[1])
            s[0] = s[0].strip('\r\n')
            s[0] = s[0].strip(' ')
            s[0] = s[0].replace(' ', '')
            s[0] = s[0].replace('\n', '')
            s[0] = s[0].replace('\r', '')
            s[0] = s[0].replace('\t', '')
            dic = {'article.desc': s[0]}
            SQLconfig.sql0.update('article', dic, 'id=%d' % info[0])
            print '%d: id = %d : %s' % (i, state[0], s[0])
