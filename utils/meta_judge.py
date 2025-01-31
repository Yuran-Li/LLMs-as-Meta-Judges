from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple, Union
import re

import utils.prompts as prompts
import utils.models as models
from utils.rubric_short import rubric_s
from utils.rubric_long import rubric_l
from utils.rubric_binary import rubric_b
# run meta-judge on judgements

class meta_judge_agent:
    def __init__(self, model_A: str) -> None:
        self.api_A = models.get_chat_api_from_model(model_A)
    async def get_meta_judgment(self, question: str, answer_A: str, answer_B: str, judgement: str, decision: str) -> Dict[str, Any]:
        
        ######### prompt for our single agent method ##########
        prompt = prompts.render_template(
            "meta_judge_prompt", question=question, answer_a=answer_A, answer_b=answer_B, judgement_1 = judgement, decision_1 = decision)
        prompt += f"Combine judgment and decision to finally assign a score for each criterion based on the following rubrics:"
        for criterion in rubric_l:
            prompt += f"Criterion: {criterion['criterion']}\nDescription:: {criterion['description']}\n"
            for i in range(1, 6):
                prompt += f"{i}: {criterion[f'score_{i}']}\n"
            prompt += "Please respond strictly in the following format, without any additional text, explanation, or commentary: \n Criterion: [criterion_name]\n Score: [1-5]\n\n"
        ########
        output_A = await self.api_A.chat(
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    top_p=1.0,
                    max_tokens=1024,
                )
        score = output_A.strip()
        return {
            "meta_score": score
        }
        
        # #######prompt for baseline
        # prompt = prompts.render_template(
        #     "meta_judge_prompt", question=question, answer_a=answer_A, answer_b=answer_B, judgement_1 = judgement, decision_1 = decision)
        # prompt += f"""Explain which judgment is more accurate according to the original rubric and why.
        #             Combine judgment and decision to finally assign a score, consider factors such as adherence, accuracy, and consistency to the judgment instruction."""
        # prompt += "Please respond strictly in the following format, without any additional text, explanation, or commentary: \n Score: [1-5]\n\n"
        # #prompt += "Please respond strictly in the following format: \n Score: [1-5] \n Explanation: \n\n"
        # #######
        
        output_A = await self.api_A.chat(
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    top_p=1.0,
                    max_tokens=1024,
                )
        score = output_A.strip()
        return {
            "meta_score": score
        }
        
        '''
        #######prompt for binary rubric
        prompt = prompts.render_template(
            "meta_judge_binary_prompt", question=question, answer_a=answer_A, answer_b=answer_B, judgement_1 = judgement, decision_1 = decision)
        prompt += f"Finally, determine the correctness of the judgment and decision based on the following rubrics:"
        for criterion in rubric_b:
            prompt += f"Criterion: {criterion['criterion']}\nDescription:: {criterion['description']}\n"
        prompt += "Please respond strictly in the following format, without any additional text, explanation, or commentary: \n result: [correct/wrong]\n\n"

        output_A = await self.api_A.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            top_p=1.0,
            max_tokens=1024,
        )
        result = output_A.strip()
        return {
            "meta_judge_result": result
        }
        ##########
        '''
    
    async def get_meta_judgment_R_adjust(self, pair: Dict[str, Any]) -> Dict[str, Any]:
        if pair["source"] in ["livebench-reasoning"]:
            ######### prompt for our single agent method ##########
            prompt = prompts.render_template(
                "meta_judge_prompt", question=pair["question"], answer_a=pair["response_A"], answer_b=pair["response_B"], judgement_1 = pair["judgments"][0]["judgment"]["response"], decision_1 = pair["judgments"][0]["decision"])
            prompt += f"Combine judgment and decision to finally assign a score for each criterion based on the following rubrics:"
            for criterion in rubric_l:
                prompt += f"Criterion: {criterion['criterion']}\nDescription:: {criterion['description']}\n"
                for i in range(1, 6):
                    prompt += f"{i}: {criterion[f'score_{i}']}\n"
                prompt += "Please respond strictly in the following format, without any additional text, explanation, or commentary: \n Criterion: [criterion_name]\n Score: [1-5]\n\n"
            ########
        elif pair["source"] in ["livebench-math"]:
            #######prompt for binary rubric
            prompt = prompts.render_template(
                "meta_judge_binary_prompt", question=pair["question"], answer_a=pair["response_A"], answer_b=pair["response_B"], judgement_1 = pair["judgments"][0]["judgment"]["response"], decision_1 = pair["judgments"][0]["decision"])
            prompt += f"Finally, determine the correctness of the judgment and decision based on the following rubrics:"
            for criterion in rubric_b:
                prompt += f"Criterion: {criterion['criterion']}\nDescription:: {criterion['description']}\n"
            prompt += "Please respond strictly in the following format, without any additional text, explanation, or commentary: \n result: [correct/wrong]\n\n"
            ##########
        elif any(sub in pair["source"] for sub in ["mmlu-pro"]) or pair["source"] in ["livecodebench"]:
            #######prompt for baseline
            prompt = prompts.render_template(
                "meta_judge_prompt", question=pair["question"], answer_a=pair["response_A"], answer_b=pair["response_B"], judgement_1 = pair["judgments"][0]["judgment"]["response"], decision_1 = pair["judgments"][0]["decision"])
            prompt += f"""Explain which judgment is more accurate according to the original rubric and why.
                        Combine judgment and decision to finally assign a score, consider factors such as adherence, accuracy, and consistency to the judgment instruction."""
            prompt += "Please respond strictly in the following format, without any additional text, explanation, or commentary: \n Score: [1-5]\n\n"
            #######

        output_A = await self.api_A.chat(
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    top_p=1.0,
                    max_tokens=1024,
                )
        score = output_A.strip()
        return {
            "meta_score": score
        }
        
    async def get_meta_judgment_discuss_start(self, pair: Dict[str, Any]) -> Dict[str, Any]:
        question = pair["question"]
        answer_A = pair["response_A"]
        answer_B = pair["response_B"]
        judgement = pair["judgments"][0]["judgment"]["response"] #+ pair["judgments"][0]["judgment"][1]["response"]
        decision = pair["judgments"][0]["decision"]
        ####### prompt for our multi-agent method ###########
        prompt = prompts.render_template(
            "meta_judge_prompt", question=question, answer_a=answer_A, answer_b=answer_B, judgement_1 = judgement, decision_1 = decision)
        if pair["source"] in ["livebench-reasoning"]:
            ######### prompt for long rubric ##########
            prompt += f"Combine judgment and decision to finally assign a score for each criterion based on the following rubrics:"
            for criterion in rubric_l:
                prompt += f"Criterion: {criterion['criterion']}\nDescription:: {criterion['description']}\n"
                for i in range(1, 6):
                    prompt += f"{i}: {criterion[f'score_{i}']}\n"
                prompt += "Please respond strictly in the following format: \n Criterion: [criterion_name]\n Score: [1-5] \n Explanation: \n\n"
                #prompt += "Please respond strictly in the following format: \n Criterion: [criterion_name]\n Score: [1-5] \n\n"
            ########
        elif pair["source"] in ["livebench-math"]:
            #######prompt for short rubric
            prompt += f"Combine judgment and decision to finally assign a score for each criterion based on the following rubrics:"
            for criterion in rubric_s:
                prompt += f"Criterion: {criterion['criterion']}\nDescription:: {criterion['description']}\n"
                for i in range(1, 6):
                    prompt += f"{i}: {criterion[f'score_{i}']}\n"
                prompt += "Please respond strictly in the following format: \n Criterion: [criterion_name]\n Score: [1-5] \n Explanation: \n\n"
                #prompt += "Please respond strictly in the following format: \n Criterion: [criterion_name]\n Score: [1-5] \n\n"
            ##########
        elif any(sub in pair["source"] for sub in ["mmlu-pro"]) or pair["source"] in ["livecodebench"]:
            #######prompt for baseline
            prompt += f"""Explain which judgment is more accurate according to the original rubric and why.
                        Combine judgment and decision to finally assign a score, consider factors such as adherence, accuracy, and consistency to the judgment instruction."""
            prompt += "Please respond strictly in the following format, without any additional text, explanation, or commentary: \n Score: [1-5] \n\n"
            #######
        ########
        output_A = await self.api_A.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            top_p=1.0,
            max_tokens=1024,
        )
        score = output_A.strip()
        return {
            "meta_score": score
        }

    async def get_meta_judgment_discuss(self, pair: Dict[str, Any]) -> Dict[str, Any]:
        question = pair["question"]
        answer_A = pair["response_A"]
        answer_B = pair["response_B"]
        judgement = pair["judgments"][0]["judgment"]["response"] #+ pair["judgments"][0]["judgment"][1]["response"]
        decision = pair["judgments"][0]["decision"]
        meta_judge_history = pair["meta_judgments_3"][0]["meta_score"]
        ####### prompt for our multi-agent method ###########
        prompt = prompts.render_template(
            "meta_judge_discuss_prompt", question=question, answer_a=answer_A, answer_b=answer_B, judgement_1 = judgement, decision_1 = decision, meta_judge_history_1 = meta_judge_history)
        if pair["source"] in ["livebench-reasoning"]:
            ######### prompt for long rubric ##########
            prompt += f"Combine judgment and decision to finally assign a score for each criterion based on the following rubrics:"
            for criterion in rubric_l:
                prompt += f"Criterion: {criterion['criterion']}\nDescription:: {criterion['description']}\n"
                for i in range(1, 6):
                    prompt += f"{i}: {criterion[f'score_{i}']}\n"
                prompt += "Please respond strictly in the following format: \n Criterion: [criterion_name]\n Score: [1-5] \n Explanation: \n\n"
                #prompt += "Please respond strictly in the following format: \n Criterion: [criterion_name]\n Score: [1-5] \n\n"
            ########
        elif pair["source"] in ["livebench-math"]:
            #######prompt for short rubric
            prompt += f"Combine judgment and decision to finally assign a score for each criterion based on the following rubrics:"
            for criterion in rubric_s:
                prompt += f"Criterion: {criterion['criterion']}\nDescription:: {criterion['description']}\n"
                for i in range(1, 6):
                    prompt += f"{i}: {criterion[f'score_{i}']}\n"
                prompt += "Please respond strictly in the following format: \n Criterion: [criterion_name]\n Score: [1-5] \n\n"
                #prompt += "Please respond strictly in the following format: \n Criterion: [criterion_name]\n Score: [1-5] \n Explanation: \n\n"
            ##########
        elif any(sub in pair["source"] for sub in ["mmlu-pro"]) or pair["source"] in ["livecodebench"]:
            #######prompt for baseline
            prompt += f"""Explain which judgment is more accurate according to the original rubric and why.
                        Combine judgment and decision to finally assign a score, consider factors such as adherence, accuracy, and consistency to the judgment instruction."""
            #prompt += "Please respond strictly in the following format: \n Score: [1-5] \n Explanation: \n\n"
            prompt += "Please respond strictly in the following format, without any additional text, explanation, or commentary: \n Score: [1-5] \n\n"
            #######
        ########
        output_A = await self.api_A.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            top_p=1.0,
            max_tokens=1024,
        )
        score = output_A.strip()
        return {
            "meta_score": score
        }
    
    async def get_meta_judgment_sum(self, pair: Dict[str, Any]) -> Dict[str, Any]:
        question = pair["question"]
        answer_A = pair["response_A"]
        answer_B = pair["response_B"]
        judgement = pair["judgments"][0]["judgment"]["response"] #+ pair["judgments"][0]["judgment"][1]["response"]
        decision = pair["judgments"][0]["decision"]
        meta_judge_history_0 = pair["meta_judgments"][0]["meta_score"]
        meta_judge_history = pair["meta_judgments_1"][0]["meta_score"]
        ####### prompt for our multi-agent method ###########
        prompt = prompts.render_template(
            "meta_judge_summary_prompt", question=question, answer_a=answer_A, answer_b=answer_B, judgement_1 = judgement, decision_1 = decision, meta_judge_history_1 = meta_judge_history_0, meta_judge_history_2 = meta_judge_history)
        if pair["source"] in ["livebench-reasoning"]:
            ######### prompt for long rubric ##########
            prompt += f"Combine judgment and decision to finally assign a score for each criterion based on the following rubrics:"
            for criterion in rubric_l:
                prompt += f"Criterion: {criterion['criterion']}\nDescription:: {criterion['description']}\n"
                for i in range(1, 6):
                    prompt += f"{i}: {criterion[f'score_{i}']}\n"
                prompt += "Please respond strictly in the following format: \n Criterion: [criterion_name]\n Score: [1-5] \n Explanation: \n\n"
                #prompt += "Please respond strictly in the following format: \n Criterion: [criterion_name]\n Score: [1-5] \n\n"
            ########
        elif pair["source"] in ["livebench-math"]:
            #######prompt for short rubric
            prompt += f"Combine judgment and decision to finally assign a score for each criterion based on the following rubrics:"
            for criterion in rubric_s:
                prompt += f"Criterion: {criterion['criterion']}\nDescription:: {criterion['description']}\n"
                for i in range(1, 6):
                    prompt += f"{i}: {criterion[f'score_{i}']}\n"
                prompt += "Please respond strictly in the following format: \n Criterion: [criterion_name]\n Score: [1-5] \n Explanation: \n\n"
            ##########
        elif any(sub in pair["source"] for sub in ["mmlu-pro"]) or pair["source"] in ["livecodebench"]:
            #######prompt for baseline
            prompt += f"""Explain which judgment is more accurate according to the original rubric and why.
                        Combine judgment and decision to finally assign a score, consider factors such as adherence, accuracy, and consistency to the judgment instruction."""
            #prompt += "Please respond strictly in the following format: \n Score: [1-5] \n Explanation: \n\n"
            prompt += "Please respond strictly in the following format, without any additional text, explanation, or commentary: \n Score: [1-5] \n\n"
            #######
        ########
        output_A = await self.api_A.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            top_p=1.0,
            max_tokens=1024,
        )
        score = output_A.strip()
        return {
            "meta_score": score
        }
    