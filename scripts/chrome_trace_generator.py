# python scripts/chrome_trace_generator.py --input_file profile_logs/all_requests_generation_result_iter_0.txt  --output_file traces_chrome/all_requests_0.trace.json
import json, argparse

# add argparser to get the input file and output file
argparser = argparse.ArgumentParser(description='Convert JSON data to Chrome Trace format')
argparser.add_argument('--input_file', type=str, required=True, help='Input JSON file')
argparser.add_argument('--output_file', type=str, required=True, help='Output Chrome Trace file')
args = argparser.parse_args()


timing_data = []
# Read the input JSON file
with open(args.input_file, 'r') as f:
    data = json.load(f)
    for item in data:
        timing_data.append(item['metrics'])

# Function to generate trace events
def create_chrome_trace(events):
    trace = {
        "traceEvents": [],
        "displayTimeUnit": "ms"  # Time unit for Chrome trace
    }

    # Create events for the trace
    for request_id, event in enumerate(events):
        arrival_time = event["arrival_time"]
        first_scheduled_time = event["first_scheduled_time"]
        first_token_time = event["first_token_time"]
        last_token_time = event["last_token_time"]
        finished_time = event["finished_time"]

        decode_time = (last_token_time - first_token_time)
        prefill_time = first_token_time - first_scheduled_time

        event['prefill_time'] = prefill_time
        event['decode_time'] = decode_time

        request_id = request_id + 2

        trace["traceEvents"].append({
            "name": "R_{}".format(request_id),
            "cat": "event_category",
            "ph": "X",  # X for complete span
            "ts": arrival_time * 1000000,
            "dur": (finished_time - arrival_time) * 1000000,  # Duration in ms
            "pid": 1,
            "tid": 1,
        })

        # Creating span for prefill time
        trace["traceEvents"].append({
            "name": "P_{}".format(request_id),
            "cat": "event_category",
            "ph": "X",  # X for complete span
            "ts": first_scheduled_time * 1000000,
            "dur": prefill_time * 1000000,  # Duration in ms
            "pid": 1,
            "tid": request_id,
            "args": {
                "event": "prefill_time"
            },
        })

        # Creating span for decode time
        trace["traceEvents"].append({
            "name": "D_{}".format(request_id),
            "cat": "event_category",
            "ph": "X",  # X for complete span
            "ts": first_token_time * 1000000,
            "dur": decode_time * 1000000,  # Duration in ms
            "pid": 1,
            "tid": request_id,
            "args": {
                "event": "decode_time"
            }
        })

        if request_id == 512:
            break   

    return trace

# Function to save the trace as a JSON file
def save_trace_to_file(trace, filename):
    with open(filename, "w") as f:
        json.dump(trace, f, indent=4)

# Convert the sample data to Chrome Trace format
chrome_trace = create_chrome_trace(timing_data)

# Save the trace to a file
save_trace_to_file(chrome_trace, args.output_file)

print("Chrome trace file created successfully!")
