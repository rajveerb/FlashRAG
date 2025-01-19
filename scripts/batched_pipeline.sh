# !/bin/bash

python examples/methods/run_exp.py --method_name 'iterretgen' \
--split 'dev' \
--dataset_name '2wikidata' \
--gpu_id '0,1' \
--save_metrics \
--metrics_log_dir ./profile_logs/ProfileIterativePipeline \
--profile \
--override_batch_size 256 \
--iter_num 1 \
--config_path ./examples/methods/my_config.yaml
echo "Run with batch size 256 completed successfully."

python examples/methods/run_exp.py --method_name 'iterretgen' \
--split 'dev' \
--dataset_name '2wikidata' \
--gpu_id '0,1' \
--save_metrics \
--metrics_log_dir ./profile_logs/ProfileIterativePipeline \
--profile \
--override_batch_size 128 \
--iter_num 1 \
--config_path ./examples/methods/my_config.yaml
echo "Run with batch size 128 completed successfully."

python examples/methods/run_exp.py --method_name 'iterretgen' \
--split 'dev' \
--dataset_name '2wikidata' \
--gpu_id '0,1' \
--save_metrics \
--metrics_log_dir ./profile_logs/ProfileIterativePipeline \
--profile \
--override_batch_size 64 \
--iter_num 1 \
--config_path ./examples/methods/my_config.yaml
echo "Run with batch size 64 completed successfully."

python examples/methods/run_exp.py --method_name 'iterretgen' \
--split 'dev' \
--dataset_name '2wikidata' \
--gpu_id '0,1' \
--save_metrics \
--metrics_log_dir ./profile_logs/ProfileIterativePipeline \
--profile \
--override_batch_size 32 \
--iter_num 1 \
--config_path ./examples/methods/my_config.yaml
echo "Run with batch size 32 completed successfully."

python examples/methods/run_exp.py --method_name 'iterretgen' \
--split 'dev' \
--dataset_name '2wikidata' \
--gpu_id '0,1' \
--save_metrics \
--metrics_log_dir ./profile_logs/ProfileIterativePipeline \
--profile \
--override_batch_size 16 \
--iter_num 1 \
--config_path ./examples/methods/my_config.yaml
echo "Run with batch size 16 completed successfully."

python examples/methods/run_exp.py --method_name 'iterretgen' \
--split 'dev' \
--dataset_name '2wikidata' \
--gpu_id '0,1' \
--save_metrics \
--metrics_log_dir ./profile_logs/ProfileIterativePipeline \
--profile \
--override_batch_size 8 \
--iter_num 1 \
--config_path ./examples/methods/my_config.yaml
echo "Run with batch size 8 completed successfully."

python examples/methods/run_exp.py --method_name 'iterretgen' \
--split 'dev' \
--dataset_name '2wikidata' \
--gpu_id '0,1' \
--save_metrics \
--metrics_log_dir ./profile_logs/ProfileIterativePipeline \
--profile \
--override_batch_size 512 \
--iter_num 1 \
--config_path ./examples/methods/my_config.yaml
echo "Run with batch size 512 completed successfully."

python examples/methods/run_exp.py --method_name 'iterretgen' \
--split 'dev' \
--dataset_name '2wikidata' \
--gpu_id '0,1' \
--save_metrics \
--metrics_log_dir ./profile_logs/ProfileIterativePipeline \
--profile \
--override_batch_size 1024 \
--iter_num 1 \
--config_path ./examples/methods/my_config.yaml
echo "Run with batch size 1024 completed successfully."