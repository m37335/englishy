import re
from typing import List, Dict, Optional, Tuple
from .grammar_dictionary import get_grammar_dictionary


class EnglishExtractor:
    """ユーザークエリから英文を抽出し、文法解析を行うクラス"""
    
    def __init__(self):
        self.grammar_dict = get_grammar_dictionary()
    
    def extract_english_from_query(self, query: str) -> List[str]:
        """クエリから英文を抽出"""
        # 英文のパターンを検出（引用符内、括弧内、または独立した英文）
        english_patterns = [
            r'"([^"]*[A-Za-z][^"]*)"',  # ダブルクォート内
            r"'([^']*[A-Za-z][^']*)'",  # シングルクォート内
            r'（([^）]*[A-Za-z][^）]*)）',  # 日本語括弧内
            r'\(([^)]*[A-Za-z][^)]*)\)',  # 英語括弧内
            r'\b[A-Z][a-z]+(?:\s+[a-z]+)*\b',  # 大文字で始まる英文
        ]
        
        extracted_english = []
        for pattern in english_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if self._is_valid_english(match):
                    extracted_english.append(match.strip())
        
        return list(set(extracted_english))  # 重複を除去
    
    def _is_valid_english(self, text: str) -> bool:
        """有効な英文かどうかを判定"""
        # 基本的な英文構造のチェック
        words = text.split()
        if len(words) < 2:  # 最低2語以上
            return False
        
        # 英単語が含まれているかチェック
        english_words = 0
        for word in words:
            if re.match(r'^[A-Za-z]+$', word):
                english_words += 1
        
        return english_words >= len(words) * 0.7  # 70%以上が英単語
    
    def analyze_grammar_structures(self, english_texts: List[str]) -> Dict[str, any]:
        """英文から文法構造を解析"""
        all_structures = []
        all_topics = []
        grammar_details = []
        
        for text in english_texts:
            # 個別の文法構造を検出
            structures = self._detect_grammar_structures(text)
            all_structures.extend(structures)
            
            # GrammarDictionaryから関連項目を検索
            for structure in structures:
                related_items = self.grammar_dict.search_by_keyword(structure)
                if related_items:
                    all_topics.extend([item.get('title', '') for item in related_items[:2]])
                    grammar_details.append({
                        'text': text,
                        'structure': structure,
                        'details': related_items[0]
                    })
        
        return {
            'grammar_structures': list(set(all_structures)),
            'related_topics': list(set(all_topics)),
            'grammar_details': grammar_details,
            'english_texts': english_texts
        }
    
    def _detect_grammar_structures(self, text: str) -> List[str]:
        """個別の英文から文法構造を検出"""
        structures = []
        
        # 仮定法過去の検出
        if re.search(r'\bI\s+wish\s+I\s+were\b', text, re.IGNORECASE):
            structures.append('仮定法過去')
        elif re.search(r'\bif\s+\w+\s+\w+ed\b.*\bwould\b', text, re.IGNORECASE):
            structures.append('仮定法過去')
        
        # 現在完了形の検出
        if re.search(r'\b(have|has)\s+\w+ed\b', text, re.IGNORECASE):
            structures.append('現在完了形')
        
        # 現在進行形の検出
        if re.search(r'\b(am|is|are)\s+\w+ing\b', text, re.IGNORECASE):
            structures.append('現在進行形')
        
        # 過去進行形の検出
        if re.search(r'\b(was|were)\s+\w+ing\b', text, re.IGNORECASE):
            structures.append('過去進行形')
        
        # 不定詞の検出
        if re.search(r'\bto\s+\w+\b', text, re.IGNORECASE):
            structures.append('不定詞')
        
        # 動名詞の検出
        if re.search(r'\b\w+ing\b', text, re.IGNORECASE):
            structures.append('動名詞')
        
        # 関係代名詞の検出
        if re.search(r'\b(who|which|that|whose)\b', text, re.IGNORECASE):
            structures.append('関係代名詞')
        
        # 受動態の検出
        if re.search(r'\b(am|is|are|was|were)\s+\w+ed\b', text, re.IGNORECASE):
            structures.append('受動態')
        
        # 助動詞の検出
        if re.search(r'\b(can|could|will|would|should|must|may|might)\b', text, re.IGNORECASE):
            structures.append('助動詞')
        
        return structures
    
    def generate_search_query(self, grammar_analysis: Dict) -> str:
        """文法解析結果から英語の検索クエリを生成"""
        english_texts = grammar_analysis.get('english_texts', [])
        grammar_structures = grammar_analysis.get('grammar_structures', [])
        
        # 英文をそのまま使用
        if english_texts:
            primary_query = english_texts[0]
        else:
            return ""
        
        # 文法構造を英語に変換して追加
        grammar_terms = []
        for structure in grammar_structures:
            english_term = self._translate_grammar_to_english(structure)
            if english_term:
                grammar_terms.append(english_term)
        
        # クエリを組み立て
        if grammar_terms:
            enhanced_query = f"{primary_query} {', '.join(grammar_terms)}"
        else:
            enhanced_query = primary_query
        
        return enhanced_query
    
    def _translate_grammar_to_english(self, japanese_grammar: str) -> Optional[str]:
        """日本語の文法用語を英語に変換"""
        grammar_translations = {
            '仮定法過去': 'subjunctive mood',
            '現在完了形': 'present perfect tense',
            '現在進行形': 'present continuous tense',
            '過去進行形': 'past continuous tense',
            '不定詞': 'infinitive',
            '動名詞': 'gerund',
            '関係代名詞': 'relative pronoun',
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
            '代名詞': 'pronoun'
        }
        
        return grammar_translations.get(japanese_grammar)
    
    def process_query(self, query: str) -> Dict[str, any]:
        """クエリを処理して英文抽出と文法解析を実行"""
        # 英文を抽出
        english_texts = self.extract_english_from_query(query)
        
        if not english_texts:
            return {
                'english_texts': [],
                'grammar_structures': [],
                'related_topics': [],
                'grammar_details': [],
                'search_query': query,  # 元のクエリをそのまま使用
                'has_english': False
            }
        
        # 文法構造を解析
        grammar_analysis = self.analyze_grammar_structures(english_texts)
        
        # 検索クエリを生成
        search_query = self.generate_search_query(grammar_analysis)
        
        return {
            'english_texts': english_texts,
            'grammar_structures': grammar_analysis['grammar_structures'],
            'related_topics': grammar_analysis['related_topics'],
            'grammar_details': grammar_analysis['grammar_details'],
            'search_query': search_query,
            'has_english': True
        }


# シングルトンインスタンス
_english_extractor = None

def get_english_extractor() -> EnglishExtractor:
    """EnglishExtractorのシングルトンインスタンスを取得"""
    global _english_extractor
    if _english_extractor is None:
        _english_extractor = EnglishExtractor()
    return _english_extractor 