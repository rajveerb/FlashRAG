# python profile_analysis_scripts/plot_retrieval.py --input_dir profile_logs --prefix retrieval_times_per_batch_iter_ --output_figs_dir profile_analysis_scripts/figs --output_stats_dir profile_analysis_scripts/stats 
import os
import matplotlib.pyplot as plt
import pandas as pd
import argparse, json

# take arguments from command line
parser = argparse.ArgumentParser(description='Plot and log retrieval time')
# profile_logs dir
parser.add_argument('--input_dir', required=True, help='Input directory containing log files')
# prefix of files to be parsed
# past_generation_result_iter_0.txt
parser.add_argument('--prefix', required=True, help='Prefix of files to be parsed')
# figs directory
parser.add_argument('--output_figs_dir', required=True, help='Output directory to save figures')
# stats directory
parser.add_argument('--output_stats_dir', required=True, help='Output directory to save stats')

args = parser.parse_args()

# read all log files in the input directory
log_files = os.listdir(args.input_dir)

# filter log files based on prefix
log_files = [f for f in log_files if f.startswith(args.prefix)]

# duration is for 0 to batch size - 1, default is 256
# {"id": [start_timestamp, duration]}


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
        for data in json_data:
            for key, value in data.items():
                    metric_data_per_log.append({'duration (s)': value[1]})
        iter_num = extract_iter_num(log_file)
        metric_data[iter_num] = metric_data_per_log

# generate log and plot per iter_num
for iter_num, metrics in metric_data.items():
    iter_data_dict = {'duration (s)': []}
    for data in metrics:
        iter_data_dict['duration (s)'].append(data['duration (s)'])
    
    iter_df = pd.DataFrame(iter_data_dict)
    
    # save the stats in a csv file per iter_num
    iter_df.describe().to_csv(os.path.join(args.output_stats_dir, f'retrieval_stats_iter_{iter_num}.csv'))
    
    # plot histogram of duration and save in output directory per iter_num
    plt.hist(iter_df['duration (s)'], bins=100)
    plt.xlabel('Duration (seconds)')
    plt.ylabel('Frequency')
    plt.title(f'Duration Histogram - Iter {iter_num}')
    plt.savefig(os.path.join(args.output_figs_dir, f'retrieval_histogram_iter_{iter_num}.png'))
    plt.close()
    
    # plot cdf of duration and save in output directory per iter_num
    plt.hist(iter_df['duration (s)'], bins=100, cumulative=True, density=True)
    plt.xlabel('Duration (seconds)')
    plt.title(f'Duration CDF - Iter {iter_num}')
    plt.savefig(os.path.join(args.output_figs_dir, f'retrieval_cdf_iter_{iter_num}.png'))
    plt.close()
