import json
import os
from typing import Dict, List, Optional
import openai


class LLMGrammarAnalyzer:
    """LLMを使用した英文法解析クラス"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def analyze_text(self, text: str) -> Dict[str, any]:
        """テキストの文法構造をLLMで解析"""
        prompt = f"""Analyze the following English sentence(s) and extract grammar information.

Input text: {text}

Please respond with ONLY a JSON object in the following format:
{{
    "grammar_structures": ["structure1", "structure2"],
    "related_topics": ["topic1", "topic2"],
    "key_points": ["point1", "point2"]
}}

Grammar structures should include specific grammar points like "subjunctive mood", "passive voice", "relative clause", etc.
Related topics should include broader grammar areas that could be studied.
Key points should be concise learning points for English learners.

JSON response:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=512
            )
            
            # レスポンスからJSONを抽出
            content = response.choices[0].message.content.strip()
            print(f"Raw LLM response: {content}")
            
            # JSON部分を抽出（```json ... ``` の形式を想定）
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
            elif "```" in content:
                # 通常のコードブロック
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
            else:
                # JSON部分が見つからない場合は全体をパース
                json_str = content
            
            result = json.loads(json_str)
            return result
            
        except Exception as e:
            # エラー時は基本的な構造を返す
            return {
                "grammar_structures": [],
                "related_topics": [],
                "key_points": [],
                "error": str(e)
            } 