# python scripts/individual_requests_verifier.py --prompt_file profile_logs/tmp_past_generation_result_iter_0.txt
# This is to verify what the cdf of the decode latency looks like if requests are sent one by one
import argparse
import json
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
    parser.add_argument('--prompt_file', type=str, required=True, help='Path to JSON file containing prompts.')
    args = parser.parse_args()
    config = Config("examples/methods/my_config.yaml",)
    print(config)
    generator: BaseGenerator = get_generator(config)

    iter_idx = extract_iter_num(args.prompt_file)
    
    with open(args.prompt_file, 'r', encoding="utf-8") as f:
        prompts = [data['prompt'] for data in json.load(f)]

        stored_output = []

        for prompt in tqdm(prompts):

            outputs = generator.generate(prompt, return_raw_output=True)

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
        open(f"profile_logs/individual_requests_verifier_{iter_idx}.txt", "a").write(json.dumps(stored_output))

if __name__ == '__main__':
    main()