# python decode_latency_verifier.py --prompt_file profile_logs/tmp_past_generation_result_iter_0.txt
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

    config = Config("../examples/methods/my_config.yaml",)
    print(config)
    generator: BaseGenerator = get_generator(config)

    
    prompts = ["""<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nCutting Knowledge Date: December 2023\nToday Date: 26 Jul 2024\n\nAnswer the question based on the given document.Only give me the answer and do not output any other words.\nThe following are given documents.\n\nDoc 1(Title: \"John V, Prince of Anhalt-Zerbst\") John V, Prince of Anhalt-Zerbst John V of Anhalt-Zerbst (Dessau, 4 September 1504 \u2013 Zerbst, 4 February 1551), was a German prince of the House of Ascania and ruler of the principality of Anhalt-Dessau. From 1544, he assumed rule of the re-created principality of Anhalt-Zerbst. John was the second (but eldest surviving) son of Ernest I, Prince of Anhalt-Dessau, by his wife Margarete, daughter of Henry I, Duke of M\u00fcnsterberg-Oels, and granddaughter of George of Pod\u011bbrady, King of Bohemia. Upon the death of his father in 1516, John and his brothers George III and Joachim I inherited Anhalt-Dessau as co-rulers\nDoc 2(Title: \"John VI, Prince of Anhalt-Zerbst\") John VI, Prince of Anhalt-Zerbst John VI of Anhalt-Zerbst (Zerbst, 24 March 1621 \u2013 Zerbst, 4 July 1667), was a German prince of the House of Ascania and ruler of the principality of Anhalt-Zerbst. He was the only son of Rudolph, Prince of Anhalt-Zerbst, by his second wife Magdalene, daughter of John VII, Count of Oldenburg. John succeeded his father in Anhalt-Zerbst at only four months of age; during his long minority, his paternal uncle Augustus of Anhalt-Pl\u00f6tzkau acted as regent in the principality. John's education was supervised primarily by his mother. Political instability caused by warfare during the Thirty\nDoc 3(Title: \"John V, Prince of Anhalt-Zerbst\") union with the widowed daughter of the Elector of Brandenburg was a high honor for John, and he decided to celebrate the wedding with great pomp. But by that time, he was in poor health; finally, in 1544, he suffered a stroke. His relations with Margarete worsened during the following years; in 1550 John ordered the temporary arrest of his wife, but she fled. John and Margarete had six children: John V, Prince of Anhalt-Zerbst John V of Anhalt-Zerbst (Dessau, 4 September 1504 \u2013 Zerbst, 4 February 1551), was a German prince of the House of Ascania and ruler of\nDoc 4(Title: \"John II, Prince of Anhalt-Zerbst\") John II, Prince of Anhalt-Zerbst John II, Prince of Anhalt-Zerbst (died 11 April 1382) was a German prince of the House of Ascania and ruler of the principality of Anhalt-Zerbst. He was the youngest son of Albert II, Prince of Anhalt-Zerbst, by his second wife Beatrix, daughter of Rudolf I, Elector of Saxony and Duke of Saxe-Wittemberg. The death of his older brother Albert III in 1359 made John his father's sole heir; his older brother Rudolf was an ordained priest. In 1362 John inherited the principality of Anhalt-Zerbst, but first had to rule jointly with his uncle Waldemar I\nDoc 5(Title: \"John Augustus, Prince of Anhalt-Zerbst\") John Augustus, Prince of Anhalt-Zerbst John Augustus, Prince of Anhalt-Zerbst (29 July 1677 in Zerbst \u2013 7 November 1742 in Zerbst), was a German prince of the House of Ascania and ruler of the principality of Anhalt-Zerbst. He was the eldest son of Karl William, Prince of Anhalt-Zerbst, by his wife Sophie, daughter of August, Duke of Saxe-Weissenfels. In 1718, after the death of Karl William, John Augustus became prince of Anhalt-Zerbst. John Augustus married Fredericka (b. Gotha, 24 March 1675; d. Karlsbad, 28 May 1709), daughter of Frederick I, Duke of Saxe-Gotha-Altenburg, on 25 May 1702 in Zerbst. They<|eot_id|><|start_header_id|>user<|end_header_id|>\n\nQuestion: When did John V, Prince Of Anhalt-Zerbst's father die?<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n""" for _ in range(2)]

    for prompt in tqdm(prompts):

        outputs = generator.generate(prompt)
        print(outputs[0])

if __name__ == '__main__':
    main()