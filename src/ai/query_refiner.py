import dspy

class RefineQueryEnglish(dspy.Signature):
    """
    You are an excellent English language educator with expertise in international research and web-based learning methodologies.
    For the user's query below, please create one concise query that is likely to provide comprehensive answers from web search and academic resources.
    Focus on research-based teaching methods and international best practices.
    """
    query = dspy.InputField(desc="User's query")
    refined_query = dspy.OutputField(desc="Refined query optimized for web search")

class RefineQueryJapanese(dspy.Signature):
    """
    あなたは日本の英語教育に精通した優秀な英語教育者です。
    以下のユーザークエリに対して、Web検索や学術リソースから包括的な回答を得られる可能性が高い、簡潔なクエリを1つ作成してください。
    中学生・高校生が理解しやすい内容を重視し、学習指導要領との整合性を考慮してください。
    """
    query = dspy.InputField(desc="ユーザーのクエリ")
    refined_query = dspy.OutputField(desc="Web検索に最適化された改善されたクエリ")

class QueryRefiner:
    def __init__(self):
        pass
    
    def refine(self, query: str) -> str:
        """Simple query refinement that returns the query as-is for now."""
        return query 