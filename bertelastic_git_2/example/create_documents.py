"""
Example script to create elasticsearch documents.
"""
import argparse
import json

import pandas as pd
from bert_serving.client import BertClient
bc = BertClient(output_fmt='list')

# add for unicode error
import codecs

# add for w2v
import numpy as np
from gensim.models import KeyedVectors
#model = KeyedVectors.load_word2vec_format('./web/model/clause.vec.bin', binary=True)
model = KeyedVectors.load_word2vec_format('./web/entity_vector/entity_vector.model.bin', binary=True)

# MeCab
import MeCab
mc = MeCab.Tagger('-r/etc/mecabrc -Owakati')

# ADD
import sentencepiece as spm
s = spm.SentencePieceProcessor()
s.Load('./bertserving/bert-jp/wiki-ja.model')

def create_document(doc, emb, index_name):
    return {
        '_op_type': 'index',
        '_index': index_name,
        'text': doc['text'],
        'title': doc['title'],
        'text_vector': emb
    }

def load_dataset(path):
    docs = []
# add for unicode error
    with codecs.open(path, "r", "utf-8", "ignore") as file:
        df = pd.read_table(file, delimiter=",")
    # df = pd.read_csv(path)
        for row in df.iterrows():
            series = row[1]
            doc = {
                'title': series.Title,
                'text': series.Description
            }
            docs.append(doc)
    return docs


def bulk_predict(docs, batch_size=256):
    """Predict bert embeddings."""
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i: i+batch_size]
        embeddings = bc.encode([doc['text'] for doc in batch_docs])
        for emb in embeddings:
            yield emb

# ADD
def parse(text):
    text = text.lower()
    return s.EncodeAsPieces(text)

def bulk_predict_jp(docs, batch_size=256):
    """Predict bert embeddings."""
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i: i+batch_size]
        embeddings = bc.encode([s.EncodeAsPieces(doc['text']) for doc in batch_docs], is_tokenized=True)
        for emb in embeddings:
            yield emb

def avg_feature_vector(texts):
    feature_vecs = []
    for words in texts:
        feature_vec = np.zeros(200)
        unk_count = 0
        for word in words:
            try:
                feature_vec = np.add(feature_vec, model.get_vector(word))
            except KeyError:
                unk_count += 1
        word_count = len(words) - unk_count
        if len(words) > 0:
            feature_vec = np.divide(feature_vec, word_count).tolist()
        feature_vecs.append(feature_vec)
    return feature_vecs

def bulk_w2v(docs, batch_size=256):
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i: i+batch_size]
        #embeddings = avg_feature_vector([s.EncodeAsPieces(doc['text']) for doc in batch_docs])
        embeddings = avg_feature_vector([mc.parse(doc['text']) for doc in batch_docs])
        for emb in embeddings:
            yield emb

def main(args):
    docs = load_dataset(args.data)
    with open(args.save, 'w') as f:
        for doc, emb in zip(docs, bulk_w2v(docs)):
            d = create_document(doc, emb, args.index_name)
            f.write(json.dumps(d) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating elasticsearch documents.')
    parser.add_argument('--data', help='data for creating documents.')
    parser.add_argument('--save', default='documents.jsonl', help='created documents.')
    parser.add_argument('--index_name', default='clausesearch', help='Elasticsearch index name.')
    args = parser.parse_args()
    main(args)
