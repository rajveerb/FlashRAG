# python profile_analysis_scripts/plot_prompt_prediction.py --input_dir profile_logs --prefix past_generation_result_iter_ --output_figs_dir profile_analysis_scripts/figs --output_stats_dir profile_analysis_scripts/stats
import os
import matplotlib.pyplot as plt
import pandas as pd
import argparse, json

# take arguments from command line
parser = argparse.ArgumentParser(description='Plot and log prompt and response length')
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

# "prompt": "xxx", "prediction": "yyy"


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
            metric_data_per_log.append({'prompt_length': len(data['prompt']), 'response_length': len(data['prediction'])})
        iter_num = extract_iter_num(log_file)
        metric_data[iter_num] = metric_data_per_log

# generate log and plot per iter_num
for iter_num, metrics in metric_data.items():
    iter_data_dict = {'prompt_length': [], 'response_length': []}
    for data in metrics:
        iter_data_dict['prompt_length'].append(data['prompt_length'])
        iter_data_dict['response_length'].append(data['response_length'])
    
    iter_df = pd.DataFrame(iter_data_dict)
    
    # save the stats in a csv file per iter_num
    iter_df.describe().to_csv(os.path.join(args.output_stats_dir, f'prompt_response_stats_iter_{iter_num}.csv'))
    
    # plot histogram of prompt length and response length and save in output directory per iter_num
    plt.hist(iter_df['prompt_length'], bins=100)
    plt.xlabel('Prompt Length')
    plt.ylabel('Frequency')
    plt.title(f'Prompt Length Histogram - Iter {iter_num}')
    plt.savefig(os.path.join(args.output_figs_dir, f'prompt_length_histogram_iter_{iter_num}.png'))
    plt.close()
    
    plt.hist(iter_df['response_length'], bins=100)
    plt.xlabel('Response Length')
    plt.ylabel('Frequency')
    plt.title(f'Response Length Histogram - Iter {iter_num}')
    plt.savefig(os.path.join(args.output_figs_dir, f'response_length_histogram_iter_{iter_num}.png'))
    plt.close()
    
    # plot cdf of prompt length and response length and save in output directory per iter_num
    plt.hist(iter_df['prompt_length'], bins=100, cumulative=True, density=True)
    plt.xlabel('Prompt Length')
    plt.title(f'Prompt Length CDF - Iter {iter_num}')
    plt.savefig(os.path.join(args.output_figs_dir, f'prompt_length_cdf_iter_{iter_num}.png'))
    plt.close()
    
    plt.hist(iter_df['response_length'], bins=100, cumulative=True, density=True)
    plt.xlabel('Response Length')
    plt.title(f'Response Length CDF - Iter {iter_num}')
    plt.savefig(os.path.join(args.output_figs_dir, f'response_length_cdf_iter_{iter_num}.png'))
    plt.close()
