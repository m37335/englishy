import dspy
import litellm


class GenerateDetailedTopicsEnglish(dspy.Signature):
    """You are an expert in English learning and language education with deep knowledge of international research and methodologies.
    Regarding the query below, preliminary web searches have been conducted for basic research.
    Based on the web search results, you are trying to search for English learning materials needed to create comprehensive explanatory and interpretive documents about the query.
    English learning content search can be done through semantic search, so searches with keywords and short phrases are possible.

    Please list up search topics in the following format to appropriately hit all the English learning materials needed for explanation and interpretation.

    Output format:
    - xxx
    - yyy
    - ...
    - zzz

    When listing search topics, please comply with the following conditions.

    - Fully understand the meaning of the query and its educational implications
    - List search topics so that all necessary English learning materials for explaining and interpreting the query are covered
    - Prioritize international research, latest methodologies, and advanced educational terminology
    - Include specific educational terms and related content that are expected to be used in English learning
    - Search topics should be as non-overlapping as possible and individually researchable. They should be **self-contained**
    - Search topics should be specific and conform to the English learning corpus (short phrases or specific educational terms)
    - Focus on international perspectives, research findings, and advanced teaching methodologies
    - No need to number search topics. Only describe the content of search topics
    - Limit search topics to a maximum of 8. More is not necessarily better
    """  # noqa: E501

    query = dspy.InputField(desc="Query", format=str)
    web_search_results = dspy.InputField(desc="Web search results", format=str)
    topics = dspy.OutputField(desc="Listed search topics", format=str)


class GenerateDetailedTopicsJapanese(dspy.Signature):
    """あなたは日本の英語教育に精通した専門家で、中学生・高校生の学習をサポートする英語教育の専門家です。
下記のクエリー（高校入試や教科書からの英文を含む可能性があります）に関して、事前にWeb検索をして簡単に下調べしてあります。
Web検索結果もふまえ、クエリーに関する英語教育的な解説・分析文書を作成するために必要な情報を検索しようとしています。

解説・分析に必要な情報を適切にヒットさせきるための検索トピックを以下の形式でリストアップしてください。

出力フォーマット：
- xxx
- yyy
- ...
- zzz

検索トピックをリストアップするにあたり、以下の条件を遵守してください。

- クエリーの背景にある英語教育的な論点を深く考察すること
- クエリーに対する解説・分析を行うのに必要な情報（英文の文法構造、語彙の難易度、構文の複雑性、読解のポイント、指導上の留意点、関連する学習指導要領（英語）、第二言語習得論、応用言語学、英語教授法、教材研究、国内外の事例、および入力された英文に含まれる具体的な文法項目（例: 現在完了進行形、関係代名詞、仮定法など）に関する解説）が揃うように検索トピックをリストアップしてください
- 検索トピックは可能な限り互いに重複せず、個別に調査可能な形にしてください。 **self-contained** であるべきです
- 検索トピックは英語教育分野の文脈に準拠した具体的なものにしてください（短文または具体的な専門用語）
- 検索精度を高めるため、第二言語習得論、応用言語学、英語教授法などの専門用語や、関連するキーワードを含めてください
- 中学生・高校生が理解しやすい内容を重視し、実践的な学習内容を含めてください
- 検索トピックをナンバリングする必要はありません。
- 検索トピックの個数は多くても8個までにしてください。
- 出力は必要な英文以外は日本語にすることを厳守すること
    """  # noqa: E501

    query = dspy.InputField(desc="Query", format=str)
    web_search_results = dspy.InputField(desc="Web search results", format=str)
    topics = dspy.OutputField(desc="Listed search topics", format=str)


def cleanse_topic(topic: str) -> str:
    if topic.startswith("- "):
        topic = topic[2:].strip()
    if topic.startswith('"') and topic.endswith('"'):
        topic = topic[1:-1].strip()
    topic = topic.strip()
    return topic


def merge_topics(english_topics: list, japanese_topics: list) -> list:
    """英語と日本語の検索トピックを統合し、重複を除去して最適化する"""
    all_topics = english_topics + japanese_topics
    
    # 重複除去（大文字小文字を無視）
    unique_topics = []
    seen = set()
    
    for topic in all_topics:
        topic_lower = topic.lower().strip()
        if topic_lower not in seen:
            unique_topics.append(topic)
            seen.add(topic_lower)
    
    # 重要度に基づいてソート（英語の専門的トピックを優先）
    priority_topics = []
    secondary_topics = []
    
    for topic in unique_topics:
        # 英語の専門的トピックを優先
        if any(keyword in topic.lower() for keyword in ['research', 'methodology', 'international', 'advanced', 'theory']):
            priority_topics.append(topic)
        else:
            secondary_topics.append(topic)
    
    # 最大12個まで返す（優先トピックを先に）
    result = priority_topics + secondary_topics
    return result[:12]


class QueryExpander(dspy.Module):
    def __init__(self, lm):
        self.generate_detailed_topics_english = dspy.Predict(GenerateDetailedTopicsEnglish)
        self.generate_detailed_topics_japanese = dspy.Predict(GenerateDetailedTopicsJapanese)
        self.lm = lm

    def forward(self, query: str, web_search_results: str) -> dspy.Prediction:
        with dspy.settings.context(lm=self.lm):
            # 段階的検索：まず日本語で基本的な情報を収集
            japanese_result = self.generate_detailed_topics_japanese(
                query=query, web_search_results=web_search_results
            )
            japanese_topics = [cleanse_topic(topic) for topic in japanese_result.topics.split("\n")]
            japanese_topics = [topic for topic in japanese_topics if topic]
            
            # 次に英語で詳細・専門的な情報を補完
            english_result = self.generate_detailed_topics_english(
                query=query, web_search_results=web_search_results
            )
            english_topics = [cleanse_topic(topic) for topic in english_result.topics.split("\n")]
            english_topics = [topic for topic in english_topics if topic]
            
            # 結果を統合
            merged_topics = merge_topics(english_topics, japanese_topics)
            
        return dspy.Prediction(topics=merged_topics) 