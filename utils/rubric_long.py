rubric_l = [
    {
        "criterion": "Accuracy of Judgment",
        "description": (
            "Evaluates if the judgment is based on accurate interpretation of the facts and evidence provided. "
            "A high score reflects a decision that aligns closely with reality, while a low score indicates clear contradictions or misjudgments. "
            "This criterion ensures that judgments are factually sound and reliable."
        ),
        "score_1": (
            "Judgment is completely inaccurate, with significant deviations from the evidence or facts provided. "
            "The decision reflects a misunderstanding or disregard for the core information."
        ),
        "score_2": (
            "Judgment is mostly inaccurate, with some elements loosely based on evidence but several major errors. "
            "Although there are minor correct aspects, they are overshadowed by pervasive inaccuracies."
        ),
        "score_3": (
            "Judgment is partially accurate, reflecting a mix of correct and incorrect interpretations of the evidence. "
            "While some parts align with the facts, others reveal a lack of full understanding or misinterpretation."
        ),
        "score_4": (
            "Judgment is mostly accurate, with minor errors or oversights that do not significantly impact reliability. "
            "The core interpretation is sound, but small inaccuracies may require slight adjustments."
        ),
        "score_5": (
            "Judgment is completely accurate, fully reflecting and appropriately interpreting all provided evidence. "
            "The decision demonstrates a clear and thorough understanding of the facts."
        ),
    },
    {
        "criterion": "Logical Soundness",
        "description": (
            "Assesses whether the judgment or decision follows a coherent and logical progression from the evidence or reasoning process. "
            "A well-reasoned decision should clearly demonstrate how conclusions were drawn and avoid logical fallacies or contradictions. "
            "This ensures the reasoning process is transparent and defensible."
        ),
        "score_1": (
            "Decision-making process is illogical, lacking clear reasoning or consistency. "
            "The conclusion appears arbitrary or disconnected from the supporting evidence."
        ),
        "score_2": (
            "Decision-making process shows significant gaps or logical flaws, making it difficult to follow. "
            "Reasoning is inconsistent, and critical errors undermine the validity of the conclusion."
        ),
        "score_3": (
            "Decision-making process is moderately logical, but some inconsistencies or gaps weaken its coherence. "
            "While the reasoning is partially sound, certain steps may appear unclear or unsupported."
        ),
        "score_4": (
            "Decision-making process is mostly logical, with minor issues that do not undermine its overall integrity. "
            "The reasoning is generally clear and follows a structured progression with only slight missteps."
        ),
        "score_5": (
            "Decision-making process is entirely logical, with clear and consistent reasoning throughout. "
            "Every step in the reasoning process is well-supported and leads naturally to the conclusion."
        ),
    },
    {
        "criterion": "Completeness of Evaluation",
        "description": (
            "Measures whether all relevant factors and perspectives were considered in forming the judgment or decision. "
            "A comprehensive evaluation accounts for key elements and avoids overlooking important details or implications. "
            "This ensures the judgment is well-rounded and thorough."
        ),
        "score_1": (
            "Evaluation is highly incomplete, ignoring most critical factors or perspectives. "
            "Key elements that are essential for a sound decision are missing entirely."
        ),
        "score_2": (
            "Evaluation is partially incomplete, missing several key elements or considerations. "
            "Although some aspects are addressed, others that are equally important are overlooked."
        ),
        "score_3": (
            "Evaluation is moderately complete, addressing most factors but with noticeable gaps. "
            "While the main points are covered, some relevant details or perspectives are insufficiently explored."
        ),
        "score_4": (
            "Evaluation is mostly complete, with only minor omissions that do not significantly impact the decision. "
            "Almost all relevant factors are included, providing a well-rounded evaluation overall."
        ),
        "score_5": (
            "Evaluation is fully comprehensive, considering all relevant factors and perspectives. "
            "Every important aspect is thoroughly examined, leaving no gaps in the analysis."
        ),
    },
    {
        "criterion": "Fairness",
        "description": (
            "Assesses if the judgment or decision is balanced and free from bias, prejudice, or favoritism. "
            "A fair decision considers all sides and treats stakeholders equitably, without leaning unfairly toward any particular group. "
            "This ensures impartiality and ethical soundness."
        ),
        "score_1": (
            "Decision is highly biased, showing clear prejudice or favoritism toward a particular outcome or group. "
            "The bias undermines the integrity and credibility of the judgment."
        ),
        "score_2": (
            "Decision is somewhat biased, with moderate evidence of partiality or unfair treatment. "
            "Certain perspectives are given undue weight, leading to an unbalanced decision."
        ),
        "score_3": (
            "Decision is mostly fair, with minor instances of bias that do not heavily influence the outcome. "
            "While the decision is generally impartial, slight preferences are evident."
        ),
        "score_4": (
            "Decision is fair and balanced, with very minimal signs of bias or unfairness. "
            "Stakeholders and perspectives are treated equitably, ensuring a mostly unbiased outcome."
        ),
        "score_5": (
            "Decision is completely fair and unbiased, treating all perspectives and groups equitably. "
            "The judgment demonstrates full impartiality and adherence to ethical standards."
        ),
    },
    {
        "criterion": "Relevance to Context",
        "description": (
            "Evaluates if the judgment or decision is appropriate and specific to the given context or problem. "
            "A relevant decision directly addresses the issue at hand without unnecessary or tangential considerations. "
            "This ensures that the response aligns with the unique requirements of the situation."
        ),
        "score_1": (
            "Completely irrelevant, failing to address the problem or align with the context in any meaningful way. "
            "The judgment shows no consideration of the situational factors or intended goals."
        ),
        "score_2": (
            "Partially relevant, but with significant deviations from the core context or problem. "
            "While there may be some alignment, key aspects of the situation are overlooked or misunderstood."
        ),
        "score_3": (
            "Mostly relevant, addressing the primary elements of the context but with minor misalignments. "
            "The judgment is generally appropriate but lacks full integration with situational details."
        ),
        "score_4": (
            "Highly relevant, aligning closely with the context and addressing most aspects effectively. "
            "Any deviations from the context are minimal and do not significantly detract from the decision’s appropriateness."
        ),
        "score_5": (
            "Perfectly relevant, demonstrating a thorough understanding of the problem and full alignment with the context. "
            "The decision is highly appropriate, addressing all situational factors seamlessly."
        ),
    },
    {
        "criterion": "Clarity of Explanation",
        "description": (
            "Measures whether the reasoning behind the judgment or decision is articulated in a clear and understandable manner. "
            "A clear explanation provides sufficient detail to justify the decision, ensuring that others can follow the reasoning process. "
            "This helps build confidence in the decision’s validity."
        ),
       "score_1": (
            "No explanation provided, or the explanation is so unclear it is incomprehensible. "
            "The reasoning behind the judgment is completely absent or inaccessible."
        ),
        "score_2": (
            "Limited explanation, with several points that are unclear or poorly articulated. "
            "While some reasoning is present, it is insufficient to provide a full understanding."
        ),
        "score_3": (
            "Moderately clear explanation, covering the main reasoning but lacking detail or leaving some ambiguities. "
            "The rationale is partially understandable but not fully transparent or detailed."
        ),
        "score_4": (
            "Mostly clear explanation, with only minor ambiguities or areas requiring further elaboration. "
            "The reasoning is well-articulated and easy to follow for the most part."
        ),
        "score_5": (
            "Highly clear explanation, providing detailed and easily understandable reasoning for the decision. "
            "The judgment is fully transparent, leaving no ambiguity in its rationale."
        ),
    },
    {
        "criterion": "Impactfulness",
        "description": (
            "Evaluates the extent to which the judgment or decision has a meaningful and constructive effect on the issue or problem. "
            "An impactful decision provides value, addresses the core concerns, and contributes positively to the situation. "
            "This ensures the decision creates tangible benefits or improvements."
        ),
        "score_1": (
            "Very weak or negative impact, with no constructive value or even detrimental effects on the issue. "
            "The judgment fails to address the problem meaningfully or worsens the situation."
        ),
        "score_2": (
            "Limited impact, with minimal relevance or benefit to the issue at hand. "
            "While some aspects may be addressed, the overall contribution to resolving the problem is minor."
        ),
        "score_3": (
            "Moderate impact, providing partial value in addressing the issue meaningfully. "
            "The decision contributes to progress but lacks sufficient strength or depth to fully address the problem."
        ),
        "score_4": (
            "Strong impact, significantly advancing the resolution of the issue and providing meaningful benefits. "
            "The decision effectively addresses key aspects of the problem."
        ),
        "score_5": (
            "Highly impactful, fully resolving or advancing the issue in a transformative and meaningful way. "
            "The decision provides comprehensive and constructive solutions to the problem."
        ),
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
    "Accuracy of Judgment": 0.25,  # Ensures decisions are based on correct interpretation of evidence, a critical aspect of quality.
    "Logical Soundness": 0.20,    # Verifies that decisions follow a coherent and logical reasoning process.
    "Completeness of Evaluation": 0.15,  # Encourages consideration of all relevant factors and perspectives.
    "Fairness": 0.10,            # Supports impartial and unbiased judgments to uphold ethical standards.
    "Relevance to Context": 0.15, # Emphasizes the importance of tailoring decisions to the specific situation or problem.
    "Clarity of Explanation": 0.10, # Ensures decisions are communicated clearly to enhance understanding and transparency.
    "Impactfulness": 0.05         # Measures the decision's constructive value and practical outcomes.
}

