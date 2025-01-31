from typing import List, Dict, Any
import argparse
import asyncio
import json
import os
import random

import utils.file_operations as file_operations
import utils.metrics as metrics

def main(args: argparse.Namespace) -> None:

    ######## score based selection #########
    random.seed(args.seed)
    # compute final metrics
    print("Computing final metrics ...") 
    pairs = file_operations.read_jsonl(args.judge_pairs)
    pairs_A = file_operations.read_jsonl(args.meta_judge_scoreA)    
    pairs_B = file_operations.read_jsonl(args.meta_judge_scoreB)
    pairs_C = file_operations.read_jsonl(args.meta_judge_scoreC)
    ####compute meta-judge score
    pairs_A_dict = {item["pair_id"]: item for item in pairs_A}
    pairs_B_dict = {item["pair_id"]: item for item in pairs_B}
    pairs_C_dict = {item["pair_id"]: item for item in pairs_C}
    
    for pair in pairs:
        pair_id = pair["pair_id"]
        pair_A = pairs_A_dict.get(pair_id)
        pair_B = pairs_B_dict.get(pair_id)
        pair_C = pairs_C_dict.get(pair_id)
        '''
        if pair_A and pair_B and pair_C:
            pair["weighted_meta_judge_score"] = metrics.get_weighted_meta_score(
            pair_A["meta_judgments"][0]["meta_score"], 
            pair_B["meta_judgments"][0]["meta_score"], 
            pair_C["meta_judgments"][0]["meta_score"],
            1,0,0
            )
            
            pair["final_score"] = sum(
                pair["weighted_meta_judge_score"][key] 
                for key in pair["weighted_meta_judge_score"].keys()
            )
            
        else:
            print(f"warning: missing data for pair_id {pair_id}")
        '''
        # ########## baseline ##########
        # pair["final_score"] = metrics.get_meta_score_baseline(
        #     pair_A["meta_judgments"][0]["meta_score"])
        # ##########
        '''
        pair_A["final_score"] = metrics.get_meta_score_baseline(
             pair_A["meta_judgments"][0]["meta_score"])
        pair_B["final_score"] = metrics.get_meta_score_baseline(
             pair_B["meta_judgments"][0]["meta_score"])
        pair["final_score"] = 0.5*pair_A["final_score"] + 0.5*pair_B["final_score"]
        '''
        ########majority voting#########
        # pair_A["weighted_meta_judge_score"] = metrics.get_weighted_meta_score(
        #     pair_A["meta_judgments"][0]["meta_score"], 
        #     pair_B["meta_judgments"][0]["meta_score"], 
        #     pair_C["meta_judgments"][0]["meta_score"],
        #     1,0,0
        #     )
        # weighted_meta_judge_score_1 = sum(
        #         pair_A["weighted_meta_judge_score"][key] 
        #         for key in pair_A["weighted_meta_judge_score"].keys()
        #     )
        # pair_B["weighted_meta_judge_score"] = metrics.get_weighted_meta_score(
        #     pair_A["meta_judgments_1"][0]["meta_score"], 
        #     pair_B["meta_judgments"][0]["meta_score"], 
        #     pair_C["meta_judgments"][0]["meta_score"],
        #     1,0,0
        #     )
        # weighted_meta_judge_score_2 = sum(
        #         pair_B["weighted_meta_judge_score"][key] 
        #         for key in pair_B["weighted_meta_judge_score"].keys()
        #     )
        # pair["final_score"] = metrics.majority_voting(weighted_meta_judge_score_1, weighted_meta_judge_score_2, threshold = args.threshold)
        #################

        ##########majority voting###############
        weighted_meta_judge_score_1 = metrics.get_meta_score_baseline(
             pair_A["meta_judgments"][0]["meta_score"])
        weighted_meta_judge_score_2 = metrics.get_meta_score_baseline(
             pair_A["meta_judgments_1"][0]["meta_score"])
        weighted_meta_judge_score_3 = metrics.get_meta_score_baseline(
             pair_A["meta_judgments_2"][0]["meta_score"]) 
        '''
        pair_A["weighted_meta_judge_score"] = metrics.get_weighted_meta_score(
            pair_A["meta_judgments_2"][0]["meta_score"], 
            pair_A["meta_judgments"][0]["meta_score"], 
            pair_C["meta_judgments"][0]["meta_score"],
            1,0,0
            )
        weighted_meta_judge_score_1 = sum(
                pair_A["weighted_meta_judge_score"][key] 
                for key in pair_A["weighted_meta_judge_score"].keys()
            )
        pair_B["weighted_meta_judge_score"] = metrics.get_weighted_meta_score(
            pair_A["meta_judgments_3"][0]["meta_score"], 
            pair_A["meta_judgments"][0]["meta_score"], 
            pair_C["meta_judgments"][0]["meta_score"],
            1,0,0
            )
        weighted_meta_judge_score_2 = sum(
                pair_B["weighted_meta_judge_score"][key] 
                for key in pair_B["weighted_meta_judge_score"].keys())
        
        pair_C["weighted_meta_judge_score"] = metrics.get_weighted_meta_score(
            pair_A["meta_judgments_4"][0]["meta_score"], 
            pair_A["meta_judgments"][0]["meta_score"], 
            pair_C["meta_judgments"][0]["meta_score"],
            1,0,0
            )
            
        weighted_meta_judge_score_3 = sum(
                pair_B["weighted_meta_judge_score"][key] 
                for key in pair_B["weighted_meta_judge_score"].keys())
        '''
        pair["final_score"] = metrics.majority_voting_for3(weighted_meta_judge_score_1, weighted_meta_judge_score_2, weighted_meta_judge_score_3, threshold = args.threshold)
        #pair["final_score"] = metrics.majority_voting(weighted_meta_judge_score_3, weighted_meta_judge_score_2, threshold = args.threshold)
        
        #########################################

    ####meta-judge selection
    for source in ["livecodebench"]:
        print("the judgements are selected by meta-judge.")
         ####selection result evaluation
        score = metrics.compute_meta_judge_select(pairs, threshold = args.threshold, include_fn = lambda x: x["source"].startswith(source))
        print(f"""{source if source else 'Overall'}: 
                Precision: {score['precision']:.2f}%.
                Accuracy: {score['accuracy']:.2f}%.
                Recall: {score['recall']:.2f}%.
                F1 Score: {score['F1 score']:.2f}%.\n
            """)
        metrics.plot_metrics_vs_threshold(pairs,source,include_fn = lambda x: x["source"].startswith(source))
    
    '''
    ########### binary label based selection #########
    random.seed(args.seed)
    # compute final metrics
    print("Computing final metrics ...") 
    pairs = file_operations.read_jsonl(args.judge_pairs)
    pairs_A = file_operations.read_jsonl(args.meta_judge_scoreA)    
    pairs_B = file_operations.read_jsonl(args.meta_judge_scoreB)
    pairs_C = file_operations.read_jsonl(args.meta_judge_scoreC)
    ############

    ####meta-judge selection
    for source in ["mmlu-pro", "livebench-reasoning", "livebench-math", "livecodebench", ""]:
        print("the judgements are selected by meta-judge.")
         ####selection result evaluation
        score = metrics.compute_meta_judge_binary_select(pairs_A, threshold = args.threshold, include_fn = lambda x: x["source"].startswith(source))
        print(f"""{source if source else 'Overall'}: 
                Precision: {score['precision']:.2f}%.
                Accuracy: {score['accuracy']:.2f}%.
                Recall: {score['recall']:.2f}%.
                F1 Score: {score['F1 score']:.2f}%.\n
            """)
    '''

    # random.seed(args.seed)
    # # compute final metrics
    # print("Computing final metrics ...") 
    # pairs = file_operations.read_jsonl(args.judge_pairs)
    # pairs_A = file_operations.read_jsonl(args.meta_judge_scoreA)    
    # pairs_B = file_operations.read_jsonl(args.meta_judge_scoreB)
    # pairs_C = file_operations.read_jsonl(args.meta_judge_scoreC)
    # ####compute meta-judge score
    # pairs_A_dict = {item["pair_id"]: item for item in pairs_A}
    # pairs_B_dict = {item["pair_id"]: item for item in pairs_B}
    # pairs_C_dict = {item["pair_id"]: item for item in pairs_C}

    # for pair in pairs:
    #     pair_id = pair["pair_id"]
    #     pair_A = pairs_A_dict.get(pair_id)
    #     pair_B = pairs_B_dict.get(pair_id)
    #     pair_C = pairs_C_dict.get(pair_id)
    #     if pair["source"] in ["livebench-reasoning", "livebench-math"]:
    #         if pair_A and pair_B and pair_C:
    #             pair["weighted_meta_judge_score"] = metrics.get_weighted_meta_score(
    #             pair_A["meta_judgments_1"][0]["meta_score"], 
    #             pair_B["meta_judgments"][0]["meta_score"], 
    #             pair_C["meta_judgments"][0]["meta_score"]
    #             )
    #             pair["final_score"] = sum(
    #                 pair["weighted_meta_judge_score"][key] 
    #                 for key in pair["weighted_meta_judge_score"].keys()
    #             )
    #         else:
    #             print(f"warning: missing data for pair_id {pair_id}")
    #     elif any(sub in pair["source"] for sub in ["mmlu-pro", "livecodebench"]):   
    #         ########## baseline ##########
    #         pair["final_score"] = metrics.get_meta_score_baseline(
    #             pair_A["meta_judgments_1"][0]["meta_score"])
    #         ###########
        
    # ####meta-judge selection
    # for source in ["mmlu-pro", "livebench-reasoning", "livebench-math", "livecodebench", ""]:
    #     print("the judgements are selected by meta-judge.")
    #      ####selection result evaluation
    #     score = metrics.compute_meta_judge_select(pairs, threshold = args.threshold, include_fn = lambda x: x["source"].startswith(source))
    #     print(f"""{source if source else 'Overall'}: 
    #             Precision: {score['precision']:.2f}%.
    #             Accuracy: {score['accuracy']:.2f}%.
    #             Recall: {score['recall']:.2f}%.
    #             F1 Score: {score['F1 score']:.2f}%.\n
    #         """)
    #     metrics.plot_metrics_vs_threshold(pairs,source,include_fn = lambda x: x["source"].startswith(source))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--judge_pairs', type=str, required=True) # path to jsonl containing pairs' judgment result
    parser.add_argument('--meta_judge_scoreA', type=str, required=True) # path to jsonl containing meta-judge result
    parser.add_argument('--meta_judge_scoreB', type=str, required=True) # 
    parser.add_argument('--meta_judge_scoreC', type=str, required=True) # 
    parser.add_argument('--threshold', type=int, default=4.5) # selection threshold
    parser.add_argument('--seed', type=int, default=42) # seed to use.
    args = parser.parse_args()
    main(args)
