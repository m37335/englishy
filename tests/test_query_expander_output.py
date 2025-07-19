"""
QueryExpanderの実際の出力を確認するテストスクリプト
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai.query_expander import QueryExpander
from utils.lm import load_lm


def test_query_expander_output():
    """QueryExpanderの実際の出力をテストする"""
    
    print("🚀 QueryExpander出力テスト開始")
    print("=" * 50)
    
    try:
        # LMを初期化
        print("📡 LM初期化中...")
        lm = load_lm()
        print("✅ LM初期化完了")
        
        # QueryExpanderを初期化
        print("🔧 QueryExpander初期化中...")
        expander = QueryExpander(lm=lm)
        print("✅ QueryExpander初期化完了")
        
        # テストケース
        test_cases = [
            "仮定法過去について",
            "受動態の使い方を教えて",
            "If I had known, I would have helped you. の文法構造",
            "英語の学習方法について",
            "現在完了進行形の例文"
        ]
        
        for i, query in enumerate(test_cases, 1):
            print(f"\n📝 テストケース {i}: {query}")
            print("-" * 40)
            
            try:
                # QueryExpanderを実行
                result = expander.forward(query=query)
                
                print(f"🔍 生成された検索トピック数: {len(result.topics)}")
                print("📋 検索トピック:")
                for j, topic in enumerate(result.topics, 1):
                    print(f"  {j}. {topic}")
                
            except Exception as e:
                print(f"❌ エラー: {e}")
                import traceback
                print(f"詳細: {traceback.format_exc()}")
        
        print("\n" + "=" * 50)
        print("✅ QueryExpander出力テスト完了")
        
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        import traceback
        print(f"詳細: {traceback.format_exc()}")


if __name__ == "__main__":
    test_query_expander_output() 