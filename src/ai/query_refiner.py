import dspy
import json
import os
from typing import Dict, List, Any

class GrammarAnalysisSignature(dspy.Signature):
    """
    Analyze the grammar structures present in the given English text.
    Identify specific grammar patterns, verb forms, sentence structures, and grammatical concepts.
    Focus on identifying key grammar points that would be useful for English language learning.
    """
    text = dspy.InputField(desc="English text to analyze for grammar structures")
    grammar_structures = dspy.OutputField(desc="List of detected grammar structures (e.g., 'subjunctive mood', 'gerund', 'past perfect', 'relative clause')")
    verb_forms = dspy.OutputField(desc="List of verb forms and tenses identified (e.g., 'present perfect', 'past continuous', 'modal verbs')")
    sentence_patterns = dspy.OutputField(desc="List of sentence patterns and structures (e.g., 'conditional sentence', 'passive voice', 'inversion')")

class GrammarAwareQueryRefiner(dspy.Module):
    """
    Grammar-aware query refiner that analyzes grammar structures, translates to English,
    and generates optimized search queries using GrammarDictionary data.
    """
    
    def __init__(self, lm=None):
        super().__init__()
        self.lm = lm
        self.grammar_data = self._load_grammar_dictionary()
        self.grammar_analyzer = dspy.Predict(GrammarAnalysisSignature, lm=self.lm)
        
        # Set LM globally for dspy if available
        if lm is not None:
            dspy.settings.configure(lm=lm)
        
    def _load_grammar_dictionary(self) -> Dict[str, Any]:
        """Load GrammarDictionary data from JSON file."""
        try:
            grammar_file = os.path.join("data", "GrammarDictionary", "english_grammar_data.json")
            if os.path.exists(grammar_file):
                with open(grammar_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"Warning: GrammarDictionary file not found at {grammar_file}")
                return []
        except Exception as e:
            print(f"Error loading GrammarDictionary: {e}")
            return []
    
    def forward(self, text: str) -> Dict[str, Any]:
        """
        Process query through grammar analysis, translation, and search query generation.
        
        Args:
            text: User's input query (can be Japanese or English)
            
        Returns:
            Dict containing:
            - refined_query: Optimized English search query
            - detected_grammar: List of detected grammar structures
            - related_items: Related grammar items from dictionary
            - original_query: Original input query
            - translation: English translation if input was Japanese
        """
        
        # Step 1: Grammar Analysis
        grammar_analysis = self._analyze_grammar(text)
        
        # Step 2: Translation (if Japanese)
        translation = self._translate_to_english(text) if self._is_japanese(text) else text
        
        # Step 3: Search Query Generation
        search_query = self._generate_search_query(translation, grammar_analysis)
        
        return {
            "refined_query": search_query,
            "detected_grammar": grammar_analysis.get("grammar_structures", []),
            "related_items": grammar_analysis.get("related_items", []),
            "original_query": text,
            "translation": translation
        }
    
    def _analyze_grammar(self, text: str) -> Dict[str, Any]:
        """Analyze grammar structures in the given text using LM and GrammarDictionary."""
        grammar_structures = []
        related_items = []
        
        # First, try LM-based analysis if available
        if self.lm is not None:
            try:
                # Use LM for advanced grammar analysis
                lm_analysis = self.grammar_analyzer(text=text)  # インスタンス化して呼び出す
                
                # Extract grammar structures from LM analysis
                if hasattr(lm_analysis, 'grammar_structures'):
                    grammar_structures.extend(lm_analysis.grammar_structures)
                if hasattr(lm_analysis, 'verb_forms'):
                    grammar_structures.extend(lm_analysis.verb_forms)
                if hasattr(lm_analysis, 'sentence_patterns'):
                    grammar_structures.extend(lm_analysis.sentence_patterns)
                
            except Exception as e:
                print(f"LM-based grammar analysis failed: {e}")
        
        # フォールバック削除: LLMが使えない場合は空リストのまま
        # if not grammar_structures:
        #     grammar_structures = self._pattern_based_analysis(text)
        
        # Match detected grammar structures with GrammarDictionary
        related_items = self._match_with_grammar_dictionary(grammar_structures)
        
        return {
            "grammar_structures": list(set(grammar_structures)),
            "related_items": related_items
        }
    
    def _match_with_grammar_dictionary(self, grammar_structures: List[str]) -> List[Dict[str, Any]]:
        """Match detected grammar structures with GrammarDictionary data."""
        related_items = []
        
        for grammar_structure in grammar_structures:
            for grammar_item in self.grammar_data:
                title = grammar_item.get("title", "").lower()
                tags = grammar_item.get("tags", [])
                
                # Check if grammar structure matches dictionary entry
                if (grammar_structure.lower() in title or 
                    title in grammar_structure.lower() or
                    any(tag.lower() in grammar_structure.lower() for tag in tags)):
                    
                    related_items.append({
                        "title": grammar_item.get("title", ""),
                        "summary": grammar_item.get("summary", ""),
                        "tags": tags,
                        "matched_structure": grammar_structure
                    })
        
        return related_items
    
    def _is_japanese(self, text: str) -> bool:
        """Check if text contains Japanese characters."""
        return any(ord(char) > 127 for char in text)
    
    def _translate_to_english(self, japanese_text: str) -> str:
        """Translate Japanese grammar terms to English (expanded version)."""
        translations = {
            # 01_文の種類
            "肯定文": "affirmative sentence",
            "否定文": "negative sentence",
            "疑問文": "interrogative sentence",
            "命令文": "imperative sentence",
            "感嘆文": "exclamatory sentence",
            "疑問詞": "wh-question",
            "5W1H": "wh-question",
            "There is are": "there is/are construction",
            "比較級": "comparative",
            "最上級": "superlative",
            "間接疑問文": "indirect question",
            "重文": "compound sentence",
            "複文": "complex sentence",

            # 02_文の要素と構造
            "文の要素": "sentence elements",
            "SVOCM": "SVOCM",
            "5文型": "five sentence patterns",
            "句": "phrase",
            "節": "clause",

            # 03_品詞の働き
            "動詞": "verb",
            "be動詞": "be verb",
            "一般動詞": "regular verb",
            "三人称単数現在形": "third person singular",
            "三単現": "third person singular",
            "助動詞": "auxiliary verb",
            "助動詞 can": "can (auxiliary verb)",
            "助動詞 (must, have to, may, should)": "must/have to/may/should (auxiliary verbs)",
            "動詞の原形": "base form of verb",
            "過去分詞": "past participle",
            "名詞": "noun",
            "名詞の複数形": "plural noun",
            "代名詞": "pronoun",
            "主格": "nominative case",
            "目的格": "objective case",
            "補語": "complement",
            "形容詞": "adjective",
            "副詞": "adverb",
            "前置詞": "preposition",
            "forとsinceの使い分け": "for/since usage",
            "by": "by (preposition)",
            "冠詞": "article",
            "接続詞": "conjunction",
            "接続詞 (when, because, if, that)": "when/because/if/that (conjunction)",
            "関係代名詞": "relative pronoun",

            # 04_動詞の活用
            "現在形": "present tense",
            "過去形": "past tense",
            "現在進行形": "present continuous",
            "過去進行形": "past continuous",
            "未来形": "future tense",
            "未来形 (will / be going to)": "future tense (will / be going to)",
            "現在完了形": "present perfect",
            "現在完了進行形": "present perfect continuous",
            "受け身": "passive voice",
            "受動態": "passive voice",
            "仮定法過去": "subjunctive mood",

            # 05_準動詞
            "不定詞の名詞的用法": "infinitive (noun use)",
            "不定詞の副詞的用法": "infinitive (adverb use)",
            "不定詞の形容詞的用法": "infinitive (adjective use)",
            "動名詞": "gerund",
            "分詞": "participle",
            "分詞の形容詞的用法": "participle (adjective use)",
        }
        # キーを長い順にreplaceし、部分一致誤変換を防ぐ
        for jp in sorted(translations, key=len, reverse=True):
            en = translations[jp]
            japanese_text = japanese_text.replace(jp, en)
        return japanese_text
    
    def _generate_search_query(self, english_text: str, grammar_analysis: Dict[str, Any]) -> str:
        """Generate optimized search query for web search."""
        grammar_structures = grammar_analysis.get("grammar_structures", [])
        
        # Create search query combining original text and grammar structures
        search_terms = [english_text]
        
        # Add grammar-specific search terms
        for grammar in grammar_structures:
            if grammar == "仮定法過去":
                search_terms.extend(["subjunctive mood", "I wish", "if I were"])
            elif grammar == "動名詞":
                search_terms.extend(["gerund", "ing form", "verb + ing"])
            elif grammar == "不定詞":
                search_terms.extend(["infinitive", "to + verb"])
            elif grammar == "過去形":
                search_terms.extend(["past tense", "simple past"])
            elif grammar == "現在形":
                search_terms.extend(["present tense", "simple present"])
            elif grammar == "受動態":
                search_terms.extend(["passive voice", "passive form"])
            elif grammar == "完了形":
                search_terms.extend(["perfect tense", "have + past participle"])
            elif grammar == "進行形":
                search_terms.extend(["progressive tense", "continuous form"])
            elif grammar == "比較級":
                search_terms.extend(["comparative", "comparison"])
            elif grammar == "最上級":
                search_terms.extend(["superlative", "superlative form"])
            elif grammar == "関係代名詞":
                search_terms.extend(["relative pronoun", "relative clause"])
            elif grammar == "助動詞":
                search_terms.extend(["modal verb", "auxiliary verb"])
        
        # Combine terms for optimal search
        if len(search_terms) > 1:
            # Use the most specific grammar term + original query
            return f"{search_terms[1]} {search_terms[0]}"
        else:
            return search_terms[0]

# Legacy classes for backward compatibility
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
    """Legacy QueryRefiner for backward compatibility."""
    def __init__(self, lm=None):
        self.lm = lm
        # Use the new GrammarAwareQueryRefiner internally
        self.grammar_aware_refiner = GrammarAwareQueryRefiner(lm)
        
        # Set LM globally for dspy if available
        if lm is not None:
            dspy.settings.configure(lm=lm)
    
    def refine(self, query: str) -> str:
        """Refine query using grammar-aware analysis."""
        try:
            result = self.grammar_aware_refiner(text=query)
            return result["refined_query"]
        except Exception as e:
            print(f"Error in grammar-aware refinement: {e}")
            # Fallback to simple return
            return query 