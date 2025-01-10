# python profile_analysis_scripts/plot_prefill_decode.py\
#  --input_dir profile_logs\
#  --prefix individual_requests_verifier_\
#  --output_figs_dir profile_analysis_scripts/figs/IterativePipeline/individual_requests\
#  --output_stats_dir profile_analysis_scripts/stats/IterativePipeline/individual_requests\
#  --output_prefix individual_requests
# python profile_analysis_scripts/plot_prefill_decode.py\
#  --input_dir profile_logs\
#  --prefix past_generation_result_iter_\
#  --output_figs_dir profile_analysis_scripts/figs\
#  --output_stats_dir profile_analysis_scripts/stats
# python profile_analysis_scripts/plot_prefill_decode.py\
#  --input_dir profile_logs\
#  --prefix all_requests_generation_result_iter_\
#  --output_figs_dir profile_analysis_scripts/figs/IterativePipeline/all_requests\
#  --output_stats_dir profile_analysis_scripts/stats/IterativePipeline/all_requests
import os
import matplotlib.pyplot as plt
import pandas as pd
import argparse, json

# take arguments from command line
parser = argparse.ArgumentParser(description='Plot prefill decode logs')
# profile_logs dir
parser.add_argument('--input_dir', required=True, help='Input directory containing log files')
# prefix of files to be parsed
# past_generation_result_iter_0.txt
parser.add_argument('--prefix', required=True, help='Prefix of files to be parsed')
# figs directory
parser.add_argument('--output_figs_dir', required=True, help='Output directory to save figures')
# stats directory
parser.add_argument('--output_stats_dir', required=True, help='Output directory to save stats')
# output prefix
parser.add_argument('--output_prefix',  help='Output prefix for files')

args = parser.parse_args()

if args.output_prefix:
    output_prefix = args.output_prefix+'_'
else:
    output_prefix = ''

# make output directories if they don't exist
os.makedirs(args.output_figs_dir, exist_ok=True)
os.makedirs(args.output_stats_dir, exist_ok=True)

# read all log files in the input directory
log_files = os.listdir(args.input_dir)

# filter log files based on prefix
log_files = [f for f in log_files if f.startswith(args.prefix)]

# "metrics": {"arrival_time": 1734371461.7364013, "last_token_time": 1734371461.7364013, "first_scheduled_time": 1734371484.8980389, "first_token_time": 1734371485.2249503, "time_in_queue": 23.161637544631958, "finished_time": 1734371485.4275546, "scheduler_time": 0.0027374383062124252}


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
            metric_data_per_log.append(data['metrics'])
        iter_num = extract_iter_num(log_file)
        metric_data[iter_num] = metric_data_per_log

# calculate prefill time as (first_token_time - first_scheduled_time)
# calculate decode time as (first_token_time - last_token_time)
# calculate request e2e time as (finished_time - arrival_time)
# generate log and plot per iter_num
for iter_num, metrics in metric_data.items():
    iter_data_dict = {'prefill_time (ms)': [], 'decode_time (s)': [], 'request_e2e_time (s)': []}
    for data in metrics:
        prefill_time = (data['first_token_time'] - data['first_scheduled_time']) * 1000 # converts to millisecs (ms)
        decode_time = (data['last_token_time'] - data['first_token_time'])
        request_e2e_time = (data['finished_time'] - data['first_scheduled_time'])
        iter_data_dict['prefill_time (ms)'].append(prefill_time)
        iter_data_dict['decode_time (s)'].append(decode_time)
        iter_data_dict['request_e2e_time (s)'].append(request_e2e_time)
    
    iter_df = pd.DataFrame(iter_data_dict)
    
    # output csv file
    output_csv_file = output_prefix + f'prefill_decode_stats_iter_{iter_num}.csv'

    # save the stats in a csv file per iter_num
    iter_df.describe().to_csv(os.path.join(args.output_stats_dir, output_csv_file))

    # histogram path
    histogram_dir = os.path.join(args.output_figs_dir, 'histograms')

    # make output directories if they don't exist
    os.makedirs(histogram_dir, exist_ok=True)
    
    # plot histogram of prefill time, decode time and request e2e time and save in output directory per iter_num
    plt.hist(iter_df['prefill_time (ms)'], bins=1000)
    plt.xlabel('Prefill Time (ms)')
    plt.ylabel('Frequency')
    plt.title(f'Prefill Time Histogram - Iter {iter_num}')
    plt.savefig(os.path.join(histogram_dir, f'{output_prefix}prefill_time_histogram_iter_{iter_num}.png'))
    plt.close()
    
    plt.hist(iter_df['decode_time (s)'], bins=100)
    plt.xlabel('Decode Time (s)')
    plt.ylabel('Frequency')
    plt.title(f'Decode Time Histogram - Iter {iter_num}')
    plt.savefig(os.path.join(histogram_dir, f'{output_prefix}decode_time_histogram_iter_{iter_num}.png'))
    plt.close()
    
    plt.hist(iter_df['request_e2e_time (s)'], bins=100)
    plt.xlabel('Request E2E Time (s)')
    plt.ylabel('Frequency')
    plt.title(f'Request E2E Time Histogram - Iter {iter_num}')
    plt.savefig(os.path.join(histogram_dir, f'{output_prefix}request_e2e_time_histogram_iter_{iter_num}.png'))
    plt.close()

    cdf_dir = os.path.join(args.output_figs_dir, 'cdf')
    os.makedirs(cdf_dir, exist_ok=True)
    
    # plot cdf of prefill time, decode time and request e2e time and save in output directory per iter_num
    plt.hist(iter_df['prefill_time (ms)'], bins=100, cumulative=True, density=True)
    plt.xlabel('Prefill Time (ms)')
    plt.title(f'Prefill Time CDF - Iter {iter_num}')
    plt.savefig(os.path.join(cdf_dir, f'{output_prefix}prefill_time_cdf_iter_{iter_num}.png'))
    plt.close()
    
    plt.hist(iter_df['decode_time (s)'], bins=100, cumulative=True, density=True)
    plt.xlabel('Decode Time (s)')
    plt.title(f'Decode Time CDF - Iter {iter_num}')
    plt.savefig(os.path.join(cdf_dir, f'{output_prefix}decode_time_cdf_iter_{iter_num}.png'))
    plt.close()
    
    plt.hist(iter_df['request_e2e_time (s)'], bins=100, cumulative=True, density=True)
    plt.xlabel('Request E2E Time (s)')
    plt.title(f'Request E2E Time CDF - Iter {iter_num}')
    plt.savefig(os.path.join(cdf_dir, f'{output_prefix}request_e2e_time_cdf_iter_{iter_num}.png'))
    plt.close()

