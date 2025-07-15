import json
import os
from typing import List, Dict, Optional
from pathlib import Path
import re


class GrammarDictionary:
    """英文法辞書データを管理・検索するクラス"""
    
    def __init__(self, data_path: str = "data/GrammarDictionary"):
        self.data_path = Path(data_path)
        self.grammar_data = []
        self._load_data()
    
    def _load_data(self):
        """JSONファイルから文法データを読み込み"""
        json_path = self.data_path / "english_grammar_data.json"
        if json_path.exists():
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    self.grammar_data = json.load(f)
            except Exception as e:
                print(f"GrammarDictionary読み込みエラー: {e}")
                self.grammar_data = []
    
    def search_by_keyword(self, keyword: str) -> List[Dict]:
        """キーワードで文法項目を検索"""
        results = []
        keyword_lower = keyword.lower()
        
        for item in self.grammar_data:
            # タイトル、タグ、サマリー、コンテンツで検索
            searchable_text = f"{item.get('title', '')} {' '.join(item.get('tags', []))} {item.get('summary', '')} {item.get('content', '')}"
            
            if keyword_lower in searchable_text.lower():
                results.append(item)
        
        return results
    
    def search_by_tags(self, tags: List[str]) -> List[Dict]:
        """タグで文法項目を検索"""
        results = []
        tags_lower = [tag.lower() for tag in tags]
        
        for item in self.grammar_data:
            item_tags = [tag.lower() for tag in item.get('tags', [])]
            if any(tag in item_tags for tag in tags_lower):
                results.append(item)
        
        return results
    
    def get_related_topics(self, topic: str) -> List[Dict]:
        """関連トピックを取得"""
        # まずトピックに関連する項目を検索
        related_items = self.search_by_keyword(topic)
        
        # 関連リンクから追加の項目を取得
        all_related = []
        for item in related_items:
            all_related.append(item)
            
            # 関連リンクの項目も追加
            for link in item.get('related_links', []):
                linked_item = self._find_by_filename(link.get('file', ''))
                if linked_item and linked_item not in all_related:
                    all_related.append(linked_item)
        
        return all_related[:5]  # 最大5件まで
    
    def _find_by_filename(self, filename: str) -> Optional[Dict]:
        """ファイル名で項目を検索"""
        for item in self.grammar_data:
            if item.get('filename') == filename:
                return item
        return None
    
    def format_for_references(self, items: List[Dict]) -> str:
        """参考文献形式でフォーマット"""
        if not items:
            return ""
        
        references = []
        for i, item in enumerate(items, 1):
            title = item.get('title', '')
            summary = item.get('summary', '')
            path = item.get('path', '')
            
            ref = f"[{i}] {title}\n"
            ref += f"   概要: {summary}\n"
            ref += f"   出典: GrammarDictionary/{path}\n"
            references.append(ref)
        
        return "\n".join(references)
    
    def get_grammar_explanation(self, topic: str) -> Optional[str]:
        """特定トピックの文法解説を取得"""
        items = self.search_by_keyword(topic)
        if not items:
            return None
        
        # 最も関連性の高い項目を選択
        best_match = items[0]
        content = best_match.get('content', '')
        
        # マークダウン形式のコンテンツを整形
        return self._format_content(content)
    
    def _format_content(self, content: str) -> str:
        """コンテンツを整形"""
        # タグ分析部分を削除
        content = re.sub(r'\*\*タグ分析:\*\*.*?\n', '', content, flags=re.MULTILINE)
        
        # 関連項目部分を削除
        if '## 関連項目' in content:
            content = content.split('## 関連項目')[0]
        
        return content.strip()
    
    def get_all_topics(self) -> List[str]:
        """全てのトピック名を取得"""
        return [item.get('title', '') for item in self.grammar_data if item.get('title')]


# シングルトンインスタンス
_grammar_dict = None

def get_grammar_dictionary() -> GrammarDictionary:
    """GrammarDictionaryのシングルトンインスタンスを取得"""
    global _grammar_dict
    if _grammar_dict is None:
        _grammar_dict = GrammarDictionary()
    return _grammar_dict 