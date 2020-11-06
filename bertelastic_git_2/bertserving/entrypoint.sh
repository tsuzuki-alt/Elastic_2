#!/bin/sh
bert-serving-start -num_worker=1 -max_seq_len=100 -show_tokens_to_client -model_dir /model
