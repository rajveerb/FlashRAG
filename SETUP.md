
## Get corpus

```bash
wget https://huggingface.co/datasets/RUC-NLPIR/FlashRAG_datasets/resolve/main/retrieval-corpus/wiki18_100w.zip
mkdir -p corpus
unzip wiki18_100w.zip -d corpus
rm wiki18_100w.zip
```

## Get 2wikidata

```bash
wget https://huggingface.co/datasets/RUC-NLPIR/FlashRAG_datasets/resolve/main/2wikimultihopqa/dev.jsonl -P examples/methods/dataset/2wikidata/
```

## Build retrieval index

```bash
# Saves the index to indexes/e5-Flat.index
python -m flashrag.retriever.index_builder \
    --retrieval_method e5 \
    --model_path intfloat/e5-base-v2 \
    --corpus_path corpus/wiki18_100w.jsonl \
    --save_dir indexes/ \
    --use_fp16 \
    --max_length 512 \
    --batch_size 256 \
    --pooling_method mean \
    --faiss_type Flat
# To get info about number of vectors in the index
python scripts/get_no_vectors.py \
    --index_path indexes/e5-Flat.index
```

## Run method `iterretgen`

```bash
# will store the config used in the run to `examples/methods/output`
# method_name options can be found in `examples/methods/run_exp.py`
 python examples/methods/run_exp.py --method_name 'iterretgen' \
    --split 'dev' \
    --dataset_name '2wikidata' \
    --gpu_id '0,1' \
    --save_metrics \
    --metrics_log_dir ./profile_logs/IterativePipeline \ 
    --config_path ./examples/methods/my_config.yaml
```