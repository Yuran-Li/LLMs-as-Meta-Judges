rubric_s = [
    {
        "criterion": "Accuracy of Judgment",
        "description": "Evaluates if the judgment aligns with the evidence and facts provided.",
        "score_1": "Highly inaccurate, with judgments that contradict evidence or facts.",
        "score_2": "Mostly inaccurate, with some alignment to evidence but significant errors.",
        "score_3": "Partially accurate, with a mix of correct and incorrect judgments.",
        "score_4": "Mostly accurate, with only minor misinterpretations.",
        "score_5": "Completely accurate, with judgments fully supported by evidence and facts.",
    },
    {
        "criterion": "Logical Soundness",
        "description": "Measures if the decision-making process follows a clear and logical reasoning path.",
        "score_1": "Illogical, with no clear reasoning or consistency.",
        "score_2": "Mostly illogical, with several gaps or flawed reasoning.",
        "score_3": "Partially logical, with some inconsistencies in the reasoning process.",
        "score_4": "Mostly logical, with minor flaws in reasoning.",
        "score_5": "Highly logical, with a clear and consistent reasoning process throughout.",
    },
    {
        "criterion": "Completeness of Evaluation",
        "description": "Assesses if all relevant factors were considered in the judgment or decision.",
        "score_1": "Very incomplete, overlooking most critical factors.",
        "score_2": "Partially incomplete, with several key factors ignored.",
        "score_3": "Moderately complete, considering most factors but missing some details.",
        "score_4": "Mostly complete, with only minor omissions.",
        "score_5": "Fully complete, considering all relevant factors comprehensively.",
    },
    {
        "criterion": "Fairness",
        "description": "Evaluates if the judgment or decision is unbiased and balanced.",
        "score_1": "Highly biased, showing clear favoritism or prejudice.",
        "score_2": "Somewhat biased, with moderate signs of unfairness.",
        "score_3": "Mostly fair, with minor instances of bias.",
        "score_4": "Fair and balanced, with very minor issues.",
        "score_5": "Completely fair and unbiased, free from any prejudice.",
    },
    {
        "criterion": "Relevance to Context",
        "description": "Assesses if the judgment or decision is appropriate to the specific context or problem.",
        "score_1": "Completely irrelevant, not addressing the problem or context.",
        "score_2": "Partially relevant, with significant deviations from the context.",
        "score_3": "Mostly relevant, with some minor misalignments.",
        "score_4": "Highly relevant, with only slight contextual deviations.",
        "score_5": "Perfectly relevant, fully aligned with the context and problem.",
    },
    {
        "criterion": "Clarity of Explanation",
        "description": "Measures if the reasoning behind the judgment or decision is clearly explained.",
        "score_1": "No explanation provided, or explanation is incomprehensible.",
        "score_2": "Limited explanation, with several unclear points.",
        "score_3": "Moderately clear, but some areas lack detail or clarity.",
        "score_4": "Mostly clear, with only minor ambiguities.",
        "score_5": "Highly clear, with detailed and understandable explanations.",
    },
    {
        "criterion": "Impactfulness",
        "description": "Evaluates if the judgment or decision is meaningful and has a constructive impact on the issue.",
        "score_1": "Very weak or negative impact, with little to no constructive value.",
        "score_2": "Limited impact, with minimal relevance to the issue.",
        "score_3": "Moderate impact, addressing the issue in a partially meaningful way.",
        "score_4": "Strong impact, significantly addressing the issue.",
        "score_5": "Highly impactful, fully resolving or advancing the issue meaningfully.",
    }
]

# weights = {
#     "Accuracy of Judgment": 0.2,  # Ensures decisions are based on correct interpretation of evidence, a critical aspect of quality.
#     "Logical Soundness": 0.2,    # Verifies that decisions follow a coherent and logical reasoning process.
#     "Completeness of Evaluation": 0.2,  # Encourages consideration of all relevant factors and perspectives.
#     "Fairness": 0,            # Supports impartial and unbiased judgments to uphold ethical standards.
#     "Relevance to Context": 0.2, # Emphasizes the importance of tailoring decisions to the specific situation or problem.
#     "Clarity of Explanation": 0.2, # Ensures decisions are communicated clearly to enhance understanding and transparency.
#     "Impactfulness": 0         # Measures the decision's constructive value and practical outcomes.
# }

weights = {
    "Accuracy of Judgment": 0.2,  # Reflects the correctness of the judgment, a core aspect of decision quality.
    "Logical Soundness": 0.2,    # Ensures the reasoning process of the decision is logical and consistent.
    "Completeness of Evaluation": 0.15,  # Measures whether all relevant factors have been fully considered.
    "Fairness": 0.1,            # Ensures the decision is unbiased and equitable.
    "Relevance to Context": 0.15, # Assesses whether the decision aligns with the specific problem or context.
    "Clarity of Explanation": 0.1, # Evaluates the clarity of reasoning behind the decision to ensure it is understandable.
    "Impactfulness": 0.1        # Assesses the practical significance and constructive value of the decision.
}

