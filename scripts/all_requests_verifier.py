# python scripts/all_requests_verifier.py --prompt_file_dir profile_logs --prompt_file_prefix past_generation_result_iter --config_path examples/methods/my_config.yaml --output_dir profile_logs/IterativePipeline/all_requests/
# This is to verify what the cdf of the prefill and decode latency looks like if requests are sent all at once
import argparse, json, os
from vllm import LLM
from flashrag.config import Config
from flashrag.generator import BaseGenerator
from flashrag.utils import get_generator
from tqdm import tqdm

# Given log file with format *iter_x.txt extract iter_x
def extract_iter_num(log_file):
    return log_file.split('_')[-1].split('.')[0]

def main():
    parser = argparse.ArgumentParser(description='Send prompts to vLLM inference system.')
    parser.add_argument('--prompt_file_prefix', type=str, required=True, help='Prefix for JSON file containing prompts.')
    parser.add_argument('--prompt_file_dir', type=str, required=True, help='Path to directory containing prompts.')
    # config args
    parser.add_argument('--config_path', type=str, required=True, help='Path to config')
    # output args
    parser.add_argument('--output_dir', type=str, default='profile_logs/IterativePipeline/all_requests/', help='Path to output directory.')
    args = parser.parse_args()

    # make output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # config = Config("examples/methods/my_config.yaml",)
    config = Config(args.config_path,)
    print(config)
    generator: BaseGenerator = get_generator(config)

    # list of prompt directory and keep files with prompt_file_prefix
    prompt_files = [os.path.join(args.prompt_file_dir, f) for f in os.listdir(args.prompt_file_dir) if os.path.isfile(os.path.join(args.prompt_file_dir, f)) and f.startswith(args.prompt_file_prefix)]

    # sort prompt_files by iter number
    prompt_files.sort(key=lambda x: extract_iter_num(x))

    for prompt_file in prompt_files:

        iter_idx = extract_iter_num(prompt_file)

        print(f"Processing {prompt_file} with iter_idx {iter_idx}")
        
        with open(prompt_file, 'r', encoding="utf-8") as f:
            prompts = [data['prompt'] for data in json.load(f)]

            stored_output = []

            outputs = generator.generate(prompts, return_raw_output=True)

            for output in outputs:
            
                stored_output.append({
                    'request_id' : output.request_id,
                    'prediction' : output.outputs[0].text,
                    'prompt' : output.prompt,
                    'metrics' : {
                        'arrival_time' : output.metrics.arrival_time,
                        'last_token_time' : output.metrics.last_token_time,
                        'first_scheduled_time' : output.metrics.first_scheduled_time,
                        'first_token_time' : output.metrics.first_token_time,
                        'time_in_queue' : output.metrics.time_in_queue,
                        'finished_time' : output.metrics.finished_time,
                        'scheduler_time' : output.metrics.scheduler_time,
                    }
                })

        # log past_generation_result
        open(os.path.join(args.output_dir,f"generation_result_iter_{iter_idx}.txt"), "w").write(json.dumps(stored_output))

if __name__ == '__main__':
    main()