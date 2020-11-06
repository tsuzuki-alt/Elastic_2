# bertelastic_addw2vからの変更点
### ＜example＞
●create_documents.py
* Tokenize処理をsentencepieceからMeCabに差し替え

### ＜web＞
●entity_vector
* 学習済word2vecモデル(entity_vector.model.bin)を格納
* 取得元：http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/
●app.py
* Tokenize処理をsentencepieceからMeCabに差し替え
●Dockerfile
* MeCabのインストール・設定処理を追加


# bertelasticからの変更点
### ＜example＞
●create_documents.py
* word2vecモデルによるベクトル化の処理を追加
●requirements.txt
* sentencepiece, gensimを追加
●index.json
* word2vec用に次元数を200に変更

### ＜web＞
●model
* word2vecモデルを格納（sentencepieceのアンダースコア対策のため修正予定）
●app.py
* word2vecを使用するクエリーを追加（response3）(response, response3はいずれかコメントアウトしないと次元数の不一致でエラー)
●requirements.txt
* gensimを追加

# オリジナルからの変更点
### ＜bertserving＞
●entrypoint.sh
* -max_seq_len=100 -show_tokens_to_clientのパラメータを追加

### ＜example＞
●create_documents.py
* sentencepieceによる独自のTokenize処理を追加
●create_documents_json.py
* WikipediaのクイズデータセットのJSONファイルをElasticSearch用のデータに変換するためのスクリプトを追加
●create_index.py
* elasticsearchのindex名を修正
●requirements.txt
* bertservingのバージョンを修正

### ＜web＞
●model
* sentencepiece用のボキャブラリーファイルを格納
●app.py
* sentencepieceによる独自のTokenize処理を追加
* 通常の単語検索用のクエリーを追加（response2）
●requirements.txt
* bertservingのバージョンを修正
* sentencepieceを追加

### ＜root＞
●docker-compose.yml
* kibanaを追加
●.devcontainer
* VS Code用の設定を追加

# 使い方
### 1. BERTの事前学習モデルをダウンロード

### 2. Run Docker containers
```bash
$ cd [project_folder]
$ docker-compose up
```

### 3. ElasticSearchへインデックスの作成
・WikiQAの場合は、index_nameに「wikiqa」へ変更
```bash
$ python example/create_index.py --index_file=example/index.json --index_name=jobsearch
```

### 4. ElasticSearchへ登録する用のjsonlファイルの作成
・WikiQAの場合は、index_nameに「wikiqa」へ変更
・WikiQAの場合は、dataに「ダウンロードしてきたwikiqaデータセットのjson」へ変更
<https://www.nlp.ecei.tohoku.ac.jp/projects/jaqket/>

```bash
$ python example/create_documents.py --data=example/example.csv --index_name=jobsearch
```
実行するとプロジェクトルートに「documents.jsonl」というファイルが生成される。

### 5. ElasticSearchへのドキュメントの登録
※プロジェクトルートの「documents.jsonl」を登録する。
```bash
$ python example/index_documents.py
```

### 6. ブラウザで確認
kibana <http://localhost:5601/>
WebAP <http://127.0.0.1:5000>
※wikiqaデータセットで試す場合はapp.pyのINDEX_NAMEを「wikiqa」に変えて再起動すればOK(docker-compose down & docker-compose up)

# Elasticsearch meets BERT

Below is a job search example:

![An example of bertsearch](./docs/example.png)

## System architecture

![System architecture](./docs/architecture.png)

## Getting Started

### 1. Download a pretrained BERT model

<details>
 <summary>List of released pretrained BERT models (click to expand...)</summary>


<table>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip">BERT-Base, Uncased</a></td><td>12-layer, 768-hidden, 12-heads, 110M parameters</td></tr>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-24_H-1024_A-16.zip">BERT-Large, Uncased</a></td><td>24-layer, 1024-hidden, 16-heads, 340M parameters</td></tr>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_10_18/cased_L-12_H-768_A-12.zip">BERT-Base, Cased</a></td><td>12-layer, 768-hidden, 12-heads , 110M parameters</td></tr>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_10_18/cased_L-24_H-1024_A-16.zip">BERT-Large, Cased</a></td><td>24-layer, 1024-hidden, 16-heads, 340M parameters</td></tr>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_11_23/multi_cased_L-12_H-768_A-12.zip">BERT-Base, Multilingual Cased (New)</a></td><td>104 languages, 12-layer, 768-hidden, 12-heads, 110M parameters</td></tr>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_11_03/multilingual_L-12_H-768_A-12.zip">BERT-Base, Multilingual Cased (Old)</a></td><td>102 languages, 12-layer, 768-hidden, 12-heads, 110M parameters</td></tr>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip">BERT-Base, Chinese</a></td><td>Chinese Simplified and Traditional, 12-layer, 768-hidden, 12-heads, 110M parameters</td></tr>
</table>

</details>

```bash
$ wget https://storage.googleapis.com/bert_models/2018_10_18/cased_L-12_H-768_A-12.zip
$ unzip cased_L-12_H-768_A-12.zip
```

### 2. Set environment variables

You need to set a pretrained BERT model and Elasticsearch's index name as environment variables:

```bash
$ export PATH_MODEL=./cased_L-12_H-768_A-12
$ export INDEX_NAME=jobsearch
```

### 3. Run Docker containers


```bash
$ docker-compose up
```

**CAUTION**: If possible, assign high memory(more than `8GB`) to Docker's memory configuration because BERT container needs high memory.

### 4. Create index

You can use the create index API to add a new index to an Elasticsearch cluster. When creating an index, you can specify the following:

* Settings for the index
* Mappings for fields in the index
* Index aliases

For example, if you want to create `jobsearch` index with `title`, `text` and `text_vector` fields, you can create the index by the following command:

```bash
$ python example/create_index.py --index_file=example/index.json --index_name=jobsearch
# index.json
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1
  },
  "mappings": {
    "dynamic": "true",
    "_source": {
      "enabled": "true"
    },
    "properties": {
      "title": {
        "type": "text"
      },
      "text": {
        "type": "text"
      },
      "text_vector": {
        "type": "dense_vector",
        "dims": 768
      }
    }
  }
}
```

**CAUTION**: The `dims` value of `text_vector` must need to match the dims of a pretrained BERT model.

### 5. Create documents

Once you created an index, you’re ready to index some document. The point here is to convert your document into a vector using BERT. The resulting vector is stored in the `text_vector` field. Let`s convert your data into a JSON document:

```bash
$ python example/create_documents.py --data=example/example.csv --index_name=jobsearch
# example/example.csv
"Title","Description"
"Saleswoman","lorem ipsum"
"Software Developer","lorem ipsum"
"Chief Financial Officer","lorem ipsum"
"General Manager","lorem ipsum"
"Network Administrator","lorem ipsum"
```

After finishing the script, you can get a JSON document like follows:

```python
# documents.jsonl
{"_op_type": "index", "_index": "jobsearch", "text": "lorem ipsum", "title": "Saleswoman", "text_vector": [...]}
{"_op_type": "index", "_index": "jobsearch", "text": "lorem ipsum", "title": "Software Developer", "text_vector": [...]}
{"_op_type": "index", "_index": "jobsearch", "text": "lorem ipsum", "title": "Chief Financial Officer", "text_vector": [...]}
...
```

### 6. Index documents

After converting your data into a JSON, you can adds a JSON document to the specified index and makes it searchable.

```bash
$ python example/index_documents.py
```

### 7. Open browser

Go to <http://127.0.0.1:5000>.
