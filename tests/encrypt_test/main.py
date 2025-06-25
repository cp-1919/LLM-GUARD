from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from app.utils import blur
import re
from openai import OpenAI
import editdistance

class ParseError(Exception):
    """结果提取错误"""

def call_gpt(data):
    for i in range(3):
        try:
            client = OpenAI(api_key="sk-518314a2e32148879e71595aad276166", base_url="https://api.deepseek.com")
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "user",
                        "content": f"Please extract english words from following words, wrap result in label<result></result>:{data}"},
                ],
                stream=False
            )
            # 防止上文提及的文本被分割
            print('Result', response.choices[0].message.content)
            res = response.choices[0].message.content.split('</result>')[-2].split('<result>')[-1]
            res = re.sub(r'\s+', ' ', res.replace('\n',' ').replace(',', ' '))
            return res
        except Exception as e:
            print('Error happens in call_gpt:', e)
            print('From', data)
            print('Size', len(data))
            continue
    raise ParseError()

def jaccard_similarity(str1, str2):
    list1 = str1.split(' ')
    list2 = str2.split(' ')
    intersection = len(set(list1).intersection(list2))
    union = len(set(list1)) + len(set(list2)) - intersection
    return intersection / float(union)

def vector_similarity(str1, str2):
    # 使用TF-IDF向量化器将文本转换为向量
    vectorizer = TfidfVectorizer().fit_transform([str1, str2])
    # 计算余弦相似度
    cosine_sim = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
    return cosine_sim[0][0]

def filter_letter(c):
    return c.isalpha() or c==' '

def eval_category(category):
    # 从数据集获取对应类别的数据
    newsgroups = fetch_20newsgroups(
        subset='all',
        categories=[category],
        remove=('headers', 'footers', 'quotes')
    )
    data = newsgroups.data
    vector_similarity_total = 0 # 总向量相似度
    jaccard_similarity_total = 0 # 总jaccard相似度
    editdistance_total = 0 # 总编辑距离
    total_word = 0 # 总字数

    total_temp = 0 # 总样本量
    with open(category+'.txt', 'a', encoding='utf-8') as f:
        data_idx = 0 # 样本容量
        while total_temp!=50: # 采集100组数据
            print('Process ', category, ' ', total_temp)
            text = ''
            while len(data[data_idx])+len(text) < 2000: # 每组数据拼接为2000字左右
                text += data[data_idx]
                data_idx += 1
            if len(text) == 0:
                if len(data[data_idx])>4000:
                    data_idx += 1
                    continue
                text = data[data_idx]
                data_idx += 1
            # 规范化样本
            text = text.replace('\n', ' ')
            text = re.sub(r'\s+', ' ', text)
            text = ''.join(filter(filter_letter, text))

            blur_text = blur(text) # 加密

            try_time = 0
            while try_time!=3:
                try:
                    res = call_gpt(blur_text)
                    # 计算相似度
                    distance = editdistance.eval(text.lower(), res.lower())
                    vector_similarity_rate = vector_similarity(text, res)
                    jaccard_similarity_rate = jaccard_similarity(text, res)
                    print(
                        f"dest:{res}\ntotal={len(text)} "
                        f"vector={vector_similarity_rate} "
                        f"jaccard={jaccard_similarity_rate} "
                        f"editdistance={distance}\n"
                    )
                except:
                    try_time += 1
                    continue
                if vector_similarity_rate > 0.5:
                    break
                try_time += 1
            if try_time == 3:
                continue

            total_temp += 1

            # 统计
            total_word += len(text)
            vector_similarity_total += vector_similarity_rate
            jaccard_similarity_total += jaccard_similarity_rate
            editdistance_total += distance

            # 生成报告
            f.write(
                f"orig:{text}\ndest:{res}\ntotal={len(text)} "
                f"vector={vector_similarity_rate} "
                f"jaccard={jaccard_similarity_rate} "
                f"editdistance={distance}\n"
            )
        f.write(f"result: "
            f"vector={vector_similarity_total/total_temp} "
            f"jaccard={jaccard_similarity_total/total_temp} "
            f"editdistance={editdistance_total} "
            f"total={total_word}"
        )

def main(start_idx):
    categories = ['alt.atheism',
     'comp.graphics',
     'comp.os.ms-windows.misc',
     'comp.sys.ibm.pc.hardware',
     'comp.sys.mac.hardware',
     'comp.windows.x',
     'misc.forsale',
     'rec.autos',
     'rec.motorcycles',
     'rec.sport.baseball',
     'rec.sport.hockey',
     'sci.crypt',
     'sci.electronics',
     'sci.med',
     'sci.space',
     'soc.religion.christian',
     'talk.politics.guns',
     'talk.politics.mideast',
     'talk.politics.misc',
     'talk.religion.misc']

    for i in range(start_idx, len(categories)):
        eval_category(categories[i])


if __name__ == '__main__':
    main(6)
