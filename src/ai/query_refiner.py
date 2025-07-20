import dspy
import json
import os
from typing import Dict, List, Any
# 追加: 共通ユーティリティのimport
from .grammar_utils import extract_grammar_labels, translate_to_english_grammar

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
        
        # Remove global dspy.settings.configure call to avoid thread conflicts
        
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
    
    def forward(self, text: str) -> dspy.Prediction:
        """Refine query using grammar-aware analysis."""
        try:
            # Use context manager instead of global configuration
            with dspy.settings.context(lm=self.lm):
                # Analyze grammar structures in the query
                grammar_analysis = self.grammar_analyzer(text=text)
                
                # Extract grammar structures and create refined query
                grammar_structures = grammar_analysis.get("grammar_structures", [])
                grammar_text = ", ".join(grammar_structures) if grammar_structures else "general English"
                
                # Create refined query with grammar context
                refined_query = f"{text} (grammar focus: {grammar_text})"
                
                return dspy.Prediction(refined_query=refined_query)
                
        except Exception as e:
            print(f"Error in grammar-aware refinement: {e}")
            # Fallback to simple return
            return dspy.Prediction(refined_query=text)
    
    def _analyze_grammar(self, text: str) -> Dict[str, Any]:
        """Analyze grammar structures in the given text using LM and GrammarDictionary."""
        # grammar_utilsの共通関数で主要文法項目を抽出
        grammar_structures = extract_grammar_labels(text)
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
        """日本語文法語→英語ラベル変換（共通関数利用）"""
        return translate_to_english_grammar(japanese_text)
    
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
    実践的な学習内容を重視し、学習指導要領との整合性を考慮してください。
    """
    query = dspy.InputField(desc="ユーザーのクエリ")
    refined_query = dspy.OutputField(desc="Web検索に最適化された改善されたクエリ")

class QueryRefiner:
    """Legacy QueryRefiner for backward compatibility."""
    def __init__(self, lm=None):
        self.lm = lm
        # Use the new GrammarAwareQueryRefiner internally
        self.grammar_aware_refiner = GrammarAwareQueryRefiner(lm)
        
        # Remove global dspy.settings.configure call to avoid thread conflicts
    
    def refine(self, query: str) -> str:
        """Refine query using grammar-aware analysis."""
        try:
            # Use context manager instead of global configuration
            with dspy.settings.context(lm=self.lm):
                result = self.grammar_aware_refiner(text=query)
                return result["refined_query"]
        except Exception as e:
            print(f"Error in grammar-aware refinement: {e}")
            # Fallback to simple return
            return query 