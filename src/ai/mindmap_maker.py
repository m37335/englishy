import dspy
import litellm


class MindMap(dspy.Signature):
    """You are a trusted and reliable designer known for creating clear and understandable mind maps from given text.
    Based on a report obtained for a query, please create a mind map following the Markdown example below.
    The mind map should comprehensively cover the main content and items of the report, with concise and clear expressions.
    
    **Important**: Include related grammar topics and learning points in appropriate sections of the mind map.
    
    Structure the mind map to include:
    1. Main topics from the report
    2. Related grammar topics integrated naturally
    3. Learning objectives and key concepts
    4. Practice activities and exercises
    5. Common mistakes and solutions
    6. Additional resources and references
    
    Example structure:
        # Main Topic
        ## Key Concepts
        ### Grammar Points
        #### Specific Grammar Rules
        ##### Examples and Usage
        ## Learning Activities
        ### Practice Exercises
        ## Common Mistakes
        ### Solutions and Tips
        ## Additional Resources
        ### References and Citations
    """  # noqa: E501

    report = dspy.InputField(desc="The provided report", format=str)
    related_topics = dspy.InputField(desc="Related grammar topics", format=str)
    mindmap = dspy.OutputField(desc="Mind map created based on the report and related topics", format=str)


class MindMapMaker(dspy.Module):
    def __init__(self, lm) -> None:
        self.lm = lm
        self.make_mindmap = dspy.Predict(MindMap)

    def forward(self, report: str, related_topics: str = "") -> dspy.Prediction:
        with dspy.settings.context(lm=self.lm):
            mindmap_result = self.make_mindmap(report=report, related_topics=related_topics)
        return mindmap_result 