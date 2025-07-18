import re
from typing import List, Dict, Optional, Tuple
from .grammar_dictionary import get_grammar_dictionary
# 共通ユーティリティをimport
from .grammar_utils import grammar_en_map, extract_grammar_labels, translate_to_english_grammar


class GrammarAnalyzer:
    """英文法構造解析と関連項目抽出を行うクラス（完全共通化版）"""
    
    def __init__(self):
        self.grammar_dict = get_grammar_dictionary()
    
    def analyze_text(self, text: str) -> Dict[str, any]:
        """テキストの文法構造を解析（grammar_utilsを活用）"""
        # 英文を抽出
        english_sentences = self._extract_english_sentences(text)
        
        analysis_result = {
            'grammar_structures': [],
            'related_topics': [],
            'difficulty_level': 'intermediate',
            'key_points': []
        }
        
        # 入力テキスト全体から文法ラベルを抽出（grammar_utils活用）
        all_grammar_labels = extract_grammar_labels(text)
        analysis_result['grammar_structures'] = all_grammar_labels
        
        for sentence in english_sentences:
            sentence_analysis = self._analyze_sentence(sentence)
            analysis_result['related_topics'].extend(sentence_analysis['topics'])
            analysis_result['key_points'].extend(sentence_analysis['points'])
        
        # 重複を除去
        analysis_result['related_topics'] = list(set(analysis_result['related_topics']))
        analysis_result['key_points'] = list(set(analysis_result['key_points']))
        
        return analysis_result
    
    def _extract_english_sentences(self, text: str) -> List[str]:
        """テキストから英文を抽出"""
        # 英文のパターンを検出（基本的な英文構造）
        english_pattern = r'[A-Z][^.!?]*[.!?]'
        sentences = re.findall(english_pattern, text)
        
        # より厳密な英文判定（主語+動詞の構造を持つもの）
        valid_sentences = []
        for sentence in sentences:
            if self._is_valid_english_sentence(sentence):
                valid_sentences.append(sentence.strip())
        
        # 文が抽出されない場合は、テキスト全体を1つの文として扱う
        if not valid_sentences and self._is_valid_english_sentence(text):
            valid_sentences.append(text.strip())
        
        return valid_sentences
    
    def _is_valid_english_sentence(self, sentence: str) -> bool:
        """有効な英文かどうかを判定"""
        # 基本的な英文構造のチェック
        words = sentence.split()
        if len(words) < 3:  # 最低3語以上
            return False
        
        # 主語+動詞の基本構造があるかチェック
        has_subject = any(word.lower() in ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'the', 'a', 'an'] 
                         for word in words[:3])
        has_verb = any(word.lower().endswith(('s', 'ed', 'ing')) or word.lower() in ['is', 'are', 'was', 'were', 'have', 'has', 'had', 'do', 'does', 'did', 'can', 'will', 'would', 'should', 'may', 'might'] 
                      for word in words)
        
        return has_subject and has_verb
    
    def _analyze_sentence(self, sentence: str) -> Dict[str, any]:
        """個別の文を解析（grammar_utilsを活用）"""
        topics = []
        points = []
        
        # 文から文法ラベルを抽出（grammar_utils活用）
        sentence_grammar_labels = extract_grammar_labels(sentence)
        
        # 関連トピックの抽出
        topics.extend(self._extract_related_topics(sentence, sentence_grammar_labels))
        
        # 重要なポイントの抽出
        points.extend(self._extract_key_points(sentence))
        
        return {
            'topics': topics,
            'points': points
        }
    
    def _extract_related_topics(self, sentence: str, grammar_labels: List[str]) -> List[str]:
        """関連トピックを抽出（grammar_utilsの結果を活用）"""
        topics = []
        
        # grammar_utilsで抽出された文法ラベルに関連するトピックを検索
        for label in grammar_labels:
            # GrammarDictionaryから関連項目を検索
            related_items = self.grammar_dict.search_by_keyword(label)
            for item in related_items[:2]:  # 上位2件まで
                topics.append(item.get('title', ''))
        
        # 従来の検出ロジックも併用（grammar_utilsで検出されない場合の補完）
        traditional_structures = self._detect_traditional_grammar_structures(sentence)
        for structure in traditional_structures:
            # 日本語→英語変換（grammar_utils活用）
            english_structure = translate_to_english_grammar(structure)
            if english_structure != structure:  # 変換された場合
                related_items = self.grammar_dict.search_by_keyword(english_structure)
                for item in related_items[:1]:  # 上位1件まで
                    topics.append(item.get('title', ''))
        
        return topics
    
    def _detect_traditional_grammar_structures(self, sentence: str) -> List[str]:
        """従来の文法構造検出（grammar_utilsの補完用）"""
        structures = []
        
        # 時制の検出
        if re.search(r'\b(am|is|are)\s+\w+ing\b', sentence, re.IGNORECASE):
            structures.append('現在進行形')
        if re.search(r'\b(was|were)\s+\w+ing\b', sentence, re.IGNORECASE):
            structures.append('過去進行形')
        if re.search(r'\b(have|has)\s+\w+ed\b', sentence, re.IGNORECASE):
            structures.append('現在完了形')
        if re.search(r'\b(have|has)\s+been\s+\w+ing\b', sentence, re.IGNORECASE):
            structures.append('現在完了進行形')
        
        # 不定詞の検出
        if re.search(r'\bto\s+\w+\b', sentence, re.IGNORECASE):
            structures.append('不定詞')
        
        # 動名詞の検出
        if re.search(r'\b\w+ing\b', sentence, re.IGNORECASE):
            structures.append('動名詞')
        
        # 関係代名詞の検出
        if re.search(r'\b(who|which|that|whose)\b', sentence, re.IGNORECASE):
            structures.append('関係代名詞')
        
        # 仮定法の検出
        if re.search(r'\bif\b.*\b(would|could|should|might)\b', sentence, re.IGNORECASE):
            structures.append('仮定法')
        
        # 受動態の検出
        if re.search(r'\b(am|is|are|was|were)\s+\w+ed\b', sentence, re.IGNORECASE):
            structures.append('受動態')
        
        return structures
    
    def _extract_key_points(self, sentence: str) -> List[str]:
        """重要なポイントを抽出"""
        points = []
        
        # 文の長さによる難易度判定
        word_count = len(sentence.split())
        if word_count > 20:
            points.append('長文読解')
        elif word_count > 15:
            points.append('中程度の文')
        else:
            points.append('短文')
        
        # 複雑な構造の検出
        if re.search(r'\b(although|because|when|while|if|unless)\b', sentence, re.IGNORECASE):
            points.append('複文')
        
        if re.search(r'\band\b.*\band\b', sentence, re.IGNORECASE):
            points.append('重文')
        
        return points
    
    def get_grammar_explanation(self, grammar_structure: str) -> Optional[str]:
        """特定の文法構造の解説を取得"""
        # grammar_utilsで英語変換を試行
        english_structure = translate_to_english_grammar(grammar_structure)
        
        items = self.grammar_dict.search_by_keyword(english_structure)
        if not items:
            return None
        
        best_match = items[0]
        return best_match.get('content', '')
    
    def get_learning_path(self, grammar_structures: List[str]) -> List[Dict]:
        """学習パスを生成（grammar_utilsの結果を活用）"""
        learning_path = []
        
        for structure in grammar_structures:
            # 基礎から応用への順序を決定
            if structure in ['present simple', 'past simple', 'be verb']:
                level = 'basic'
            elif structure in ['present continuous', 'past continuous', 'present perfect']:
                level = 'intermediate'
            elif structure in ['subjunctive mood', 'relative pronoun', 'infinitive']:
                level = 'advanced'
            else:
                level = 'intermediate'
            
            # GrammarDictionaryから詳細情報を取得
            items = self.grammar_dict.search_by_keyword(structure)
            if items:
                item = items[0]
                learning_path.append({
                    'structure': structure,
                    'level': level,
                    'title': item.get('title', ''),
                    'summary': item.get('summary', ''),
                    'related_items': [link.get('text', '') for link in item.get('related_links', [])]
                })
        
        # レベル順にソート
        level_order = {'basic': 1, 'intermediate': 2, 'advanced': 3}
        learning_path.sort(key=lambda x: level_order.get(x['level'], 2))
        
        return learning_path
    
    def format_analysis_result(self, analysis: Dict) -> str:
        """解析結果をフォーマット"""
        result = "## 文法構造解析結果\n\n"
        
        if analysis['grammar_structures']:
            result += "### 検出された文法構造\n"
            for structure in analysis['grammar_structures']:
                result += f"- {structure}\n"
            result += "\n"
        
        if analysis['related_topics']:
            result += "### 関連文法項目\n"
            for topic in analysis['related_topics']:
                result += f"- {topic}\n"
            result += "\n"
        
        if analysis['key_points']:
            result += "### 学習ポイント\n"
            for point in analysis['key_points']:
                result += f"- {point}\n"
            result += "\n"
        
        # 学習パスを生成
        learning_path = self.get_learning_path(analysis['grammar_structures'])
        if learning_path:
            result += "### 推奨学習順序\n"
            for i, item in enumerate(learning_path, 1):
                result += f"{i}. **{item['structure']}** ({item['level']})\n"
                result += f"   {item['summary']}\n"
                if item['related_items']:
                    result += f"   関連項目: {', '.join(item['related_items'][:3])}\n"
                result += "\n"
        
        return result


# シングルトンインスタンス
_grammar_analyzer = None

def get_grammar_analyzer() -> GrammarAnalyzer:
    """GrammarAnalyzerのシングルトンインスタンスを取得"""
    global _grammar_analyzer
    if _grammar_analyzer is None:
        _grammar_analyzer = GrammarAnalyzer()
    return _grammar_analyzer 