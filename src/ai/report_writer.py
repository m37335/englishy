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
実践的な指導内容を重視し、学習効果を高めるポイントを含めてください。
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

**最重要**: 提供された検索結果（references）を積極的に活用し、重複を避けて多様で深い内容を記載してください。

**引用番号の必須使用（最重要）**：
- 必ず検索結果を参照する際は引用番号（[1], [2], [3]など）を使用してください
- 各段落で最低1つ以上の引用番号を含めてください
- 引用番号は文の最後に配置してください（例：「...です[1][2]。」）
- 検索結果の内容を説明する際は必ず引用番号を付けてください
- 引用番号なしの内容は最小限にしてください

**内容の質向上方針**：
1. **重複排除（最重要）**: 同じ内容や類似した説明を絶対に繰り返さない。各段落で異なる視点や新しい情報を提供
2. **深い分析の重視**: 表面的な説明ではなく、原因、背景、影響、応用など多角的な分析を含める
3. **多様な視点の統合**: 異なる情報源からの多様な視点を統合し、包括的な理解を促進
4. **実践的応用の充実**: 理論だけでなく、具体的な学習方法や実践例を詳細に説明
5. **段階的学習の構成**: 基礎から応用まで、段階的に理解を深められる論理的な流れ
6. **情報の多様性**: 同じ概念でも異なる角度から説明し、重複を避ける
7. **詳細な解説の充実**: 箇条書きだけでなく、詳細な解説文で深い理解を促進
8. **論理的な展開**: 各段落が論理的に繋がり、全体として一貫した流れを構築

**表現の多様性向上**：
- 「〜という文は、英語の〜を用いた表現の一例です。」のような定型表現を避ける
- 同じ説明パターンを繰り返さず、多様な表現方法を使用
- 各段落で異なる角度からの説明を心がける
- 具体例、比較、対比、段階的説明など様々な手法を活用
- 重複チェック: 同じ概念や説明が複数箇所に現れないよう注意
- **詳細な解説文の重視**: 箇条書きだけでなく、詳細な解説文で深い理解を促進
- **論理的な流れ**: 各段落が論理的に繋がり、全体として一貫した流れを構築
- **英文例の多様性**: ユーザーから与えられた英文以外の解説用英文は、同じものを繰り返し使用しない。多様で実用的な例文を提供

**可読性向上のための構造化（必須）**：
本文中に適切な箇条書きや番号付きリストを配置し、情報を整理してください：

**1. 重要な概念の箇条書き化**：
- 重要な概念やルールは箇条書きで整理（「。」は付けない）
- 例：「• 主語が動作の受け手であることを示す」「• 基本構造は「be動詞 + 過去分詞」」
- **禁止**: 「・特徴: ・ポイント1 ・ポイント2」のような階層的リスト

**2. 具体的な例文の番号付きリスト**：
- 実際の使用例を番号付きリストで提示
- 例：「1. The book is written by the author.（その本は著者によって書かれている）」
- **重要**: ユーザーから与えられた英文以外の例文は、同じものを繰り返し使用しない。多様で実用的な例文を提供

**3. よくある間違いと対策の詳細分析**：
- **間違いの原因分析**: なぜその間違いが起こるのか、心理的・言語学的背景を含めて詳細に説明
- **具体的な間違い例**: 実際に学習者が犯しやすい間違いを具体的に提示（「。」は付けない）
- **間違いの分類**: 文法、語彙、発音、理解の誤りなど、カテゴリ別に整理
- **段階的な対策**: 基礎レベルから応用レベルまで、段階的な対策を提示
- **予防的指導法**: 間違いを未然に防ぐための指導方法や学習アプローチ
- **実践的練習**: 間違いを克服するための具体的な練習方法や演習問題
- **学習者の心理的サポート**: 間違いに対する学習者の心理的負担を軽減する方法
- **長期的な改善戦略**: 継続的な学習を通じた根本的な改善方法
- **例：「• 間違い：The book are written → 正しい：The book is written → 原因：主語と動詞の一致の理解不足 → 対策：主語の単複を明確に意識する練習」**

**4. 練習問題の番号付きリスト**：
- 練習問題や例文を番号付きリストで提示
- 例：「1. The song is sung by the choir.」「2. The homework will be completed by the students.」
- **重要**: ユーザーから与えられた英文以外の練習問題は、同じものを繰り返し使用しない。多様で実用的な問題を提供

**5. 注意点の箇条書き**：
- 学習時の注意点を箇条書きで提示（「。」は付けない）
- 例：「• 主語と動詞の一致に注意」「• 過去分詞の形を正確に覚える」

**6. 小見出しの使用**：
- 複数のポイントをまとめる場合は「### 小見出し」を使用
- 例：「### 受動態の特徴」の下にフラットなリストを配置

**リスト化のルール**：
- **箇条書き（• または -）**: 概念、ポイント、注意点、活用場面など（「。」は付けず、簡潔にまとめる）
- **番号付きリスト（1. 2. 3.）**: 例文、練習問題、学習ステップなど
- **適切な間隔**: リストの前後に空行を入れて読みやすくする
- **自然な配置**: 本文の流れを妨げないよう、適切な箇所に配置
- **階層的リストの禁止**: 箇条書きの中に箇条書きを入れない（例：「・特徴: ・ポイント1 ・ポイント2」は禁止）
- **小見出しの使用**: 複数のポイントをまとめる場合は「### 小見出し」を使用し、その下にフラットなリストを配置
- **箇条書きの簡潔性**: 箇条書きは「。」で終わらず、簡潔な名詞句や動詞句でまとめる
- **詳細解説とのバランス**: 箇条書きは要点整理用、詳細な解説文で深い理解を促進
- **論理的な構成**: 箇条書きの前後に詳細な解説文を配置し、論理的な流れを構築
- **箇条書きの「。」禁止（最重要）**: 箇条書きには絶対に「。」を付けない。名詞句や動詞句で簡潔にまとめる

**検索結果の活用方針**：
1. **具体的なデータの引用**: 検索結果から具体的な数値、統計、研究結果を引用
2. **実践例の紹介**: 検索結果から実際の教育実践例や学習方法を紹介
3. **最新情報の反映**: 検索結果から最新の教育理論や研究動向を反映
4. **多様な視点の統合**: 異なる情報源からの多様な視点を統合
5. **実用的な内容**: 検索結果から学習者にとって実用的な情報を抽出

**内容構成の指針**：
- **導入**: 各セクションの目的と重要性を明確に説明
- **理論的背景**: 学術的な根拠と理論的枠組みを提示
- **実践的分析**: 具体的な例やケーススタディを含む深い分析
- **学習への応用**: 実際の学習場面での活用方法を具体的に提示
- **まとめ**: セクションの要点を整理し、次のセクションへの橋渡し

アウトラインの中にある引用番号は漏れることなく必ず参照し、収集された情報源の内容を適切に解釈しながら、各節ごとに400字以上で解説を記載してください。

**重要**: キーワードを重点的に活用してください。各キーワードに関連する具体的な内容を含め、キーワード間の関連性を明示してください。実践的な例や練習問題を含めて、効果的な指導法を提示してください。

解説は緻密かつ包括的で、情報源に基づいたものであることが望ましいです。特に、入力された英文がある場合は、その英文の具体的な分析（文法、語彙、構文、読解ポイントなど）を詳細に含めてください。実践的な指導内容を重視し、学習効果を高めるポイントを含めてください。必要に応じて、関連する英語教育理論、歴史的背景、国内外の事例、最新の統計データなどを盛り込んでください。
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
4. **必須**: 本文中に適切な箇条書きや番号付きリストを配置し、情報を整理して読みやすくしてください。ただし、箇条書きだけでなく、詳細な解説文で深い理解を促進してください。
5. 日本語の「ですます調」で解説を書いてください。
6. 出力は必要な英文以外は日本語にすることを厳守すること。
7. Related Topicsは本文内の適切な箇所に自然に統合し、学習の流れを妨げないようにしてください。
8. 文法用語は必ず日本語で統一してください。
9. **重複排除**: 同じ内容や類似した説明を繰り返さず、各段落で新しい情報や異なる視点を提供してください。
10. **深い分析**: 表面的な説明ではなく、原因、背景、影響、応用など多角的な分析を含めてください。
11. **詳細解説の充実**: 箇条書きだけでなく、詳細な解説文で深い理解を促進してください。
12. **論理的な展開**: 各段落が論理的に繋がり、全体として一貫した流れを構築してください。
13. **構造化**: 適切な箇条書きや番号付きリストで情報を整理しつつ、詳細な解説文とのバランスを保ってください。
14. **よくある間違いと対策の深い分析**: 「よくある間違いと対策」セクションでは、単なる間違いの列挙ではなく、間違いの原因分析、心理的背景、段階的な対策、予防的指導法、実践的練習、学習者の心理的サポート、長期的な改善戦略を含む包括的な分析を提供してください。
15. **英文例の多様性**: ユーザーから与えられた英文以外の解説用英文は、同じものを繰り返し使用せず、多様で実用的な例文を提供してください。
16. **箇条書きの「。」禁止**: 箇条書きには絶対に「。」を付けず、名詞句や動詞句で簡潔にまとめてください。
    """

    query = dspy.InputField(desc="Query", format=str)
    references = dspy.InputField(desc="Collected information sources and citation numbers", format=str)
    section_outline = dspy.InputField(desc="Section outline", format=str)
    keywords = dspy.InputField(desc="Keywords to focus on", format=str)
    section = dspy.OutputField(desc="Generated section", format=str)


class WriteRelatedTopics(dspy.Signature):
    """あなたは英語学習教材の専門家で、指導効果を最大化する関連トピックを生成する信頼できるライターです。
    与えられたクエリー、アウトライン構造、キーワード、文法解析結果を基に、生徒の理解を深めるための関連トピックを生成してください。
    
    **重要**: 関連トピックは必ず日本語で作成し、文法用語も日本語に統一してください（例：gerund→動名詞、infinitive→不定詞、subjunctive→仮定法など）。
    
    関連トピックの生成方針：
    1. **学習の流れに沿った関連性**: アウトライン構造を考慮し、学習の自然な流れに沿った関連トピック
    2. **キーワードとの連携**: 提供されたキーワードを活用し、重点的に学習すべき関連トピック
    3. **文法解析結果の活用**: 既存の文法解析結果を基に、より深い理解を促進する関連トピック
    4. **実践的な学習効果**: 実際の学習に役立つ、実践的な関連トピック
    5. **段階的な学習**: 基礎から応用まで、段階的に学習できる関連トピック
    
    出力フォーマット：
    ## 関連学習トピック
    
    ### 基礎文法項目
    - **[文法項目名]**: [その文法項目の簡潔な説明]。学習のポイント: [学習時の注意点]
    
    ### 発展学習項目
    - **[発展項目名]**: [発展項目の説明]。関連性: [メイントピックとの関連]
    
    ### 実践応用項目
    - **[実践項目名]**: [実践項目の説明]。活用場面: [実際の使用場面]
    
    ### 学習のポイント
    - [学習効果を高めるための具体的なアドバイス]
    - [よくある間違いと対策]
    - [効果的な練習方法]
    
    生成時の注意点：
    - アウトライン構造の各セクションに関連するトピックを生成
    - キーワードを重点的に活用し、学習効果を最大化
    - 文法解析結果を基に、より正確で包括的な関連トピック
    - 実践的な学習に活用できるレベルで説明
    - 実践的な学習に役立つ内容を重視
    - 段階的な学習フローに沿った構成
    """  # noqa: E501

    query = dspy.InputField(desc="クエリー", format=str)
    outline_structure = dspy.InputField(desc="アウトライン構造", format=str)
    keywords = dspy.InputField(desc="重要なキーワード", format=str)
    grammar_analysis = dspy.InputField(desc="文法解析結果", format=str)
    related_topics = dspy.OutputField(desc="学習効果を最大化する関連トピック", format=str)


class WriteReferences(dspy.Signature):
    """あなたは英語教育の専門家で、実用的で学習効果の高い参考文献の整理に精通しています。
    与えられたクエリー、レポート内容、検索結果、アウトライン構造、キーワードを基に、多様で実用的な情報源を含む包括的な参考文献リストを生成してください。
    
    **重要**: 参考文献は必ず日本語で作成し、統一された引用形式（APA形式）を使用してください。
    
    参考文献生成の方針：
    1. **多様性の重視**: 学術的資料から実用的なWebリソースまで、多様な情報源を含める
    2. **学習効果の最大化**: 理解しやすく、実践に役立つ情報源を選択
    3. **アウトライン構造との連携**: 各セクションに関連する情報源を適切に整理
    4. **キーワードとの関連性**: 重要なキーワードに関連する情報源を重点的に選択
    5. **段階的な学習支援**: 基礎から応用まで、段階的に学習できる情報源の構成
    
    出力フォーマット（APA形式）：
    ## 参考文献
    
    ### 学術文献・研究論文（高信頼度）
    1. 著者名, A. A., & 著者名, B. B. (出版年). 論文タイトル. *雑誌名*, *巻号*, ページ番号. DOI: [DOI番号]
    2. 著者名, C. C. (出版年). 書籍タイトル. 出版社名.
    
    ### 公式ガイドライン・政策文書（高信頼度）
    1. 文部科学省. (年度). タイトル. 取得日時, https://www.mext.go.jp/...
    2. 教育委員会. (年度). タイトル. 取得日時, https://www.city.xxx.lg.jp/...
    
    ### 教育機関・組織のリソース（中〜高信頼度）
    1. 機関名. (アクセス日). タイトル. 取得日時, https://www.xxx.ac.jp/...
    2. 機関名. (アクセス日). タイトル. 取得日時, https://www.xxx.org/...
    
    ### 実用的なWebリソース（中信頼度）
    1. サイト名. (アクセス日). タイトル. 取得日時, https://www.xxx.com/... - [内容の特徴]
    2. サイト名. (アクセス日). タイトル. 取得日時, https://www.xxx.com/... - [内容の特徴]
    
    ### 補足的な学習リソース（中信頼度）
    1. サイト名. (アクセス日). タイトル. 取得日時, https://www.xxx.com/... - [学習への活用方法]
    2. サイト名. (アクセス日). タイトル. 取得日時, https://www.xxx.com/... - [学習への活用方法]
    
    **柔軟な信頼性評価基準**：
    - **高信頼度**: 査読済み論文、学術誌、公式文書、権威ある教育機関の出版物
    - **中信頼度**: 教育関連サイト、専門ブログ、ニュース記事、実用的なWebリソース
    - **低信頼度**: 個人の意見のみ、未検証の情報、明らかに不正確な内容
    
    **包括的な情報源選択**：
    - **学術的資料**: 研究論文、学術誌、教育理論書
    - **公式文書**: 文部科学省、教育委員会、国際教育機関のガイドライン
    - **教育機関**: 大学、研究機関、教育団体のリソース
    - **実用的サイト**: 英語学習サイト、教育ブログ、ニュース記事
    - **補足資料**: 練習問題、解説動画、学習ツール
    
    **品質チェック基準**：
    - **内容の正確性**: 明らかな誤りや矛盾がないこと
    - **学習への有用性**: 実際の学習に役立つ内容であること
    - **適切なレベル**: 実践的な学習に活用できるレベルであること
    - **情報の鮮度**: 古すぎず、現在も有効な情報であること
    - **出典の明確性**: 情報源が明確に記載されていること
    
    **除外基準（最小限）**：
    - 明らかに不正確または有害な情報
    - 完全に匿名で検証不可能な情報源
    - 学習レベルに明らかに不適切な内容（過度に専門的または初級的）
    - 純粋に商業的・宣伝的な内容のみ
    
    **出力条件**：
    - レポートで実際に引用された情報源を中心に、関連する補足情報源も含める
    - 各情報源の信頼度レベルと内容の特徴を簡潔に記載
    - 実践的な学習に活用できる内容を重視
    - 日本語と英語の情報源を適切に分類
    - アウトライン構造に基づく論理的な整理
    - キーワードに関連する情報源を重点的に選択
    - 出力は日本語で統一
    - APA形式の統一された引用形式を使用
    - 多様性を重視し、実用的な学習リソースを積極的に含める
    """  # noqa: E501

    query = dspy.InputField(desc="クエリー", format=str)
    report_content = dspy.InputField(desc="レポート内容", format=str)
    search_results = dspy.InputField(desc="使用された検索結果", format=str)
    outline_structure = dspy.InputField(desc="アウトライン構造", format=str)
    keywords = dspy.InputField(desc="重要なキーワード", format=str)
    references = dspy.OutputField(desc="生成された参考文献", format=str)


class WriteInlineReferences(dspy.Signature):
    """あなたは英語教育の専門家で、本文中の引用番号に対応した参考文献リストを生成する信頼できるライターです。
    与えられた本文と検索結果を基に、本文中で実際に引用された番号に対応する参考文献リストを生成してください。
    
    **重要**: 本文中で実際に引用されている番号のみを含め、対応する検索結果から適切な参考文献を選択してください。
    
    **処理手順**：
    1. **引用番号の抽出**: 本文から引用番号（[1], [2], [3]など）を抽出
    2. **対応する検索結果の選択**: 抽出された番号に対応する検索結果を選択
    3. **参考文献リストの生成**: 選択された検索結果から適切な参考文献形式でリストを生成
    
    **出力フォーマット**：
    ## 参考文献
    
    1. サイト名. (アクセス日). タイトル. 取得日時, https://www.xxx.com/...
    2. サイト名. (アクセス日). タイトル. 取得日時, https://www.xxx.com/...
    3. サイト名. (アクセス日). タイトル. 取得日時, https://www.xxx.com/...
    
    **注意点**：
    - 本文中で実際に引用されている番号のみを含める
    - 引用されていない番号は含めない
    - 検索結果から適切な情報源を選択する
    - APA形式の統一された引用形式を使用
    - 日本語で統一
    - 各参考文献は番号順に整理
    """

    report_content = dspy.InputField(desc="本文内容", format=str)
    search_results = dspy.InputField(desc="検索結果", format=str)
    inline_references = dspy.OutputField(desc="本文中で引用された番号に対応する参考文献リスト", format=str)


class WriteIntegratedSection(dspy.Signature):
    """あなたは日本の英語教育に精通し、客観的なデータと英語教育理論に基づいた分かりやすい解説を書くことに定評のある信頼できるライターです。
下記のクエリー（高校入試や教科書からの英文を含む可能性があります）に関するレポートのアウトラインに基づき、各章の本文を執筆してください。

**最重要**: 提供された検索結果（references）を積極的に活用し、重複を避けて多様で深い内容を記載してください。

**引用番号の必須使用（最重要）**：
- 必ず検索結果を参照する際は引用番号（[1], [2], [3]など）を使用してください
- 各段落で最低1つ以上の引用番号を含めてください
- 引用番号は文の最後に配置してください（例：「...です[1][2]。」）
- 検索結果の内容を説明する際は必ず引用番号を付けてください
- 引用番号なしの内容は最小限にしてください

**内容の質向上方針**：
1. **重複排除**: 同じ内容や類似した説明を繰り返さない。各段落で異なる視点や新しい情報を提供
2. **深い分析の重視**: 表面的な説明ではなく、原因、背景、影響、応用など多角的な分析を含める
3. **多様な視点の統合**: 異なる情報源からの多様な視点を統合し、包括的な理解を促進
4. **実践的応用の充実**: 理論だけでなく、具体的な学習方法や実践例を詳細に説明
5. **段階的学習の構成**: 基礎から応用まで、段階的に理解を深められる論理的な流れ
6. **詳細な解説の充実**: 箇条書きだけでなく、詳細な解説文で深い理解を促進
7. **論理的な展開**: 各段落が論理的に繋がり、全体として一貫した流れを構築

**表現の多様性向上**：
- 「〜という文は、英語の〜を用いた表現の一例です。」のような定型表現を避ける
- 同じ説明パターンを繰り返さず、多様な表現方法を使用
- 各段落で異なる角度からの説明を心がける
- 具体例、比較、対比、段階的説明など様々な手法を活用
- **詳細な解説文の重視**: 箇条書きだけでなく、詳細な解説文で深い理解を促進
- **論理的な流れ**: 各段落が論理的に繋がり、全体として一貫した流れを構築
- **英文例の多様性**: ユーザーから与えられた英文以外の解説用英文は、同じものを繰り返し使用しない。多様で実用的な例文を提供

**可読性向上のための構造化（必須）**：
本文中に適切な箇条書きや番号付きリストを配置し、情報を整理してください：

**1. 重要な概念の箇条書き化**：
- 重要な概念やルールは箇条書きで整理（「。」は付けない）
- 例：「• 主語が動作の受け手であることを示す」「• 基本構造は「be動詞 + 過去分詞」」

**2. 具体的な例文の番号付きリスト**：
- 実際の使用例を番号付きリストで提示
- 例：「1. The book is written by the author.（その本は著者によって書かれている）」

**3. よくある間違いと対策の詳細分析**：
- **間違いの原因分析**: なぜその間違いが起こるのか、心理的・言語学的背景を含めて詳細に説明
- **具体的な間違い例**: 実際に学習者が犯しやすい間違いを具体的に提示（「。」は付けない）
- **間違いの分類**: 文法、語彙、発音、理解の誤りなど、カテゴリ別に整理
- **段階的な対策**: 基礎レベルから応用レベルまで、段階的な対策を提示
- **予防的指導法**: 間違いを未然に防ぐための指導方法や学習アプローチ
- **実践的練習**: 間違いを克服するための具体的な練習方法や演習問題
- **学習者の心理的サポート**: 間違いに対する学習者の心理的負担を軽減する方法
- **長期的な改善戦略**: 継続的な学習を通じた根本的な改善方法
- **例：「• 間違い：The book are written → 正しい：The book is written → 原因：主語と動詞の一致の理解不足 → 対策：主語の単複を明確に意識する練習」**

**4. 練習問題の番号付きリスト**：
- 練習問題や例文を番号付きリストで提示
- 例：「1. The song is sung by the choir.」「2. The homework will be completed by the students.」

**5. 注意点の箇条書き**：
- 学習時の注意点を箇条書きで提示（「。」は付けない）
- 例：「• 主語と動詞の一致に注意」「• 過去分詞の形を正確に覚える」

**リスト化のルール**：
- **箇条書き（• または -）**: 概念、ポイント、注意点、活用場面など（「。」は付けず、簡潔にまとめる）
- **番号付きリスト（1. 2. 3.）**: 例文、練習問題、学習ステップなど
- **適切な間隔**: リストの前後に空行を入れて読みやすくする
- **自然な配置**: 本文の流れを妨げないよう、適切な箇所に配置
- **箇条書きの簡潔性**: 箇条書きは「。」で終わらず、簡潔な名詞句や動詞句でまとめる
- **詳細解説とのバランス**: 箇条書きは要点整理用、詳細な解説文で深い理解を促進
- **論理的な構成**: 箇条書きの前後に詳細な解説文を配置し、論理的な流れを構築
- **箇条書きの「。」禁止（最重要）**: 箇条書きには絶対に「。」を付けない。名詞句や動詞句で簡潔にまとめる

**検索結果の活用方針**：
1. **具体的なデータの引用**: 検索結果から具体的な数値、統計、研究結果を引用
2. **実践例の紹介**: 検索結果から実際の教育実践例や学習方法を紹介
3. **最新情報の反映**: 検索結果から最新の教育理論や研究動向を反映
4. **多様な視点の統合**: 異なる情報源からの多様な視点を統合
5. **実用的な内容**: 検索結果から学習者にとって実用的な情報を抽出

**内容構成の指針**：
- **導入**: 各セクションの目的と重要性を明確に説明（詳細な解説文で）
- **理論的背景**: 学術的な根拠と理論的枠組みを詳細に提示
- **実践的分析**: 具体的な例やケーススタディを含む深い分析（多角的な視点で）
- **学習への応用**: 実際の学習場面での活用方法を具体的に提示（段階的な説明で）
- **まとめ**: セクションの要点を整理し、次のセクションへの橋渡し（論理的な流れで）
- **詳細解説の充実**: 各セクションで詳細な解説文を充実させ、深い理解を促進
- **論理的な展開**: 各段落が論理的に繋がり、全体として一貫した流れを構築

アウトラインの中にある引用番号は漏れることなく必ず参照し、収集された情報源の内容を適切に解釈しながら、各節ごとに600字以上で詳細な解説を記載してください。箇条書きだけでなく、詳細な解説文で深い理解を促進してください。

**重要**: Related Topics（関連文法事項）を本文内の適切な箇所に自然に統合してください。文法解説は、該当するセクションの内容と自然に結びつくように配置し、学習者が理解しやすい形で提示してください。

解説は緻密かつ包括的で、情報源に基づいたものであることが望ましいです。特に、入力された英文がある場合は、その英文の具体的な分析（文法、語彙、構文、読解ポイントなど）を詳細に含めてください。実践的な指導内容を重視し、学習効果を高めるポイントを含めてください。必要に応じて、関連する英語教育理論、歴史的背景、国内外の事例、最新の統計データなどを盛り込んでください。**重要**: 箇条書きだけでなく、詳細な解説文で深い理解を促進し、各段落が論理的に繋がるよう心がけてください。

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
9. **重複排除**: 同じ内容や類似した説明を繰り返さず、各段落で新しい情報や異なる視点を提供してください。
10. **深い分析**: 表面的な説明ではなく、原因、背景、影響、応用など多角的な分析を含めてください。
11. **詳細解説の充実**: 箇条書きだけでなく、詳細な解説文で深い理解を促進してください。
12. **論理的な展開**: 各段落が論理的に繋がり、全体として一貫した流れを構築してください。
13. **構造化**: 適切な箇条書きや番号付きリストで情報を整理しつつ、詳細な解説文とのバランスを保ってください。
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
実践的な指導内容を重視し、学習効果を高めるポイントを含めてください。
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

    async def __call__(self, query: str, references: str, section_outline: str, keywords: str = "") -> AsyncGenerator[str, None]:
        # キーワードが提供されていない場合は空文字列を使用
        if not keywords:
            keywords = ""
        
        async for chunk in self.generate(
            {"query": query, "references": references, "section_outline": section_outline, "keywords": keywords}
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


import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class StreamRelatedTopicsWriter(StreamLineWriter):
    def __init__(self, lm=None) -> None:
        super().__init__(lm=lm, signature_cls=WriteRelatedTopics)
        self.grammar_analyzer = get_grammar_analyzer()

    async def __call__(
        self, 
        query: str, 
        outline_structure: Optional[Dict] = None,
        keywords: Optional[List[str]] = None,
        grammar_analysis: Optional[Dict] = None
    ) -> AsyncGenerator[str, None]:
        """
        アウトライン構造、キーワード、文法解析結果を基に関連トピックを生成
        
        Args:
            query: クエリー
            outline_structure: アウトライン構造（Outlineオブジェクト）
            keywords: 重要なキーワードリスト
            grammar_analysis: 文法解析結果
            
        Yields:
            str: 関連トピックの生成結果
        """
        # アウトライン構造をテキストに変換
        outline_text = ""
        if outline_structure:
            outline_text = self._convert_outline_to_text(outline_structure)
        
        # キーワードをテキストに変換
        keywords_text = ""
        if keywords:
            keywords_text = ", ".join(keywords)
        
        # 文法解析結果をテキストに変換
        grammar_text = ""
        if grammar_analysis:
            grammar_text = self._convert_grammar_analysis_to_text(grammar_analysis)
        else:
            # 文法解析が提供されていない場合は実行
            analysis = self.grammar_analyzer.analyze_text(query)
            grammar_text = self._convert_grammar_analysis_to_text(analysis)
        
        # 関連トピック生成
        async for chunk in self.generate({
            "query": query,
            "outline_structure": outline_text,
            "keywords": keywords_text,
            "grammar_analysis": grammar_text
        }):
            yield chunk
        
        related_topics = self.get_generated_text()
        self.related_topics = related_topics
        logger.info(f"Generated related topics with {len(keywords) if keywords else 0} keywords")
    
    def _convert_outline_to_text(self, outline: Dict) -> str:
        """
        アウトライン構造をテキスト形式に変換
        
        Args:
            outline: Outlineオブジェクト
            
        Returns:
            str: アウトライン構造のテキスト表現
        """
        try:
            text_parts = []
            
            # タイトル
            if hasattr(outline, 'title') and outline.title:
                text_parts.append(f"タイトル: {outline.title}")
            
            # セクション構造
            if hasattr(outline, 'section_outlines') and outline.section_outlines:
                text_parts.append("\nセクション構造:")
                for i, section in enumerate(outline.section_outlines, 1):
                    text_parts.append(f"  {i}. {section.title}")
                    
                    # サブセクション
                    if hasattr(section, 'subsection_outlines') and section.subsection_outlines:
                        for j, subsection in enumerate(section.subsection_outlines, 1):
                            text_parts.append(f"    {i}.{j} {subsection.title}")
            
            result = "\n".join(text_parts)
            if not result.strip():
                return "アウトライン構造の変換に失敗しました"
            return result
            
        except Exception as e:
            logger.warning(f"Failed to convert outline to text: {e}")
            return "アウトライン構造の変換に失敗しました"
    
    def _convert_grammar_analysis_to_text(self, grammar_analysis: Dict) -> str:
        """
        文法解析結果をテキスト形式に変換
        
        Args:
            grammar_analysis: 文法解析結果
            
        Returns:
            str: 文法解析結果のテキスト表現
        """
        try:
            text_parts = []
            
            # 検出された文法構造
            if hasattr(grammar_analysis, 'grammar_structures') and grammar_analysis.grammar_structures:
                text_parts.append("検出された文法構造:")
                for structure in grammar_analysis.grammar_structures:
                    text_parts.append(f"  - {structure}")
            
            # 関連トピック
            if hasattr(grammar_analysis, 'related_topics') and grammar_analysis.related_topics:
                text_parts.append("\n関連トピック:")
                for topic in grammar_analysis.related_topics:
                    text_parts.append(f"  - {topic}")
            
            # 学習ポイント
            if hasattr(grammar_analysis, 'learning_points') and grammar_analysis.learning_points:
                text_parts.append("\n学習ポイント:")
                for point in grammar_analysis.learning_points:
                    text_parts.append(f"  - {point}")
            
            # 難易度
            if hasattr(grammar_analysis, 'difficulty_level') and grammar_analysis.difficulty_level:
                text_parts.append(f"\n難易度: {grammar_analysis.difficulty_level}")
            
            result = "\n".join(text_parts)
            if not result.strip():
                return "文法解析結果の変換に失敗しました"
            return result
            
        except Exception as e:
            logger.warning(f"Failed to convert grammar analysis to text: {e}")
            return "文法解析結果の変換に失敗しました"


class StreamReferencesWriter(StreamLineWriter):
    def __init__(self, lm=None) -> None:
        super().__init__(lm=lm, signature_cls=WriteReferences)

    async def __call__(
        self, 
        query: str, 
        report_content: str, 
        search_results: str,
        outline_structure: Optional[Dict] = None,
        keywords: Optional[List[str]] = None
    ) -> AsyncGenerator[str, None]:
        """
        レポート内容、検索結果、アウトライン構造、キーワードを基に参考文献を生成
        
        Args:
            query: クエリー
            report_content: レポート内容
            search_results: 使用された検索結果
            outline_structure: アウトライン構造（Outlineオブジェクト）
            keywords: 重要なキーワードリスト
            
        Yields:
            str: 参考文献の生成結果
        """
        # アウトライン構造をテキストに変換
        outline_text = ""
        if outline_structure:
            outline_text = self._convert_outline_to_text(outline_structure)
        
        # キーワードをテキストに変換
        keywords_text = ""
        if keywords:
            keywords_text = ", ".join(keywords)
        
        # 参考文献生成
        async for chunk in self.generate({
            "query": query, 
            "report_content": report_content, 
            "search_results": search_results,
            "outline_structure": outline_text,
            "keywords": keywords_text
        }):
            yield chunk
        
        references = self.get_generated_text()
        self.references = references
        logger.info(f"Generated references with {len(keywords) if keywords else 0} keywords")
    
    def _convert_outline_to_text(self, outline: Dict) -> str:
        """
        アウトライン構造をテキスト形式に変換
        
        Args:
            outline: Outlineオブジェクト
            
        Returns:
            str: アウトライン構造のテキスト表現
        """
        try:
            text_parts = []
            
            # タイトル
            if hasattr(outline, 'title') and outline.title:
                text_parts.append(f"タイトル: {outline.title}")
            
            # セクション構造
            if hasattr(outline, 'section_outlines') and outline.section_outlines:
                text_parts.append("\nセクション構造:")
                for i, section in enumerate(outline.section_outlines, 1):
                    text_parts.append(f"  {i}. {section.title}")
                    
                    # サブセクション
                    if hasattr(section, 'subsection_outlines') and section.subsection_outlines:
                        for j, subsection in enumerate(section.subsection_outlines, 1):
                            text_parts.append(f"    {i}.{j} {subsection.title}")
            
            result = "\n".join(text_parts)
            if not result.strip():
                return "アウトライン構造の変換に失敗しました"
            return result
            
        except Exception as e:
            logger.warning(f"Failed to convert outline to text: {e}")
            return "アウトライン構造の変換に失敗しました"


class StreamInlineReferencesWriter(StreamLineWriter):
    def __init__(self, lm=None) -> None:
        super().__init__(lm=lm, signature_cls=WriteInlineReferences)

    async def __call__(self, report_content: str, search_results: str) -> AsyncGenerator[str, None]:
        """
        本文内容と検索結果を基に、本文中で実際に引用された番号に対応する参考文献リストを生成
        
        Args:
            report_content: 本文内容
            search_results: 検索結果
            
        Yields:
            str: 本文中で引用された番号に対応する参考文献リスト
        """
        # 本文から引用番号を抽出
        import re
        reference_numbers = re.findall(r'\[(\d+)\]', report_content)
        
        # 重複を除去してソート
        unique_numbers = sorted(list(set(reference_numbers)), key=int)
        
        # デバッグ: 抽出された番号をログ出力
        logger.info(f"Extracted reference numbers: {reference_numbers}")
        logger.info(f"Unique reference numbers: {unique_numbers}")
        
        # 検索結果を解析して参考文献リストを生成
        inline_references_text = "## 参考文献\n\n"
        
        # 検索結果を解析して文献リストを作成
        search_lines = search_results.split('\n')
        logger.info(f"Search results lines count: {len(search_lines)}")
        
        # 検索結果から文献情報を抽出
        references = []
        current_title = ""
        current_url = ""
        
        for line in search_lines:
            line = line.strip()
            if line.startswith("Title: "):
                current_title = line.replace("Title: ", "").strip()
            elif line.startswith("URL: "):
                current_url = line.replace("URL: ", "").strip()
                # TitleとURLが揃ったら文献として追加
                if current_title and current_url:
                    references.append({
                        'title': current_title,
                        'url': current_url
                    })
                    current_title = ""
                    current_url = ""
        
        logger.info(f"Extracted {len(references)} references from search results")
        
        # 引用番号と文献を対応させる
        for i, number in enumerate(unique_numbers):
            try:
                ref_num = int(number)
                # 番号に対応する文献を選択（1から始まる番号を0ベースのインデックスに変換）
                if ref_num <= len(references):
                    ref = references[ref_num - 1]  # 1ベースの番号を0ベースのインデックスに変換
                    inline_references_text += f"{ref_num}. {ref['title']}. {ref['url']}\n"
                    logger.info(f"Added reference {ref_num}: {ref['title']}")
                else:
                    # 番号が文献数より大きい場合はプレースホルダー
                    inline_references_text += f"{ref_num}. （文献情報が見つかりませんでした）\n"
                    logger.warning(f"Reference number {ref_num} exceeds available references")
            except ValueError:
                continue
        
        # 引用番号が見つからない場合は空のリストを生成
        if not unique_numbers:
            inline_references_text = "## 参考文献\n\n（本文中に引用番号が見つかりませんでした）"
        
        # デバッグ: 生成された参考文献リストをログ出力
        logger.info(f"Generated inline references text: {inline_references_text}")
        
        # 手動で作成した参考文献リストを直接返す（AIのgenerate()は使用しない）
        self.inline_references = inline_references_text
        logger.info(f"Generated inline references for {len(unique_numbers)} unique numbers: {unique_numbers}")
        
        # 参考文献リストをチャンクに分けて返す
        chunk_size = 100
        for i in range(0, len(inline_references_text), chunk_size):
            yield inline_references_text[i:i + chunk_size]


class StreamIntegratedSectionWriter(StreamLineWriter):
    def __init__(self, lm=None) -> None:
        super().__init__(lm=lm, signature_cls=WriteIntegratedSection)
        self.grammar_analyzer = get_grammar_analyzer()

    async def __call__(self, query: str, references: str, section_outline: str, related_topics: str, keywords: str = "") -> AsyncGenerator[str, None]:
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
        
        # キーワード情報を追加
        if keywords:
            enhanced_related_topics += f"\n\n### 重点キーワード\n{keywords}"
        
        async for chunk in self.generate({
            "query": query, 
            "references": references, 
            "section_outline": section_outline,
            "related_topics": enhanced_related_topics
        }):
            yield chunk
        section_content = self.get_generated_text()
        self.section_content = section_content 