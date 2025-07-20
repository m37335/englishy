import dspy
import litellm


class MindMap(dspy.Signature):
    """あなたは、英語学習教材の専門家で、分かりやすいマインドマップを作成する信頼できるデザイナーです。
    与えられたレポートとアウトライン構造を基に、学習者が理解しやすいマインドマップを作成してください。
    
    **重要**: マインドマップは必ず日本語で作成し、文法用語も日本語に統一してください（例：gerund→動名詞、infinitive→不定詞、subjunctive→仮定法など）。
    
    マインドマップの構成要素：
    1. **メインコンセプト**: レポートの中心的な学習項目
    2. **文法ポイント**: 関連する文法構造とルール
    3. **学習のポイント**: 重要な学習目標と概念
    4. **実践活動**: 練習問題とアクティビティ
    5. **よくある間違い**: 学習者が陥りやすい間違いと解決策
    6. **関連トピック**: 発展的な学習項目
    7. **キーワード**: 重要な学習キーワードの統合
    
    マインドマップの構造例：
    ```
    # 仮定法過去の完全ガイド
    ## 1. 基本概念
    ### 仮定法過去とは
    ### 基本的な形と意味
    ### 使用場面と例文
    ## 2. 文法ポイント
    ### 時制の特徴
    ### 仮定法過去の作り方
    ### 他の法との違い
    ## 3. 学習のポイント
    ### 重要な学習項目
    ### 理解すべき概念
    ### 練習のコツ
    ## 4. 実践活動
    ### 練習問題
    ### 会話練習
    ### 作文練習
    ## 5. よくある間違い
    ### 典型的な間違い
    ### 解決策と対策
    ### 注意点
    ## 6. 関連トピック
    ### 発展学習
    ### 他の仮定法
    ### 応用表現
    ## 7. キーワード
    ### 重要語彙
    ### 学習ポイント
    ### 参考資料
    ```
    
    作成時の注意点：
    - 階層構造を明確にし、学習の流れを自然にする
    - キーワードを適切に配置し、学習効果を高める
    - 実践的な内容を重視し、学習者が活用できる構成にする
    - 関連トピックとのつながりを明確に示す
    - 日本語の文法用語を統一し、理解しやすくする
    - **可読性の向上**: ###レベルは最大3つまでとし、深すぎる階層を避ける
    - **簡潔性の重視**: 各項目は簡潔で分かりやすい表現にする
    - **視覚的な整理**: 関連する項目をグループ化し、見やすく配置する
    """  # noqa: E501

    report = dspy.InputField(desc="レポート内容", format=str)
    outline_structure = dspy.InputField(desc="アウトライン構造", format=str)
    keywords = dspy.InputField(desc="重要なキーワード", format=str)
    related_topics = dspy.InputField(desc="関連する文法トピック", format=str)
    mindmap = dspy.OutputField(desc="レポートとアウトライン構造を基に作成されたマインドマップ", format=str)


import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class MindMapMaker(dspy.Module):
    def __init__(self, lm) -> None:
        self.lm = lm
        self.make_mindmap = dspy.Predict(MindMap)

    def forward(
        self, 
        report: str, 
        outline_structure: Optional[Dict] = None,
        keywords: Optional[List[str]] = None,
        related_topics: str = ""
    ) -> dspy.Prediction:
        """
        レポートとアウトライン構造を基にマインドマップを生成
        
        Args:
            report: レポート内容
            outline_structure: アウトライン構造（Outlineオブジェクト）
            keywords: 重要なキーワードリスト
            related_topics: 関連する文法トピック
            
        Returns:
            dspy.Prediction: マインドマップ生成結果
        """
        # アウトライン構造をテキストに変換
        outline_text = ""
        if outline_structure:
            outline_text = self._convert_outline_to_text(outline_structure)
        
        # キーワードをテキストに変換
        keywords_text = ""
        if keywords:
            keywords_text = ", ".join(keywords)
        
        with dspy.settings.context(lm=self.lm):
            mindmap_result = self.make_mindmap(
                report=report,
                outline_structure=outline_text,
                keywords=keywords_text,
                related_topics=related_topics
            )
            logger.info(f"Generated mindmap with {len(keywords) if keywords else 0} keywords")
        
        return mindmap_result
    
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
                            
                            # キーワード
                            if hasattr(subsection, 'keywords') and subsection.keywords:
                                text_parts.append(f"      キーワード: {', '.join(subsection.keywords)}")
            
            result = "\n".join(text_parts)
            if not result.strip():
                return "アウトライン構造の変換に失敗しました"
            return result
            
        except Exception as e:
            logger.warning(f"Failed to convert outline to text: {e}")
            return "アウトライン構造の変換に失敗しました" 