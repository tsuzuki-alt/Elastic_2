#!/bin/sh
#w2vファイルのダウンロードと配置
mkdir ./web/entity_vector
FILE_ID=15n49D2BaB6lUVP2MvGJdT9gWtdmy47LU
FILE_NAME=./web/entity_vector/entity_vector.model.bin
curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=${FILE_ID}" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"  
curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=${FILE_ID}" -o ${FILE_NAME}
