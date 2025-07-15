from typing import AsyncGenerator

import dspy

from ai.utils.stream_writer import StreamLineWriter
from .grammar_dictionary import get_grammar_dictionary
from .grammar_analyzer import get_grammar_analyzer


class WriteLeadEnglish(dspy.Signature):
    """You are a trusted and reliable writer known for creating clear explanations in English learning and language education with expertise in international research and methodologies.
    You have conducted research on the query below and created a report. Please generate a concise lead paragraph to be displayed immediately after the report title.
    A lead paragraph is a concise summary that serves as an abstract for the entire report, including the overall argument development and main topics.

    When generating the lead paragraph, strictly follow these rules:
    - The lead paragraph should present a comprehensive overview of the overall context and main topics covered in the report, making it readable on its own
    - Focus on international research findings, latest methodologies, and advanced educational approaches
    - The lead paragraph should be approximately 140-280 characters
    - Generate only the lead paragraph text in English
    - Emphasize research-based insights and international best practices
    """  # noqa: E501

    query = dspy.InputField(desc="Query", format=str)
    title = dspy.InputField(desc="Report title", format=str)
    draft = dspy.InputField(desc="Report content", format=str)
    lead = dspy.OutputField(desc="Lead paragraph text", format=str)


class WriteLeadJapanese(dspy.Signature):
    """あなたは日本の英語教育に精通し、分かりやすい解説記事を書くことに定評のある信頼できるライターです。
下記のクエリー（高校入試や教科書からの英文を含む可能性があります）に関する調査レポートの、タイトルの直後に表示する簡潔なリード文を生成してください。
リード文は、レポート全体の要旨、特に英語教育的な観点からの主要な論点や分析の方向性を含めた、140〜280文字程度の簡潔な文章にしてください。
中学生・高校生が理解しやすい内容を重視し、実践的な学習内容を含めてください。
出力は必要な英文以外は日本語にすることを厳守すること。

**文法用語の日本語統一**：
- gerund → 動名詞
- infinitive → 不定詞
- subjunctive → 仮定法
- participle → 分詞
- modal verb → 助動詞
- relative pronoun → 関係代名詞
- passive voice → 受動態
- active voice → 能動態
- present perfect → 現在完了形
- past perfect → 過去完了形
- future perfect → 未来完了形
- conditional → 条件法
- imperative → 命令法
- interrogative → 疑問文

クエリー: {query}
"""

    query = dspy.InputField(desc="Query", format=str)
    title = dspy.InputField(desc="Report title", format=str)
    draft = dspy.InputField(desc="Report content", format=str)
    lead = dspy.OutputField(desc="Lead paragraph text", format=str)


class WriteSectionEnglish(dspy.Signature):
    """You are a trusted and persistent writer known for proper English language interpretation and creating clear explanations with expertise in international research and methodologies.
    You have conducted research on the query below and created a report outline based on the query.
    Please refer to all citation numbers in the outline without omission, and write the content of each section while appropriately interpreting the collected information sources. Be sure to write at least 400 characters for each subsection.
    The explanation should be detailed and comprehensive with high information content, based on information sources. Focus on international research findings, latest methodologies, and advanced educational approaches. Include overviews of relevant English learning concepts, related educational materials, appropriate examples, historical background, and latest teaching methods as needed.
    Since content reliability is important, be sure to check information sources and remember to cite as instructed below.
    1. Do not change the titles "# Title", "## Title", "### Title" in the outline.
    2. Be sure to write based on information source information and be careful of hallucinations.
       Cite the information sources that form the basis of the description as "...[4][1][27]." "...[21][9]." in order of relevance.
    3. The more correctly citations are indicated, the higher your explanation will be evaluated.
       Creative writing without citations is not evaluated at all unless the reasoning is clear.
    4. There is no need to include information sources at the end of the explanation.
    5. Write the explanation in English.
    6. Use only citation numbers unless there is a logical need to quote the text.
    7. Do not cite numbers that are not in "Collected information sources and citation numbers". That becomes creative writing and loses value.
    """

    query = dspy.InputField(desc="Query", format=str)
    references = dspy.InputField(desc="Collected information sources and citation numbers", format=str)
    section_outline = dspy.InputField(desc="Section outline", format=str)
    section = dspy.OutputField(desc="Generated section", format=str)


class WriteSectionJapanese(dspy.Signature):
    """あなたは日本の英語教育に精通し、客観的なデータと英語教育理論に基づいた分かりやすい解説を書くことに定評のある信頼できるライターです。
下記のクエリー（高校入試や教科書からの英文を含む可能性があります）に関するレポートのアウトラインに基づき、各章の本文を執筆してください。
アウトラインの中にある引用番号は漏れることなく必ず参照し、収集された情報源の内容を適切に解釈しながら、各節ごとに400字以上で解説を記載してください。
解説は緻密かつ包括的で、情報源に基づいたものであることが望ましいです。特に、入力された英文がある場合は、その英文の具体的な分析（文法、語彙、構文、読解ポイントなど）を詳細に含めてください。中学生・高校生が理解しやすい内容を重視し、実践的な学習内容を含めてください。必要に応じて、関連する英語教育理論、歴史的背景、国内外の事例、最新の統計データなどを盛り込んでください。
なお、内容の信頼性が重要なので、必ず情報源にあたり、下記指示にあるように引用をするのを忘れないで下さい。

**文法用語の日本語統一**：
- gerund → 動名詞
- infinitive → 不定詞
- subjunctive → 仮定法
- participle → 分詞
- modal verb → 助動詞
- relative pronoun → 関係代名詞
- passive voice → 受動態
- active voice → 能動態
- present perfect → 現在完了形
- past perfect → 過去完了形
- future perfect → 未来完了形
- conditional → 条件法
- imperative → 命令法
- interrogative → 疑問文

1. アウトラインの"# Title"、"## Title"、"### Title"のタイトルは変更しないでください。
2. 必ず情報源の情報に基づき記載し、ハルシネーションに気をつけること。
   記載の根拠となる参照すべき情報源は "...です[4][1][27]。" "...ます[21][9]。" のように明示してください。
3. 正しく引用が明示されているほどあなたの解説は高く評価されます。
4. 内容に応じて箇条書きを適切に配置し、読者の理解度を深めてください。
5. 日本語の「ですます調」で解説を書いてください。
6. 出力は必要な英文以外は日本語にすることを厳守すること。
7. 文法用語は必ず日本語で統一してください。
    """

    query = dspy.InputField(desc="Query", format=str)
    references = dspy.InputField(desc="Collected information sources and citation numbers", format=str)
    section_outline = dspy.InputField(desc="Section outline", format=str)
    section = dspy.OutputField(desc="Generated section", format=str)


class WriteRelatedTopics(dspy.Signature):
    """あなたは英文法に精通した専門家です。
下記の英文を分析し、含まれる主要な文法項目を特定してください。
特定した各文法項目について、以下の形式で簡潔に解説してください。

出力フォーマット：
- **[文法項目名]**: [その文法項目の簡潔な説明]。例: [提供された英文からの該当箇所]

例:
- **現在完了進行形**: 過去のある時点から現在まで継続している動作を表します。例: "We have been discussing it since last week."
- **関係代名詞**: 名詞を修飾する節を導きます。例: "It's a song about friendship." (ここでは関係代名詞が省略されているが、概念として関連する)

検索トピックをリストアップするにあたり、以下の条件を遵守してください。
- 英文に含まれる主要な文法項目を網羅的に特定すること。
- 各文法項目の説明は、中学生・高校生が理解できるレベルで簡潔に記述すること。
- 提供された英文中の具体的な箇所を例として引用し、解説と関連付けること。
- 文法項目は、一般的な文法分類に従うこと。
- 箇条書き形式で出力すること。
- 出力は必要な英文以外は日本語にすることを厳守すること。
    """

    query = dspy.InputField(desc="Query", format=str)
    related_topics = dspy.OutputField(desc="Related grammar topics", format=str)


class WriteReferences(dspy.Signature):
    """あなたは英語教育の専門家で、参考文献の整理に精通しています。
レポートで使用された情報源を基に、信頼性を最重視した厳選された参考文献リストを生成してください。

出力フォーマット：
## 参考文献

### 学術文献・研究論文
1. [著者名] (出版年). [タイトル]. [出版社/雑誌名]. DOI: [DOI番号]
2. [著者名] (出版年). [タイトル]. [出版社/雑誌名]. DOI: [DOI番号]

### 公式ガイドライン・政策文書
1. [文部科学省] (年度). [タイトル]. [URL]
2. [教育委員会] (年度). [タイトル]. [URL]

### 信頼できる教育機関・組織のリソース
1. [機関名] (アクセス日). [タイトル]. [URL]
2. [機関名] (アクセス日). [タイトル]. [URL]

### 検証済みオンラインリソース
1. [サイト名] (アクセス日). [タイトル]. [URL] - [信頼性の根拠]
2. [サイト名] (アクセス日). [タイトル]. [URL] - [信頼性の根拠]

**信頼性評価基準（必須遵守）**：
- **学術的価値**: 査読済み論文、学術誌、大学・研究機関の出版物を最優先
- **公式性**: 文部科学省、教育委員会、国際教育機関の公式文書を重視
- **時効性**: 最新の情報源（3年以内）を優先、古い情報は学術的価値が高い場合のみ
- **著者・機関の信頼性**: 著名な研究者、権威ある教育機関、国際的に認められた組織
- **検証可能性**: URL、DOI、ISBN等の識別子が明確に記載されていること
- **内容の質**: 具体的なデータ、統計、研究結果に基づく情報を優先
- **偏りの排除**: 商業的・宣伝的な内容は除外、客観的・学術的な内容のみ

**除外基準**：
- 個人ブログ、SNS投稿、匿名情報源
- 商業的・宣伝的なウェブサイト
- 学術的根拠のない一般サイト
- 古すぎる情報（10年以上前）で学術的価値のないもの

**出力条件**：
- レポートで実際に引用された情報源のみを含める
- 各情報源の信頼性根拠を簡潔に記載
- 中学生・高校生の学習に適した内容を重視
- 日本語と英語の情報源を適切に分類
- 出力は日本語で統一
    """

    query = dspy.InputField(desc="Query", format=str)
    report_content = dspy.InputField(desc="Report content", format=str)
    search_results = dspy.InputField(desc="Search results used", format=str)
    references = dspy.OutputField(desc="Generated references", format=str)


class WriteIntegratedSection(dspy.Signature):
    """あなたは日本の英語教育に精通し、客観的なデータと英語教育理論に基づいた分かりやすい解説を書くことに定評のある信頼できるライターです。
下記のクエリー（高校入試や教科書からの英文を含む可能性があります）に関するレポートのアウトラインに基づき、各章の本文を執筆してください。
アウトラインの中にある引用番号は漏れることなく必ず参照し、収集された情報源の内容を適切に解釈しながら、各節ごとに400字以上で解説を記載してください。

**重要**: Related Topics（関連文法事項）を本文内の適切な箇所に統合してください。文法解説は、該当するセクションの内容と自然に結びつくように配置し、学習者が理解しやすい形で提示してください。

解説は緻密かつ包括的で、情報源に基づいたものであることが望ましいです。特に、入力された英文がある場合は、その英文の具体的な分析（文法、語彙、構文、読解ポイントなど）を詳細に含めてください。中学生・高校生が理解しやすい内容を重視し、実践的な学習内容を含めてください。必要に応じて、関連する英語教育理論、歴史的背景、国内外の事例、最新の統計データなどを盛り込んでください。

**文法用語の日本語統一**：
- gerund → 動名詞
- infinitive → 不定詞
- subjunctive → 仮定法
- participle → 分詞
- modal verb → 助動詞
- relative pronoun → 関係代名詞
- passive voice → 受動態
- active voice → 能動態
- present perfect → 現在完了形
- past perfect → 過去完了形
- future perfect → 未来完了形
- conditional → 条件法
- imperative → 命令法
- interrogative → 疑問文

なお、内容の信頼性が重要なので、必ず情報源にあたり、下記指示にあるように引用をするのを忘れないで下さい。
1. アウトラインの"# Title"、"## Title"、"### Title"のタイトルは変更しないでください。
2. 必ず情報源の情報に基づき記載し、ハルシネーションに気をつけること。
   記載の根拠となる参照すべき情報源は "...です[4][1][27]。" "...ます[21][9]。" のように明示してください。
3. 正しく引用が明示されているほどあなたの解説は高く評価されます。
4. 内容に応じて箇条書きを適切に配置し、読者の理解度を深めてください。
5. 日本語の「ですます調」で解説を書いてください。
6. 出力は必要な英文以外は日本語にすることを厳守すること。
7. Related Topicsは本文内の適切な箇所に自然に統合し、学習の流れを妨げないようにしてください。
8. 文法用語は必ず日本語で統一してください。
    """

    query = dspy.InputField(desc="Query", format=str)
    references = dspy.InputField(desc="Collected information sources and citation numbers", format=str)
    section_outline = dspy.InputField(desc="Section outline", format=str)
    related_topics = dspy.InputField(desc="Related grammar topics", format=str)
    section = dspy.OutputField(desc="Generated section with integrated related topics", format=str)


class WriteConclusionEnglish(dspy.Signature):
    """You are a trusted and reliable writer known for creating clear explanations in English learning with expertise in international research and methodologies.
    Based on the report draft, generate a conclusion that summarizes the entire report using expressions as different as possible from the main text, while including future directions and response strategies.
    Focus on international research findings, latest methodologies, and advanced educational approaches.
    Write at least 400 characters, preferably 600 or more.
    Generate only the conclusion text and do not include headers like "## Conclusion".
    Write the conclusion in English.
    """

    query = dspy.InputField(desc="Query", format=str)
    report_draft = dspy.InputField(desc="Report draft", format=str)
    conclusion = dspy.OutputField(desc="Generated conclusion", format=str)


class WriteConclusionJapanese(dspy.Signature):
    """あなたは英語教育問題に精通し、未来志向の提言をすることに定評のある信頼できるライターです。
レポートのドラフトを踏まえて、レポート全体の要約を本文とはできるだけ異なる表現で記載しつつ、英語教育的な観点からの今後の展望や課題、考えられる対策を含んだ結論部を生成します。
中学生・高校生が理解しやすい内容を重視し、実践的な学習内容を含めてください。
最低でも400字以上、可能なら600字以上記載してください。
結論の文章部分のみ生成し、"## 結論" のようなヘッダは入れないでください。
出力は必要な英文以外は日本語にすることを厳守すること。

**文法用語の日本語統一**：
- gerund → 動名詞
- infinitive → 不定詞
- subjunctive → 仮定法
- participle → 分詞
- modal verb → 助動詞
- relative pronoun → 関係代名詞
- passive voice → 受動態
- active voice → 能動態
- present perfect → 現在完了形
- past perfect → 過去完了形
- future perfect → 未来完了形
- conditional → 条件法
- imperative → 命令法
- interrogative → 疑問文
    """

    query = dspy.InputField(desc="Query", format=str)
    report_draft = dspy.InputField(desc="Report draft", format=str)
    conclusion = dspy.OutputField(desc="Generated conclusion", format=str)


def merge_content(english_content: str, japanese_content: str, content_type: str) -> str:
    """英語と日本語のコンテンツを統合し、最適化する"""
    # 英語コンテンツがより専門的で包括的な場合、それを優先
    if len(english_content) > len(japanese_content) * 1.5:
        return english_content
    
    # 日本語コンテンツがより教育的で実践的な場合、それを優先
    if any(keyword in japanese_content for keyword in ['学習', '教育', '指導', '解説', '分析', '理解']):
        return japanese_content
    
    # デフォルトでは英語コンテンツを返す（より包括的）
    return english_content


class StreamLeadWriter(StreamLineWriter):
    def __init__(self, lm=None) -> None:
        super().__init__(lm=lm, signature_cls=WriteLeadJapanese)

    async def __call__(self, query: str, title: str, draft: str) -> AsyncGenerator[str, None]:
        async for chunk in self.generate({"query": query, "title": title, "draft": draft}):
            yield chunk
        lead = self.get_generated_text()
        self.lead = lead


class StreamSectionWriter(StreamLineWriter):
    def __init__(self, lm=None) -> None:
        super().__init__(lm=lm, signature_cls=WriteSectionJapanese)

    async def __call__(self, query: str, references: str, section_outline: str) -> AsyncGenerator[str, None]:
        async for chunk in self.generate(
            {"query": query, "references": references, "section_outline": section_outline}
        ):
            yield chunk
        section_content = self.get_generated_text()
        self.section_content = section_content


class StreamConclusionWriter(StreamLineWriter):
    def __init__(self, lm=None) -> None:
        super().__init__(lm=lm, signature_cls=WriteConclusionJapanese)

    async def __call__(self, query: str, report_draft: str) -> AsyncGenerator[str, None]:
        async for chunk in self.generate({"query": query, "report_draft": report_draft}):
            yield chunk
        conclusion = self.get_generated_text()
        self.conclusion = conclusion


class StreamRelatedTopicsWriter(StreamLineWriter):
    def __init__(self, lm=None) -> None:
        super().__init__(lm=lm, signature_cls=WriteRelatedTopics)
        self.grammar_analyzer = get_grammar_analyzer()

    async def __call__(self, query: str) -> AsyncGenerator[str, None]:
        # 文法構造解析を実行
        analysis = self.grammar_analyzer.analyze_text(query)
        
        # 解析結果をクエリに追加
        enhanced_query = query
        if analysis['grammar_structures']:
            grammar_info = "\n\n検出された文法構造:\n"
            for structure in analysis['grammar_structures']:
                grammar_info += f"- {structure}\n"
            enhanced_query += grammar_info
        
        if analysis['related_topics']:
            related_info = "\n\n関連文法項目:\n"
            for topic in analysis['related_topics'][:3]:
                related_info += f"- {topic}\n"
            enhanced_query += related_info
        
        async for chunk in self.generate({"query": enhanced_query}):
            yield chunk
        related_topics = self.get_generated_text()
        self.related_topics = related_topics


class StreamReferencesWriter(StreamLineWriter):
    def __init__(self, lm=None) -> None:
        super().__init__(lm=lm, signature_cls=WriteReferences)

    async def __call__(self, query: str, report_content: str, search_results: str) -> AsyncGenerator[str, None]:
        async for chunk in self.generate({
            "query": query, 
            "report_content": report_content, 
            "search_results": search_results
        }):
            yield chunk
        references = self.get_generated_text()
        self.references = references


class StreamIntegratedSectionWriter(StreamLineWriter):
    def __init__(self, lm=None) -> None:
        super().__init__(lm=lm, signature_cls=WriteIntegratedSection)
        self.grammar_analyzer = get_grammar_analyzer()

    async def __call__(self, query: str, references: str, section_outline: str, related_topics: str) -> AsyncGenerator[str, None]:
        # セクション内容から文法構造を解析
        analysis = self.grammar_analyzer.analyze_text(section_outline + " " + related_topics)
        
        # 文法解析結果を統合
        grammar_analysis = ""
        if analysis['grammar_structures'] or analysis['key_points']:
            grammar_analysis = "\n\n### 文法構造分析\n"
            if analysis['grammar_structures']:
                grammar_analysis += "**検出された文法構造:**\n"
                for structure in analysis['grammar_structures']:
                    grammar_analysis += f"- {structure}\n"
            if analysis['key_points']:
                grammar_analysis += "\n**学習ポイント:**\n"
                for point in analysis['key_points']:
                    grammar_analysis += f"- {point}\n"
        
        # 関連トピックに文法解析結果を追加
        enhanced_related_topics = related_topics
        if grammar_analysis:
            enhanced_related_topics += grammar_analysis
        
        async for chunk in self.generate({
            "query": query, 
            "references": references, 
            "section_outline": section_outline,
            "related_topics": enhanced_related_topics
        }):
            yield chunk
        section_content = self.get_generated_text()
        self.section_content = section_content 