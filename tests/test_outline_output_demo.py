#!/usr/bin/env python3
"""
アウトライン出力確認用デモスクリプト
キーワード機能が追加されたアウトラインがどのような出力になるかを確認
"""


def extract_keywords_from_content(content: str) -> list[str]:
    """コンテンツからキーワードを抽出する（簡易版）"""
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
    """参照情報からサブセクション用のキーワードを抽出（簡易版）"""
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


class SubsectionOutline:
    """サブセクションアウトライン（簡易版）"""
    def __init__(self, title: str, reference_ids: list[int], keywords: list[str] = None):
        self.title = title
        self.reference_ids = reference_ids
        self.keywords = keywords or []
    
    def to_text(self) -> str:
        text = f"### {self.title}\n"
        if self.reference_ids:
            text += f"[{']['.join(map(str, self.reference_ids))}]\n"
        if self.keywords:
            text += f"**キーワード**: [{', '.join(self.keywords)}]\n"
        return text


class SectionOutline:
    """セクションアウトライン（簡易版）"""
    def __init__(self, title: str, subsection_outlines: list[SubsectionOutline]):
        self.title = title
        self.subsection_outlines = subsection_outlines
    
    def to_text(self) -> str:
        return "\n".join(
            ["## " + self.title] + [subsection_outline.to_text() for subsection_outline in self.subsection_outlines]
        )


class Outline:
    """アウトライン（簡易版）"""
    def __init__(self, title: str, section_outlines: list[SectionOutline]):
        self.title = title
        self.section_outlines = section_outlines
    
    def to_text(self) -> str:
        return "\n".join(
            ["# " + self.title] + [section_outline.to_text() for section_outline in self.section_outlines]
        )


def demo_keyword_extraction():
    """キーワード抽出機能のデモ"""
    print("=" * 60)
    print("🔍 キーワード抽出機能デモ")
    print("=" * 60)
    
    # サンプルコンテンツ
    sample_contents = [
        "Gerund Formation in English Grammar - Learn about gerund formation and teaching methods.",
        "Teaching English Grammar: Effective methods for infinitive and participle instruction.",
        "動名詞の指導方法と不定詞との違いについて学習します。",
        "This article covers subjunctive mood, passive voice, and modal verbs in detail."
    ]
    
    for i, content in enumerate(sample_contents, 1):
        keywords = extract_keywords_from_content(content)
        print(f"\n📝 サンプル{i}: {content[:50]}...")
        print(f"🔑 抽出キーワード: {keywords}")


def demo_outline_structure():
    """アウトライン構造のデモ"""
    print("\n" + "=" * 60)
    print("📋 アウトライン構造デモ")
    print("=" * 60)
    
    # サンプルアウトラインを作成
    subsection1 = SubsectionOutline(
        title="基本的な形と意味",
        reference_ids=[1, 2, 3],
        keywords=["gerund", "formation", "teaching"]
    )
    
    subsection2 = SubsectionOutline(
        title="不定詞との違い",
        reference_ids=[4, 5, 6],
        keywords=["infinitive", "difference", "usage"]
    )
    
    section = SectionOutline(
        title="動名詞とは",
        subsection_outlines=[subsection1, subsection2]
    )
    
    outline = Outline(
        title="動名詞の完全ガイド",
        section_outlines=[section]
    )
    
    print("📄 生成されたアウトライン:")
    print(outline.to_text())


def demo_keyword_integration():
    """キーワード統合機能のデモ"""
    print("\n" + "=" * 60)
    print("🔗 キーワード統合機能デモ")
    print("=" * 60)
    
    # サンプル参照情報
    references = [
        {
            "id": 1,
            "title": "Gerund Formation Guide",
            "snippet": "Learn about gerund formation and usage patterns in English grammar."
        },
        {
            "id": 2,
            "title": "Teaching English Grammar",
            "snippet": "Effective teaching methods for grammar instruction and practice exercises."
        },
        {
            "id": 3,
            "title": "Infinitive vs Gerund",
            "snippet": "Understanding the differences between infinitive and gerund usage."
        }
    ]
    
    # サブセクションの引用番号
    subsection_refs = [1, 2, 3]
    
    # キーワード抽出
    keywords = extract_keywords_from_references(references, subsection_refs)
    
    print("📚 参照情報:")
    for ref in references:
        print(f"  - ID {ref['id']}: {ref['title']}")
    
    print(f"\n🔑 抽出されたキーワード: {keywords}")
    
    # サブセクションにキーワードを統合
    subsection = SubsectionOutline(
        title="基本的な形と意味",
        reference_ids=subsection_refs,
        keywords=keywords
    )
    
    print(f"\n📝 キーワード統合後のサブセクション:")
    print(subsection.to_text())


def demo_complete_outline():
    """完全なアウトラインのデモ"""
    print("\n" + "=" * 60)
    print("📋 完全なアウトライン構造デモ")
    print("=" * 60)
    
    # 複数のセクションとサブセクションを含む完全なアウトライン
    subsections_section1 = [
        SubsectionOutline(
            title="基本的な形と意味",
            reference_ids=[1, 2, 3],
            keywords=["gerund", "formation", "teaching"]
        ),
        SubsectionOutline(
            title="不定詞との違い",
            reference_ids=[4, 5, 6],
            keywords=["infinitive", "difference", "usage"]
        )
    ]
    
    subsections_section2 = [
        SubsectionOutline(
            title="主語として使う場合",
            reference_ids=[1, 3, 7],
            keywords=["subject", "sentence", "structure"]
        ),
        SubsectionOutline(
            title="目的語として使う場合",
            reference_ids=[2, 4, 8],
            keywords=["object", "verb", "complement"]
        )
    ]
    
    subsections_section3 = [
        SubsectionOutline(
            title="不定詞との混同",
            reference_ids=[5, 6, 9],
            keywords=["confusion", "infinitive", "mistake"]
        ),
        SubsectionOutline(
            title="動詞の使い分け",
            reference_ids=[7, 8, 10],
            keywords=["verb", "choice", "context"]
        )
    ]
    
    sections = [
        SectionOutline(title="動名詞とは", subsection_outlines=subsections_section1),
        SectionOutline(title="使い方のポイント", subsection_outlines=subsections_section2),
        SectionOutline(title="よくある間違い", subsection_outlines=subsections_section3)
    ]
    
    complete_outline = Outline(
        title="動名詞の完全ガイド",
        section_outlines=sections
    )
    
    print("📄 完全なアウトライン（キーワード付き）:")
    print(complete_outline.to_text())


def main():
    """メイン関数"""
    print("🚀 アウトライン出力確認デモ")
    print("キーワード機能が追加されたアウトラインの出力を確認します")
    
    try:
        # 各デモを実行
        demo_keyword_extraction()
        demo_outline_structure()
        demo_keyword_integration()
        demo_complete_outline()
        
        print("\n" + "=" * 60)
        print("✅ デモ完了")
        print("=" * 60)
        print("\n📝 確認ポイント:")
        print("1. キーワードが適切に抽出されているか")
        print("2. アウトライン構造が正しく生成されているか")
        print("3. キーワードがサブセクションに統合されているか")
        print("4. 引用番号とキーワードが共存しているか")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 