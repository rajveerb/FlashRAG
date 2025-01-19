# python profile_analysis_scripts/plot_retrieval_breakdown.py --input_dir profile_logs/ProfileIterativePipeline/batch_size_256/retrieval --prefix retrieval_times_per_batch_iter --output_figs_dir profile_analysis_scripts/figs/ProfileIterativePipeline/batch_size_256/retrieval --output_stats_dir profile_analysis_scripts/stats/ProfileIterativePipeline/batch_size_256/retrieval --batch_size 256
import os
import matplotlib.pyplot as plt
import pandas as pd
import argparse, json

# take arguments from command line
parser = argparse.ArgumentParser(description='Plot and log prompt and response length')
# profile_logs dir
parser.add_argument('--input_dir', required=True, help='Input directory containing log files')
# prefix of files to be parsed
parser.add_argument('--prefix', required=True, help='Prefix of files to be parsed')
# figs directory
parser.add_argument('--output_figs_dir', required=True, help='Output directory to save figures')
# stats directory
parser.add_argument('--output_stats_dir', required=True, help='Output directory to save stats')
# batch size
parser.add_argument('--batch_size', required=True, help='Batch size')

args = parser.parse_args()

# read all log files in the input directory
log_files = os.listdir(args.input_dir)

# create output directories if they don't exist
os.makedirs(args.output_figs_dir, exist_ok=True)
os.makedirs(args.output_stats_dir, exist_ok=True)

# filter log files based on prefix
log_files = [f for f in log_files if f.startswith(args.prefix)]

# Given log file with format *iter_x.txt extract iter_x
def extract_iter_num(log_file):
    return log_file.split('_')[-1].split('.')[0]

# parse log files and store in a list
metric_data = {}
# read as json 
for log_file in log_files:
    with open(os.path.join(args.input_dir, log_file), 'r') as f:
        json_data = json.load(f)
        metric_data_per_log = []
        for data in json_data.values():
            timing_data = data['batch_timing']["0"]
            # below is what timing_data looks like
            # {
            #     "embedding_time": [
            #         1737147917904585486,
            #         63377723 # time in ns
            #     ],
            #     "vector_search_time": [
            #         1737147917967963209,
            #         92621378851 # time in ns
            #     ],
            #     "load_docs_time": [
            #         1737148010589342060,
            #         47527875 # time in ns
            #     ],
            #     "overall_time": [
            #         1737147917904585486,
            #         92732284449 # time in ns
            #     ]
            # }
            metric_data_per_log.append(timing_data)
        iter_num = extract_iter_num(log_file)
        metric_data[iter_num] = metric_data_per_log

# generate log and plot per iter_num
for iter_num, metrics in metric_data.items():
    iter_data_dict = {
        'embedding_time': [],
        'vector_search_time': [],
        'load_docs_time': [],
        'overall_time': []
    }
    for data in metrics:
        iter_data_dict['embedding_time'].append(data['embedding_time'][1])
        iter_data_dict['vector_search_time'].append(data['vector_search_time'][1])
        iter_data_dict['load_docs_time'].append(data['load_docs_time'][1])
        iter_data_dict['overall_time'].append(data['overall_time'][1])
    
    iter_df = pd.DataFrame(iter_data_dict)
    
    # Determine the scale (ms, µs, s) for each metric based on its maximum value
    scales = {}
    units = {}
    for metric in iter_data_dict.keys():
        max_value = iter_df[metric].max()
        if max_value > 1e9:
            scales[metric] = 1e9
            units[metric] = 's'
        elif max_value > 1e6:
            scales[metric] = 1e6
            units[metric] = 'ms'
        else:
            scales[metric] = 1e3
            units[metric] = 'µs'
        iter_df[metric] = iter_df[metric] / scales[metric]
    
    # save the stats in a csv file per iter_num
    iter_df.describe().to_csv(os.path.join(args.output_stats_dir, f'timing_stats_iter_{iter_num}.csv'))
    
    # plot histogram of each timing metric and save in output directory per iter_num
    for metric in iter_data_dict.keys():
        plt.hist(iter_df[metric], bins=100)
        plt.xlabel(f'{metric.replace("_", " ").title()} ({units[metric]})')
        plt.ylabel('Frequency')
        plt.title(f'{metric.replace("_", " ").title()} Histogram - Iter {iter_num} - Batch Size {args.batch_size}')
        plt.savefig(os.path.join(args.output_figs_dir, f'{metric}_histogram_iter_{iter_num}.png'))
        plt.close()
    
    # plot cdf of each timing metric and save in output directory per iter_num
    for metric in iter_data_dict.keys():
        plt.hist(iter_df[metric], bins=100, cumulative=True, density=True)
        plt.xlabel(f'{metric.replace("_", " ").title()} ({units[metric]})')
        plt.title(f'{metric.replace("_", " ").title()} CDF - Iter {iter_num} - Batch Size {args.batch_size}')
        plt.savefig(os.path.join(args.output_figs_dir, f'{metric}_cdf_iter_{iter_num}.png'))
        plt.close()
    
    # Normalize times to a common scale based on the maximum value across all metrics
    max_value = max(scales.values())
    # get the unit key with the maximum value
    max_unit = units[[k for k, v in scales.items() if v == max(scales.values())][0]]
    iter_df['embedding_time'] = iter_df['embedding_time'] * scales['embedding_time'] / max_value
    iter_df['vector_search_time'] = iter_df['vector_search_time'] * scales['vector_search_time'] / max_value
    iter_df['load_docs_time'] = iter_df['load_docs_time'] * scales['load_docs_time'] / max_value
    normalized_unit = units[[k for k, v in scales.items() if v == max(scales.values())][0]]

    # plot stacked bar chart of embedding_time, vector_search_time, and load_docs_time
    iter_df[['embedding_time', 'vector_search_time', 'load_docs_time']].plot(kind='bar', stacked=True)
    plt.ylabel(f'Normalized Time ({max_unit})')
    plt.title(f'Stacked Bar Chart of Timing Metrics - Iter {iter_num} - Batch Size {args.batch_size}')
    plt.savefig(os.path.join(args.output_figs_dir, f'stacked_bar_timing_metrics_iter_{iter_num}.png'))
    plt.close()