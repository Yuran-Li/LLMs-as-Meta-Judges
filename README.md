# LLMs-as-Meta-Judges

This repo is developed on the basis of repo: (https://github.com/ScalerLab/JudgeBench)

### Installation
Set up a new environment and run `pip install -r requirements.txt`. This repository has been built and tested with Python 3.10.12.

### Run Meta-Judge on JudgeBench
run:
```
export OPENAI_API_KEY=your-openai-api-key         # (GPT-4o, GPT-4o-mini, o1-preview, o1-mini, etc.)
export ANTHROPIC_API_KEY=your-anthropic-api-key   # (Claude-3.5-Sonnet, Claude-3-Haiku, etc.)
export TOGETHER_API_KEY=your-together-api-key     # (Llama-3.1-405B-Instruct, etc.)
```
Then run `run_meta_judge.py`. For example:
```
python run_meta_judge.py --judge_name arena_hard --judge_model gpt-4o-mini --pairs data/dataset=judgebench,response_model=gpt-4o-2024-05-13.jsonl
```
This will print out an meta_judge report, and save an output file under `outputs/metajudges` containing the meta-judgments for each pair. 

### Run Meta-Judge-selection on Judgment result
run:
```
python run_meta_judge_selection.py --judge_pairs $path to jsonl containing judgment result --meta_judge_scoreA $path to jsonl containing meta-judgment result from model_A --meta_judge_scoreB $path to jsonl containing meta-judgment result from model_B --meta_judge_scoreC $path to jsonl containing meta-judgment result from model_C [--threshold $selection threshold]
```
