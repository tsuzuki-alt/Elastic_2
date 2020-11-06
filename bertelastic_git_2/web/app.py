import os
from pprint import pprint

from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
from bert_serving.client import BertClient
import sentencepiece as spm

# add for w2v
import numpy as np
from gensim.models import KeyedVectors
#model = KeyedVectors.load_word2vec_format('./model/clause.vec.bin', binary=True)
wv = KeyedVectors.load_word2vec_format('./entity_vector/entity_vector.model.bin', binary=True)

# add for mecab
import MeCab
mc = MeCab.Tagger('-r/etc/mecabrc -Owakati')

SEARCH_SIZE = 5
#INDEX_NAME = os.environ['INDEX_NAME']
INDEX_NAME = "clausesearch_2"
app = Flask(__name__)

s = spm.SentencePieceProcessor()
s.Load('./model/wiki-ja.model')

def parse(text):
    text = text.lower()
    return s.EncodeAsPieces(text)

def avg_feature_vector(sentence):
    #words = parse(sentence)
    words = mc.parse(sentence)
    feature_vec = np.zeros(200)
    unk_count = 0
    for word in words:
        try:
            feature_vec = np.add(feature_vec, wv.get_vector(word))
        except KeyError:
            unk_count += 1
    word_count = len(words) - unk_count
    if len(words) > 0:
        feature_vec = np.divide(feature_vec, word_count).tolist()
    return feature_vec

# mecab 品詞を限定する場合
'''
mc = MeCab.Tagger('-r/etc/mecabrc')

def avg_feature_vector(sentence):
    node = mc.parseToNode(sentence)
    sum_vec = np.zeros(200)
    word_count = 0
    while node:
        fields = node.feature.split(",")
        if fields[0] == '名詞' or fields[0] == '動詞' or fields[0] == '形容詞':
            sum_vec += wv[node.surface]
            word_count += 1
        node = node.next
    feature_vec_2 = np.divide(sum_vec, word_count).tolist()
    return feature_vec
'''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def analyzer():
    bc = BertClient(ip='bertserving', output_fmt='list')
    client = Elasticsearch('elasticsearch:9200')

    query = request.args.get('q')
    query_vector = bc.encode([parse(query)], is_tokenized=True)[0]
    query_vector_w2v = avg_feature_vector(query)
    
    # script_query = {
    #     "script_score": {
    #         "query": {"match_all": {}},
    #         "script": {
    #             "source": "cosineSimilarity(params.query_vector, doc['text_vector']) + 1.0",
    #             "params": {"query_vector": query_vector}
    #         }
    #     }
    # }
    
    w2v_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['text_vector']) + 1.0",
                "params": {"query_vector": query_vector_w2v}
            }
        }
    }

    normal_query = { "match" : { "text" : query } }
    
    '''
    response = client.search(
         index=INDEX_NAME,
         body={
             "size": SEARCH_SIZE,
             "query": script_query,
             "_source": {"includes": ["title", "text"]}
         }
     )
    '''

    response2 = client.search(
        index=INDEX_NAME,
        body={
            "size": SEARCH_SIZE,
            "query": normal_query,
            "_source": {"includes": ["title", "text"]}
        }
    )
    
    response3 = client.search(
        index=INDEX_NAME,
        body={
            "size": SEARCH_SIZE,
            "query": w2v_query,
            "_source": {"includes": ["title", "text"]}
        }
    )

    # pprint(response)
    pprint(response2)
    pprint(response3)
    return jsonify(response3)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
