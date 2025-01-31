from typing import List, Dict, Any
import argparse
import asyncio
import json
import os
import random

from tqdm.asyncio import tqdm_asyncio

import utils.file_operations as file_operations
import utils.judges as judges
import utils.meta_judge as meta_judge
import utils.metrics as metrics



######
#meta_judges
######
async def judge_judges(pairs: List[Dict[str, Any]], concurrency_limit: int = 1, output_file: str = None):
    semaphore = asyncio.Semaphore(concurrency_limit)
    meta_judge_agent = meta_judge.meta_judge_agent("claude-3-5-sonnet-20241022")#("claude-3-5-sonnet-20241022, gpt-4o-mini-2024-07-18, meta-llama/Meta-Llama-3.1-405B-Instruct", gpt-4o)
    file_lock = asyncio.Lock()
    
    async def judge_judge(pair: Dict[str, Any]):
        async with semaphore:
            #print("pair is:", pair["judgments"][0].keys())
            question = pair["question"]
            response_A = pair["response_A"]
            response_B = pair["response_B"]
            judgement = pair["judgments"][0]["judgment"]["response"] #+ pair["judgments"][0]["judgment"][1]["response"]
            decision = pair["judgments"][0]["decision"]
            source = pair["source"]

            try:
                meta_judgment_1 = await meta_judge_agent.get_meta_judgment(question, response_A, response_B, judgement, decision)
                #meta_judgment_1 = await meta_judge_agent.get_meta_judgment_R_adjust(pair)
            except Exception as e:
                print(f"Failed to meta_judge pair {pair['pair_id']} due to the following error: {e}.")
                meta_judgment_1 = None
            meta_judgments = [meta_judgment_1]
            
            pair["meta_judgments"] = meta_judgments
            return pair

    async def judge_judge_by_discuss(pair: Dict[str, Any]):
        async with semaphore:
            #print("pair is:", pair["judgments"][0].keys())
            try:
                #meta_judgment_1 = await meta_judge_agent.get_meta_judgment_discuss_start(pair)
                meta_judgment_1 = await meta_judge_agent.get_meta_judgment_discuss(pair)
            except Exception as e:
                print(f"Failed to meta_judge pair {pair['pair_id']} due to the following error: {e}.")
                meta_judgment_1 = None
            meta_judgments = [meta_judgment_1]
            
            pair["meta_judgments_4"] = meta_judgments
            return pair

    #tasks = [asyncio.create_task(judge_judge(pair)) for pair in pairs]
    tasks = [asyncio.create_task(judge_judge_by_discuss(pair)) for pair in pairs]
    
    for future in tqdm_asyncio.as_completed(tasks):
        pair = await future
        if output_file is not None:
            async with file_lock:
                with open(output_file, 'a') as f:
                    f.write(json.dumps(pair, ensure_ascii=False) + '\n')

    return pairs
######
######

def main(args: argparse.Namespace) -> None:
    
    random.seed(args.seed)
    
    pairs = file_operations.read_jsonl(args.pairs)    

    dataset_name = os.path.basename(args.pairs).replace(".jsonl", "")
    file_path = f"{dataset_name},judge_name={args.judge_name},judge_model={args.judge_model.replace('/', '_')}.jsonl"
    os.makedirs("./outputs", exist_ok=True)
    file_path_judge = os.path.join("./outputs/judgments", file_path)
    file_path_meta_judge = os.path.join("./outputs/meta-judges/split-task/livecodebench/start-claude", file_path)
    
    assert os.path.exists(file_path_judge), "ERROR!!!!Please choose the judgement that has been generated in output file!!!"
    #pairs = file_operations.read_jsonl(file_path_judge)
    #pairs = file_operations.read_jsonl("./split_task/response_model=gpt-4o,judge_model=gpt-4o-mini/livecodebench.json")
    pairs = file_operations.read_jsonl("./outputs/meta-judges/split-task/livecodebench/start-claude/dataset=judgebench,response_model=gpt-4o-2024-05-13,judge_name=arena_hard,judge_model=gpt-4o-mini,expert,4o-mini,round3.jsonl")
    #!!!add meta-judge to filt out bad judgement, then improve judgement score!!!!##
    meta_judge_choice = {args.meta_judge_choice}
    if meta_judge_choice: 
        print("Meta Judging the judges ...")
        pairs = asyncio.run(
            judge_judges(
                pairs,
                concurrency_limit=args.concurrency_limit,
                output_file=file_path_meta_judge,
            )
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--judge_name', type=str, required=True) # name of judge, should correspond to an entry in utils/judges/get_judge_from_judge_name_and_model.
    parser.add_argument('--judge_model', type=str, required=True) # model to be used by judge.
    parser.add_argument('--single_game', action="store_true") # by default, we run each pair through twice (A,B) and (B,A). This flag will only run the original ordering, and should be used if a judge is order-independent.
    parser.add_argument('--seed', type=int, default=42) # seed to use.
    parser.add_argument('--concurrency_limit', type=int, default=1) # We use asyncio to speed things up, 10 is usally a good value here.
    parser.add_argument('--pairs', type=str, required=True) # path to jsonl containing pairs for judging
    parser.add_argument('--meta_judge_choice', type=bool, default=True)
    args = parser.parse_args()
    main(args)
