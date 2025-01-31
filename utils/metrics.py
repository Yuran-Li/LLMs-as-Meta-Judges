from typing import List, Dict, Any
from utils.rubric_short import weights
import re
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any
# compute final metrics
# basically just compute how accuracy the judge is

def flip_judgment(decision: str) -> str:
    if decision == "A>B":
        decision = "B>A"
    elif decision == "B>A":
        decision = "A>B"
    return decision


def compute_final_metrics(pairs: List[Dict[str, Any]], reverse_order: bool, include_fn=lambda x: x) -> None:
    
    pairs = [pair for pair in pairs if include_fn(pair)]

    n_pairs = len(pairs)

    if not reverse_order:
        n_correct = sum(
            pair["judgments"][0]["decision"] == pair["label"]
            for pair in pairs
        )
        n_incorrect = n_pairs - n_correct
        return 100*n_correct/n_pairs
    else:
        
        n_all_correct = 0
        n_all_incorrect = 0
        n_some_correct = 0
        
        n_correct = 0
        n_incorrect = 0
        n_tie = 0
        
        n_nulls = 0
        n_inconsistent = 0
        
        for pair in pairs:
            
            label = pair["label"]
            judgment1, judgment2 = pair["judgments"]
        
            decision1 = judgment1["decision"] if judgment1 is not None else None
            decision2 = flip_judgment(judgment2["decision"] if judgment2 is not None else None)
            
            if decision1 is None or decision2 is None:
                n_nulls += 1
            
            # consistency metrics
            if decision1 == label and decision2 == label:
                n_all_correct += 1
            elif decision1 != label and decision2 != label:
                n_all_incorrect += 1
            else:
                n_some_correct += 1
                
            if decision1 != decision2:
                n_inconsistent += 1
                
            # new metrics
            counter = 0
            for decision in [decision1, decision2]:
                if decision == label:
                    counter += 1
                elif decision == flip_judgment(label):
                    counter -= 1
                
            if counter > 0:
                n_correct += 1
            elif counter < 0:
                n_incorrect += 1
            else:
                n_tie += 1
        
        return 100*n_correct/n_pairs
        
##############################################################
def compute_meta_judge_select(pairs: List[Dict[str, Any]], threshold: int, include_fn=lambda x: x) -> None:
    
    pairs = [pair for pair in pairs if include_fn(pair)]
    n_pairs = len([pair for pair in pairs if pair["final_score"]>threshold])
    reverse_order = False
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    if not reverse_order:
        TP = sum(
        pair["judgments"][0]["decision"] == pair["label"] and pair["final_score"] > threshold
        for pair in pairs)
        TN = sum(
            pair["judgments"][0]["decision"] != pair["label"] and pair["final_score"] <= threshold
            for pair in pairs)
        FP = sum(
            pair["judgments"][0]["decision"] != pair["label"] and pair["final_score"] > threshold
            for pair in pairs)
        FN = sum(
            pair["judgments"][0]["decision"] == pair["label"] and pair["final_score"] <= threshold
            for pair in pairs)
    else:
        n_all_correct = 0
        n_all_incorrect = 0
        n_some_correct = 0
        
        n_correct = 0
        n_incorrect = 0
        n_tie = 0
        
        n_nulls = 0
        n_inconsistent = 0
        
        for pair in pairs:
            
            label = pair["label"]
            judgment1, judgment2 = pair["judgments"]
        
            decision1 = judgment1["decision"] if judgment1 is not None else None
            decision2 = flip_judgment(judgment2["decision"] if judgment2 is not None else None)
            
            if decision1 is None or decision2 is None:
                n_nulls += 1
            
            # consistency metrics
            if decision1 == label and decision2 == label:
                n_all_correct += 1
            elif decision1 != label and decision2 != label:
                n_all_incorrect += 1
            else:
                n_some_correct += 1
                
            if decision1 != decision2:
                n_inconsistent += 1
                
            # new metrics
            counter = 0
            for decision in [decision1, decision2]:
                if decision == label:
                    counter += 1
                elif decision == flip_judgment(label):
                    counter -= 1
                
            if counter > 0:
                if pair["final_score"] > threshold:
                    TP += 1
                else:
                    FN += 1
                n_correct += 1
            elif counter < 0:
                if pair["final_score"] <= threshold:
                    TN += 1
                else:
                    FP += 1
                n_incorrect += 1
            else:
                if pair["final_score"] <= threshold:
                    TN += 1
                else:
                    FP += 1
                n_tie += 1
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    accuracy = (TP + TN) / (TP + FP + FN + TN)
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {"precision": precision*100,
            "accuracy":accuracy*100,
            "recall": recall*100,
            "F1 score": f1*100}

def compute_meta_judge_binary_select(pairs: List[Dict[str, Any]], threshold: int, include_fn=lambda x: x) -> None:
    
    pairs = [pair for pair in pairs if include_fn(pair)]
    
    TP = sum(
        pair["judgments"][0]["decision"] == pair["label"] and 
        ("result: correct" in pair["meta_judgments"][0]["meta_judge_result"] or "result: [correct]" in pair["meta_judgments"][0]["meta_judge_result"] )
        for pair in pairs)
    TN = sum(
        pair["judgments"][0]["decision"] != pair["label"] and 
        ("result: correct" not in pair["meta_judgments"][0]["meta_judge_result"] and "result: [correct]" not in pair["meta_judgments"][0]["meta_judge_result"])
        for pair in pairs)
    FP = sum(
        pair["judgments"][0]["decision"] != pair["label"] and 
        ("result: correct" in pair["meta_judgments"][0]["meta_judge_result"] or "result: [correct]" in pair["meta_judgments"][0]["meta_judge_result"]) 
        for pair in pairs)
    FN = sum(
        pair["judgments"][0]["decision"] == pair["label"] and 
        ("result: correct" not in pair["meta_judgments"][0]["meta_judge_result"] and "result: [correct]" not in pair["meta_judgments"][0]["meta_judge_result"])
        for pair in pairs)
    
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    accuracy = (TP + TN) / (TP + FP + FN + TN)
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {"precision": precision*100,
            "accuracy":accuracy*100,
            "recall": recall*100,
            "F1 score": f1*100}

def plot_metrics_vs_threshold(pairs: List[Dict[str, Any]], source: str, include_fn=lambda x: x) -> None:
    
    pairs = [pair for pair in pairs if include_fn(pair)]
    thresholds = np.linspace(0, 5, 50)
    precisions, recalls, accuracies, f1_scores = [], [], [], []
    for threshold in thresholds:
        pairs = [pair for pair in pairs if include_fn(pair)]
        n_pairs = len([pair for pair in pairs if pair["final_score"]>threshold])
        reverse_order = False
        TP = 0
        TN = 0
        FP = 0
        FN = 0
        if not reverse_order:
            TP = sum(
            pair["judgments"][0]["decision"] == pair["label"] and pair["final_score"] > threshold
            for pair in pairs)
            TN = sum(
                pair["judgments"][0]["decision"] != pair["label"] and pair["final_score"] <= threshold
                for pair in pairs)
            FP = sum(
                pair["judgments"][0]["decision"] != pair["label"] and pair["final_score"] > threshold
                for pair in pairs)
            FN = sum(
                pair["judgments"][0]["decision"] == pair["label"] and pair["final_score"] <= threshold
                for pair in pairs)
        else:
            n_all_correct = 0
            n_all_incorrect = 0
            n_some_correct = 0
            
            n_correct = 0
            n_incorrect = 0
            n_tie = 0
            
            n_nulls = 0
            n_inconsistent = 0
            
            for pair in pairs:
                
                label = pair["label"]
                judgment1, judgment2 = pair["judgments"]
            
                decision1 = judgment1["decision"] if judgment1 is not None else None
                decision2 = flip_judgment(judgment2["decision"] if judgment2 is not None else None)
                
                if decision1 is None or decision2 is None:
                    n_nulls += 1
                
                # consistency metrics
                if decision1 == label and decision2 == label:
                    n_all_correct += 1
                elif decision1 != label and decision2 != label:
                    n_all_incorrect += 1
                else:
                    n_some_correct += 1
                    
                if decision1 != decision2:
                    n_inconsistent += 1
                    
                # new metrics
                counter = 0
                for decision in [decision1, decision2]:
                    if decision == label:
                        counter += 1
                    elif decision == flip_judgment(label):
                        counter -= 1
                    
                if counter > 0:
                    if pair["final_score"] > threshold:
                        TP += 1
                    else:
                        FN += 1
                    n_correct += 1
                elif counter < 0:
                    if pair["final_score"] <= threshold:
                        TN += 1
                    else:
                        FP += 1
                    n_incorrect += 1
                else:
                    if pair["final_score"] <= threshold:
                        TN += 1
                    else:
                        FP += 1
                    n_tie += 1
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        accuracy = (TP + TN) / (TP + FP + FN + TN)
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        precisions.append(precision)
        recalls.append(recall)
        accuracies.append(accuracy)
        f1_scores.append(f1)

    plt.plot(thresholds, precisions, label="Precision")
    plt.plot(thresholds, recalls, label="Recall")
    plt.plot(thresholds, accuracies, label="Accuracy")
    plt.plot(thresholds, f1_scores, label="F1 Score")

    plt.xlabel("Threshold")
    plt.ylabel("Metric Value")
    plt.title("Metrics vs. Threshold" + " " + source)
    plt.legend()
    plt.grid()
    judge_type = "panda"
    save_path = f"/Users/yuranli/Documents/PhD-1st/course/project/experiment-result/{judge_type}-{source}.png"
    plt.savefig(save_path, format="png", dpi=300)
    print(f"Plot saved to {save_path}")
    plt.show()
    plt.close()

def get_weighted_meta_score(output_A: str, output_B: str, output_C: str, W_A: int, W_B: int, W_C: int) -> None:
        score_sum = {}
        weighted_sum = {}
        # W_A = 0.5
        # W_B = 0.5
        # W_C = 0
        matches_A = re.findall(r"Criterion: (.+?)\s+Score: (\d+)", output_A)
        scores_A = {criterion: int(score) for criterion, score in matches_A}
        matches_B = re.findall(r"Criterion: (.+?)\s+Score: (\d+)", output_B)
        scores_B = {criterion: int(score) for criterion, score in matches_B}
        matches_C = re.findall(r"Criterion: (.+?)\s+Score: (\d+)", output_C)
        scores_C = {criterion: int(score) for criterion, score in matches_C}
        for key in scores_A:
            score_sum[key] = W_A*scores_A[key]+W_B*scores_B[key]+W_C*scores_C[key]
            weighted_sum[key] = weighted_sum.get(key, 0) + score_sum[key]*weights[key]
        return weighted_sum

def get_meta_score_baseline(output_A: str) -> None:
        match = re.search(r"Score: (\d+)", output_A)
        # Extract the integer score
        score_A = int(match.group(1)) if match else None
        return score_A

def majority_voting(meta_score_1: int, meta_score_2: int, threshold: int) -> None:
    if meta_score_1 > threshold and meta_score_2 > threshold:
        return 5
    else:
        return 1

def majority_voting_for3(meta_score_1: int, meta_score_2: int, meta_score_3: int, threshold: int) -> None:
    count = 0
    if meta_score_1 > threshold:
        count += 1
    if meta_score_2 > threshold:
        count += 1
    if meta_score_3 > threshold:
        count += 1
    if count>=2:
        return 5
    else:
        return 1