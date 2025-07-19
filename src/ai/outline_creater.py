import re

import dspy
import litellm
from pydantic import BaseModel

from src.utils.logging import logger


def extract_keywords_from_content(content: str) -> list[str]:
    """コンテンツからキーワードを抽出する"""
    keywords = []
    
    # 文法関連キーワード
    grammar_keywords = [
        "gerund", "infinitive", "participle", "subjunctive", "modal verb",
        "relative pronoun", "passive voice", "active voice", "present perfect",
        "past perfect", "future perfect", "conditional", "imperative", "interrogative",
        "動名詞", "不定詞", "分詞", "仮定法", "助動詞", "関係代名詞", "受動態", "能動態",
        "現在完了形", "過去完了形", "未来完了形", "条件法", "命令法", "疑問文"
    ]
    
    # 教育関連キーワード
    education_keywords = [
        "teaching", "learning", "education", "student", "practice", "exercise",
        "method", "approach", "technique", "strategy", "difficulty", "mistake",
        "指導", "学習", "教育", "生徒", "練習", "演習", "方法", "アプローチ",
        "テクニック", "戦略", "困難", "間違い", "理解", "応用"
    ]
    
    # コンテンツからキーワードを検索
    content_lower = content.lower()
    for keyword in grammar_keywords + education_keywords:
        if keyword.lower() in content_lower:
            keywords.append(keyword)
    
    # 重複を除去して上位10個まで返す
    unique_keywords = list(dict.fromkeys(keywords))[:10]
    return unique_keywords


def extract_keywords_from_references(references: list[dict], subsection_reference_ids: list[int]) -> list[str]:
    """参照情報からサブセクション用のキーワードを抽出"""
    keywords = []
    
    for ref in references:
        # サブセクションの引用番号と一致するかチェック
        ref_id = ref.get('id', 0)
        if ref_id in subsection_reference_ids:
            # タイトルとスニペットからキーワード抽出
            content = f"{ref.get('title', '')} {ref.get('snippet', '')}"
            ref_keywords = extract_keywords_from_content(content)
            keywords.extend(ref_keywords)
    
    # 重複を除去して上位5個まで返す
    unique_keywords = list(dict.fromkeys(keywords))[:5]
    return unique_keywords


class CreateOutline(dspy.Signature):
    """あなたは、中学生・高校生の英語学習をサポートする英語教育の専門家です。最新の英語教育研究や学習法を常にフォローし、生徒が理解しやすい解説を心がけています。収集された情報源をもとに、下記のクエリーに対する分かりやすい解説レポートのアウトラインと簡潔なタイトルを作成してください。結論パートは作成しないでください。

**重要**: タイトルとセクション名は必ず日本語で作成してください。文法用語も日本語に統一してください（例：gerund→動名詞、infinitive→不定詞、subjunctive→仮定法など）。

アウトラインは以下のMarkdownフォーマットに従って作成し、次のルールを厳守すること：

1. **学習者目線の構成**：
   - クエリーに対して、中学生・高校生が理解しやすい英語教育的な観点からの解説・分析を目的とした構成にする
   - 基礎から応用へと段階的に理解できるような流れにする

2. **タイトルの形式**：
   - "# タイトル" をレポートのタイトルに用いる（必ず日本語）
   - "## セクション名" を章のタイトルとして用いる（必ず日本語）
   - "### サブセクション名" を節のタイトルとして用いる（必ず日本語）

3. **文法用語の日本語統一**：
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

4. **セクション構成**：
   - 各章 ("## セクション名") に対して、必ず2～3個の節 ("### サブセクション名") を生成すること
   - 章の数はクエリーに応じて5～15個の間で作成すること（内容の複雑さに応じて調整）
   - より包括的な内容の場合は章を増やし、シンプルな内容の場合は章を減らす

5. **サブセクションの内容**：
   - 各節には、収集された情報源をできるだけ多く含めるようにし、必ず最低3～5個以上の異なる引用番号を使用すること
   - 節同士で内容が類似しそうな場合、節を統合し、他の論点の節を追加すること
   - 引用番号が重複する場合は、アウトライン全体を見直してより多様な情報源を取り入れること

6. **引用情報の記載方法**：
   - 引用番号は節の次の行に記載すること
   - "### サブセクション名 [3][4]" のように同じ行に記載してはならない
   - 存在しない引用番号は使用しないこと

7. **Markdownフォーマットに関するルール**：
   - "## 結論"という結論パートは絶対に作成してはいけない
   - 出力には "# タイトル", "## セクション名"、"### サブセクション名" などのMarkdown形式のタイトル以外のテキストを一切含めないこと
   - "#### タイトル" のような深い階層は作成しないこと
   - 番号付けは不要、階層は "#", "##", "###" のみ使用すること

8. **内容の質**：
   - 各行はタイトル、セクション、サブセクション、引用番号のいずれかで、それ以外の情報を記載してはならない
   - 中学生・高校生が理解しやすい、実践的な内容を心がけること
   - 英語学習の基礎から応用まで、段階的に理解できる構成にする

【出力例】
# 動名詞の完全ガイド
## 動名詞とは
### 基本的な形と意味
[1][2][3]
### 不定詞との違い
[4][5][6]
## 使い方のポイント
### 主語として使う場合
[1][3][7]
### 目的語として使う場合
[2][4][8]
## よくある間違い
### 不定詞との混同
[5][6][9]
### 動詞の使い分け
[7][8][10]
## 練習問題
### 基礎問題
[1][2][3]
### 応用問題
[4][5][6]

【不適切な出力例】
# Gerunds in English Language Learning    // 英語タイトルはNG
## Understanding Gerunds    // 英語セクション名はNG
### Definition and Characteristics    // 英語サブセクション名はNG
[4][67]
このサブセクションでは...    // 説明文など要求していない不要な行は削除
### Differences Between Gerunds and Infinitives    // 英語サブセクション名はNG
[30][28][1][27][102]
## セクション2
[2][24][29][11][4]    // セクション自体に引用がついている
### サブセクション1
### サブセクション: yyy    // 「サブセクション: 」という修飾はNG
[2][24][51]
### サブセクション3
[29][11][4][156]     // 存在しない引用番号を使用している
"""  # noqa: E501

    query = dspy.InputField(desc="Query", format=str)
    topics = dspy.InputField(desc="Expanded topics for research", format=str)
    references = dspy.InputField(desc="Collected information sources and citation numbers", format=str)
    outline = dspy.OutputField(desc="Report outline", format=str)


class FixOutline(dspy.Signature):
    """あなたは、中学生・高校生向けの英語学習教材の編集者です。英語学習の解説レポートのアウトラインを作成しましたが、下記のルールに従っていない部分があるかもしれません。校正・編集して、学習者が理解しやすい構成にしてください。

**重要**: タイトルとセクション名は必ず日本語で作成してください。文法用語も日本語に統一してください（例：gerund→動名詞、infinitive→不定詞、subjunctive→仮定法など）。

以下のルールに従って校正・編集してください：

1. **学習者目線の構成**：
   - クエリーに対して、中学生・高校生が理解しやすい英語教育的な観点からの解説・分析を目的とした構成にする
   - 基礎から応用へと段階的に理解できるような流れにする

2. **タイトルの形式**：
   - "# タイトル" をレポートのタイトルに用いる（必ず日本語）
   - "## セクション名" を章のタイトルとして用いる（必ず日本語）
   - "### サブセクション名" を節のタイトルとして用いる（必ず日本語）

3. **文法用語の日本語統一**：
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

4. **セクション構成**：
   - 各章 ("## セクション名") に対して、必ず2～3個の節 ("### サブセクション名") を生成すること
   - 章の数はクエリーに応じて5～15個の間で作成すること（内容の複雑さに応じて調整）
   - より包括的な内容の場合は章を増やし、シンプルな内容の場合は章を減らす

5. **サブセクションの内容**：
   - 各節には、収集された情報源をできるだけ多く含めるようにし、必ず最低3～5個以上の異なる引用番号を使用すること
   - 節同士で内容が類似しそうな場合、節を統合し、他の論点の節を追加すること
   - 引用番号が重複する場合は、アウトライン全体を見直してより多様な情報源を取り入れること

6. **引用情報の記載方法**：
   - 引用番号は節の次の行に記載すること
   - "### サブセクション名 [3][4]" のように同じ行に記載してはならない
   - 存在しない引用番号は使用しないこと

7. **Markdownフォーマットに関するルール**：
   - "## 結論"という結論パートは絶対に作成してはいけない
   - 出力には "# タイトル", "## セクション名"、"### サブセクション名" などのMarkdown形式のタイトル以外のテキストを一切含めないこと
   - "#### タイトル" のような深い階層は作成しないこと
   - 番号付けは不要、階層は "#", "##", "###" のみ使用すること

8. **内容の質**：
   - 各行はタイトル、セクション、サブセクション、引用番号のいずれかで、それ以外の情報を記載してはならない
   - 中学生・高校生が理解しやすい、実践的な内容を心がけること
   - 英語学習の基礎から応用まで、段階的に理解できる構成にする

【修正が必要なアウトライン例】

```
# Gerunds in English Language Learning    // 英語タイトルはNG
## Understanding Gerunds    // 英語セクション名はNG
### Definition and Characteristics    // 英語サブセクション名はNG
[4][67]
このサブセクションでは...    // 説明文など要求していない不要な行は削除
### Differences Between Gerunds and Infinitives    // 英語サブセクション名はNG
[30][28][1][27][102]
## セクション2
[2][24][29][11][4]    // セクション自体に引用がついている
### サブセクション1
### サブセクション: yyy    // 「サブセクション: 」という修飾はNG
[2][24][51]
### サブセクション3
[29][11][4][156]     // 存在しない引用番号を使用している
```

【修正後のアウトライン例】

```
# 動名詞の完全ガイド
## 動名詞とは
### 基本的な形と意味
[4][67]
### 不定詞との違い
[30][28][1][27][102]
## 使い方のポイント
### 主語として使う場合
[2][24][29]
### 目的語として使う場合
[11][4][51]
## よくある間違い
### 不定詞との混同
[29][11][4]
```
"""  # noqa: E501

    outline = dspy.InputField(desc="Input outline", format=str)
    fixed_outline = dspy.OutputField(desc="Corrected outline", format=str)


class SubsectionOutline(BaseModel):
    title: str
    reference_ids: list[int]
    keywords: list[str] = []  # 新規追加: キーワードリスト

    def to_text(self) -> str:
        text = f"### {self.title}\n"
        if self.reference_ids:
            text += f"[{']['.join(map(str, self.reference_ids))}]\n"
        if self.keywords:  # 新規追加: キーワード表示
            text += f"**キーワード**: [{', '.join(self.keywords)}]\n"
        return text


class SectionOutline(BaseModel):
    title: str
    subsection_outlines: list[SubsectionOutline]

    def to_text(self) -> str:
        return "\n".join(
            ["## " + self.title] + [subsection_outline.to_text() for subsection_outline in self.subsection_outlines]
        )


class Outline(BaseModel):
    title: str
    section_outlines: list[SectionOutline]

    def to_text(self) -> str:
        return "\n".join(
            ["# " + self.title] + [section_outline.to_text() for section_outline in self.section_outlines]
        )


class OutlineCreater(dspy.Module):
    def __init__(self, lm) -> None:
        self.lm = lm
        self.gen_outline = dspy.Predict(CreateOutline)
        self.fix_outline = dspy.Predict(FixOutline)

    @staticmethod
    def __parse_outline(outline) -> Outline:
        report_title = None
        section_title = None
        subsection_title = None
        section_outlines = []
        subsection_outlines = []
        reference_ids = []
        for line in outline.splitlines():
            if not line.strip():
                continue
            elif line.startswith("# "):
                assert report_title is None
                report_title = line[2:].strip()
                continue
            elif line.startswith("## "):
                if section_title is not None:
                    assert len(subsection_outlines) > 0
                    section_outlines.append(
                        SectionOutline(title=section_title, subsection_outlines=subsection_outlines)
                    )  # noqa: E501
                section_title = line[3:].strip()
                subsection_outlines = []
                continue
            elif line.startswith("### "):
                if subsection_title is not None:
                    subsection_outlines.append(SubsectionOutline(title=subsection_title, reference_ids=reference_ids))
                subsection_title = line[4:].strip()
                reference_ids = []
                continue
            else:
                assert subsection_title is not None
                assert re.match(r"\[\d+\]+", line)
                reference_ids = [int(matched) for matched in re.findall(r"\[(\d+)\]", line)]
                subsection_outlines.append(SubsectionOutline(title=subsection_title, reference_ids=reference_ids))
                subsection_title = None
                reference_ids = []
                continue
        if subsection_title:
            assert section_title is not None
            subsection_outlines.append(SubsectionOutline(title=subsection_title, reference_ids=reference_ids))
            section_outlines.append(SectionOutline(title=section_title, subsection_outlines=subsection_outlines))
        assert report_title is not None
        return Outline(title=report_title, section_outlines=section_outlines)

    def forward(self, query: str, topics: list, references: list[str]) -> dspy.Prediction:
        topics_text = "\n".join([f"- {topic}" for topic in topics])
        
        # Convert references to text if they are dictionaries
        if references and isinstance(references[0], dict):
            references_text = "\n\n".join([
                f"Title: {ref.get('title', '')}\nURL: {ref.get('url', '')}\nContent: {ref.get('snippet', '')}"
                for ref in references
            ])
        else:
            references_text = "\n\n".join(references)
        
        with dspy.settings.context(lm=self.lm):
            create_outline_result = self.gen_outline(
                query=query,
                topics=topics_text,
                references=references_text,
            )
            logger.info(f"created outline: \n{create_outline_result.outline}")
            fix_outline_result = self.fix_outline(outline=create_outline_result.outline)
            logger.info(f"fixed outline: \n{fix_outline_result.fixed_outline}")
            parsed_outline = self.__parse_outline(fix_outline_result.fixed_outline)
            
            # 新規追加: キーワード抽出
            if references and isinstance(references[0], dict):
                self._add_keywords_to_outline(parsed_outline, references)
                logger.info("Keywords extracted and added to outline")
        
        return dspy.Prediction(outline=parsed_outline)
    
    def _add_keywords_to_outline(self, outline: Outline, references: list[dict]) -> None:
        """アウトラインの各サブセクションにキーワードを追加"""
        for section in outline.section_outlines:
            for subsection in section.subsection_outlines:
                keywords = extract_keywords_from_references(references, subsection)
                subsection.keywords = keywords 