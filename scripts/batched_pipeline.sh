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

python profile_analysis_scripts/plot_retrieval_breakdown.py --input_dir profile_logs/ProfileIterativePipeline/batch_size_256/retrieval --prefix retrieval_times_per_batch_iter --output_figs_dir profile_analysis_scripts/figs/ProfileIterativePipeline/batch_size_256/retrieval --output_stats_dir profile_analysis_scripts/stats/ProfileIterativePipeline/batch_size_8/retrieval --batch_size 8

python profile_analysis_scripts/plot_retrieval_breakdown.py --input_dir profile_logs/ProfileIterativePipeline/batch_size_128/retrieval --prefix retrieval_times_per_batch_iter --output_figs_dir profile_analysis_scripts/figs/ProfileIterativePipeline/batch_size_128/retrieval --output_stats_dir profile_analysis_scripts/stats/ProfileIterativePipeline/batch_size_128/retrieval --batch_size 128

python profile_analysis_scripts/plot_retrieval_breakdown.py --input_dir profile_logs/ProfileIterativePipeline/batch_size_64/retrieval --prefix retrieval_times_per_batch_iter --output_figs_dir profile_analysis_scripts/figs/ProfileIterativePipeline/batch_size_64/retrieval --output_stats_dir profile_analysis_scripts/stats/ProfileIterativePipeline/batch_size_64/retrieval --batch_size 64

python profile_analysis_scripts/plot_retrieval_breakdown.py --input_dir profile_logs/ProfileIterativePipeline/batch_size_32/retrieval --prefix retrieval_times_per_batch_iter --output_figs_dir profile_analysis_scripts/figs/ProfileIterativePipeline/batch_size_32/retrieval --output_stats_dir profile_analysis_scripts/stats/ProfileIterativePipeline/batch_size_32/retrieval --batch_size 32

python profile_analysis_scripts/plot_retrieval_breakdown.py --input_dir profile_logs/ProfileIterativePipeline/batch_size_16/retrieval --prefix retrieval_times_per_batch_iter --output_figs_dir profile_analysis_scripts/figs/ProfileIterativePipeline/batch_size_16/retrieval --output_stats_dir profile_analysis_scripts/stats/ProfileIterativePipeline/batch_size_16/retrieval --batch_size 16

python profile_analysis_scripts/plot_retrieval_breakdown.py --input_dir profile_logs/ProfileIterativePipeline/batch_size_8/retrieval --prefix retrieval_times_per_batch_iter --output_figs_dir profile_analysis_scripts/figs/ProfileIterativePipeline/batch_size_8/retrieval --output_stats_dir profile_analysis_scripts/stats/ProfileIterativePipeline/batch_size_8/retrieval --batch_size 8

python profile_analysis_scripts/plot_retrieval_breakdown.py --input_dir profile_logs/ProfileIterativePipeline/batch_size_512/retrieval --prefix retrieval_times_per_batch_iter --output_figs_dir profile_analysis_scripts/figs/ProfileIterativePipeline/batch_size_512/retrieval --output_stats_dir profile_analysis_scripts/stats/ProfileIterativePipeline/batch_size_512/retrieval --batch_size 512

python profile_analysis_scripts/plot_retrieval_breakdown.py --input_dir profile_logs/ProfileIterativePipeline/batch_size_1024/retrieval --prefix retrieval_times_per_batch_iter --output_figs_dir profile_analysis_scripts/figs/ProfileIterativePipeline/batch_size_1024/retrieval --output_stats_dir profile_analysis_scripts/stats/ProfileIterativePipeline/batch_size_1024/retrieval --batch_size 1024

echo "All runs completed successfully."