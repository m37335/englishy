import re
from typing import List, Dict, Optional, Tuple
from .grammar_dictionary import get_grammar_dictionary


class GrammarAnalyzer:
    """英文法構造解析と関連項目抽出を行うクラス"""
    
    def __init__(self):
        self.grammar_dict = get_grammar_dictionary()
        self.grammar_en_map = {
            '現在進行形': 'present continuous',
            '過去進行形': 'past continuous',
            '現在完了形': 'present perfect',
            '現在完了進行形': 'present perfect continuous',
            '不定詞': 'infinitive',
            '動名詞': 'gerund',
            '関係代名詞': 'relative pronoun',
            '仮定法': 'subjunctive mood',
            '受動態': 'passive voice',
            '助動詞': 'modal verb',
            'be動詞': 'be verb',
            '一般動詞': 'regular verb',
            '過去形': 'past tense',
            '現在形': 'present tense',
            '未来形': 'future tense',
            '比較級': 'comparative',
            '最上級': 'superlative',
            '前置詞': 'preposition',
            '接続詞': 'conjunction',
            '副詞': 'adverb',
            '形容詞': 'adjective',
            '名詞': 'noun',
            '代名詞': 'pronoun',
            '重文': 'compound sentence',
            '複文': 'complex sentence',
            '三単現': 'third person singular',
            '否定文': 'negative sentence',
            '疑問文': 'interrogative sentence',
            '命令文': 'imperative sentence',
            '感嘆文': 'exclamatory sentence',
            '倒置': 'inversion',
            '関係副詞': 'relative adverb',
            '関係代名詞節': 'relative clause',
            '分詞構文': 'participial construction',
            '仮定法過去': 'subjunctive mood',
            '仮定法過去完了': 'past perfect subjunctive',
            '直接話法': 'direct speech',
            '間接話法': 'indirect speech',
        }
    
    def analyze_text(self, text: str) -> Dict[str, any]:
        """テキストの文法構造を解析"""
        # 英文を抽出
        english_sentences = self._extract_english_sentences(text)
        
        analysis_result = {
            'grammar_structures': [],
            'related_topics': [],
            'difficulty_level': 'intermediate',
            'key_points': []
        }
        
        for sentence in english_sentences:
            sentence_analysis = self._analyze_sentence(sentence)
            analysis_result['grammar_structures'].extend(sentence_analysis['structures'])
            analysis_result['related_topics'].extend(sentence_analysis['topics'])
            analysis_result['key_points'].extend(sentence_analysis['points'])
        
        # 重複を除去
        grammar_structures_ja = list(set(analysis_result['grammar_structures']))
        # 日本語→英語変換
        grammar_structures_en = [self.grammar_en_map.get(s, s) for s in grammar_structures_ja]
        analysis_result['grammar_structures'] = grammar_structures_en
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
        """個別の文を解析"""
        structures = []
        topics = []
        points = []
        
        # 文法構造の検出
        structures.extend(self._detect_grammar_structures(sentence))
        
        # 関連トピックの抽出
        topics.extend(self._extract_related_topics(sentence))
        
        # 重要なポイントの抽出
        points.extend(self._extract_key_points(sentence))
        
        return {
            'structures': structures,
            'topics': topics,
            'points': points
        }
    
    def _detect_grammar_structures(self, sentence: str) -> List[str]:
        """文法構造を検出"""
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
    
    def _extract_related_topics(self, sentence: str) -> List[str]:
        """関連トピックを抽出"""
        topics = []
        
        # 検出された文法構造に関連するトピックを検索
        structures = self._detect_grammar_structures(sentence)
        for structure in structures:
            # GrammarDictionaryから関連項目を検索
            related_items = self.grammar_dict.search_by_keyword(structure)
            for item in related_items[:2]:  # 上位2件まで
                topics.append(item.get('title', ''))
        
        return topics
    
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
        items = self.grammar_dict.search_by_keyword(grammar_structure)
        if not items:
            return None
        
        best_match = items[0]
        return best_match.get('content', '')
    
    def get_learning_path(self, grammar_structures: List[str]) -> List[Dict]:
        """学習パスを生成"""
        learning_path = []
        
        for structure in grammar_structures:
            # 基礎から応用への順序を決定
            if structure in ['現在形', '過去形', 'be動詞']:
                level = 'basic'
            elif structure in ['現在進行形', '過去進行形', '現在完了形']:
                level = 'intermediate'
            elif structure in ['仮定法', '関係代名詞', '不定詞']:
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