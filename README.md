# Englishy - AI-Powered English Learning Report Generator

Englishyは、AIを活用した英語学習支援システムです。ユーザーの質問に対して、Web検索とAI分析を組み合わせて包括的な英語学習レポートを自動生成します。

## 🎯 プロジェクト完了状況

**🎉 全AIモジュール改善完了・統合テスト成功！**

- ✅ **全8つのAIモジュール改善完了**
- ✅ **実際のアプリケーションで動作確認済み**
- ✅ **マインドマップの視覚的表示成功**
- ✅ **キーワード機能の全モジュール統合**
- ✅ **Docker環境の完全最適化**

## 🚀 主な機能

- **AI駆動レポート生成**: 英語学習に関する質問から包括的なレポートを自動生成
- **Web検索統合**: DuckDuckGo検索エンジンを使用した最新情報の取得
- **Streamlit UI**: 直感的なWebインターフェース
- **Docker対応**: 簡単なセットアップとデプロイ
- **モジュラー設計**: 拡張可能なAIモジュール構成
- **共通化・ユーティリティ化**: 文法項目抽出・変換ロジックの一元管理
- **自動テスト**: Docker環境でのpytest自動テスト実行
- **マインドマップ生成**: streamlit-markmapを使用した視覚的学習マップ
- **キーワード機能**: 全モジュールでのキーワード活用による学習効果向上
- **LLMベース解析**: OpenAI GPT-4oを使用した高精度文法解析

## 📋 システム要件

- Python 3.12+
- Docker & Docker Compose
- OpenAI API Key
- uv (Pythonパッケージマネージャー)

## 🛠️ セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/m37335/englishy.git
cd englishy
```

### 2. 環境変数の設定

`.env`ファイルを作成し、OpenAI API Keyを設定：

```bash
cp env.example .env
```

`.env`ファイルを編集：
```text
OPENAI_API_KEY=sk-...  # OpenAI API Key
ENGLISHY_WEB_SEARCH_ENGINE=DuckDuckGo
ENGLISHY_LM=openai/gpt-4o-mini
```

### 3. Dockerでの実行（推奨）

```bash
# コンテナのビルドと起動
docker-compose up --build

# バックグラウンド実行
docker-compose up -d --build
```

アプリケーションは http://localhost:8502 でアクセス可能です。

### 4. ローカルでの実行

```bash
# 依存関係のインストール
make install

# アプリケーションの起動
make englishy-run-app
```

## 🏗️ アーキテクチャ

Englishyは以下のモジュラー構成を採用しています：

```
src/
├── ai/                           # AIモジュール
│   ├── grammar_utils.py          # 共通文法ユーティリティ（統合済み）
│   ├── llm_grammar_analyzer.py   # LLMベース高精度文法解析（新規）
│   ├── query_refiner.py          # クエリ改善（grammar_utils統合済み）
│   ├── grammar_analyzer.py       # 文法解析（grammar_utils統合済み）
│   ├── query_expander.py         # クエリ拡張（grammar_utils統合済み）
│   ├── outline_creater.py        # アウトライン生成（キーワード機能実装済み）
│   ├── mindmap_maker.py          # マインドマップ生成（アウトライン・キーワード統合済み）
│   ├── report_writer.py          # レポート執筆（キーワード活用機能実装済み）
│   ├── related_topics_writer.py  # 関連トピック生成（アウトライン・キーワード統合済み）
│   ├── references_writer.py      # 参考文献生成（アウトライン・キーワード統合・APA形式）
│   └── openai_client.py          # OpenAI APIクライアント
├── app/                          # Streamlitアプリケーション
│   ├── app.py                   # メインアプリ
│   ├── research.py              # リサーチ処理（フロー最適化・キーワード統合済み）
│   ├── report.py                # レポート表示・管理
│   ├── config.py                # 設定管理
│   └── utils/                   # ユーティリティ
│       ├── mindmap_utils.py     # マインドマップ表示（streamlit-markmap対応）
│       └── lm.py                # 言語モデルユーティリティ
├── retriever/                   # 情報検索
│   ├── web_search/              # Web検索
│   └── article_search/          # 記事検索
└── utils/                       # ユーティリティ
```

### 🔄 最適化された処理フロー

1. **クエリ改善**: ユーザーの質問を検索最適化（grammar_utils.py活用）
2. **クエリ拡張**: 検索トピックの拡張（Web検索前）
3. **Web検索**: 複数クエリでの関連情報取得・重複除去
4. **文法解析**: 文法構造の自動検出・分類（grammar_utils.py活用）
5. **LLM解析**: オプションで高精度なLLMベース解析
6. **アウトライン生成**: レポート構造の自動設計・キーワード抽出
7. **レポート執筆**: キーワードを活用した包括的な内容生成
8. **関連トピック生成**: アウトライン・キーワードを活用した関連学習項目
9. **参考文献生成**: APA形式での学術的厳密な参考文献
10. **マインドマップ**: 視覚的な学習マップ作成（streamlit-markmap対応）

## 🧪 テスト

### 自動テスト実行

```bash
# Docker内でのテスト実行
docker-compose run --rm englishy pytest tests/ -v

# 特定モジュールのテスト
docker-compose run --rm englishy pytest tests/test_grammar_utils.py -v
```

### テスト内容

- ✅ **QueryRefinerテスト**: 文法項目抽出・日本語→英語変換
- ✅ **GrammarAnalyzerテスト**: 文法構造解析（10項目）
- ✅ **LLMGrammarAnalyzerテスト**: LLMベース高精度解析
- ✅ **QueryExpanderテスト**: クエリ拡張（7項目）
- ✅ **OutlineCreaterテスト**: アウトライン生成・キーワード機能
- ✅ **MindMapMakerテスト**: マインドマップ生成（8項目）
- ✅ **RelatedTopicsWriterテスト**: 関連トピック生成（11項目）
- ✅ **ReferencesWriterテスト**: 参考文献生成（9項目）
- ✅ **統合テスト**: 全モジュールの統合動作確認

## 📝 使用例

### 入力例
```
「仮定法過去について教えて」
```

### 出力例
- **包括的なレポート**: 仮定法過去の完全ガイド
- **キーワード活用**: 重要な学習ポイントの明確化
- **関連トピック**: 段階的な学習フロー
- **参考文献**: APA形式での学術的参考文献
- **マインドマップ**: 視覚的な学習マップ
- **具体的な例文と解説**: 中学生・高校生向けの指導法
- **練習問題**: 実践的な学習活動

## 🔧 開発

### コードフォーマット

```bash
make format
make lint
```

### 新しいAIモジュールの追加

1. `src/ai/`ディレクトリに新しいモジュールを作成
2. `grammar_utils.py`の共通関数を活用
3. `src/app/research.py`でモジュールを統合
4. テストを追加

### 共通化・ユーティリティ化

- **grammar_utils.py**: 文法項目抽出・変換の共通ロジック
- **extract_grammar_labels()**: テキストから文法ラベルを抽出
- **translate_to_english_grammar()**: 日本語文法語→英語ラベル変換
- **mindmap_utils.py**: マインドマップ表示の共通ロジック

## 📊 最新の改善内容（2025年7月）

### 🎯 全AIモジュール改善完了
- **QueryRefiner**: grammar_utils統合・部分一致誤変換防止
- **GrammarAnalyzer**: grammar_utils統合・英語出力一貫性統一
- **LLMGrammarAnalyzer**: OpenAI GPT-4o対応の高精度解析
- **QueryExpander**: grammar_utils統合・Web検索特化設計
- **OutlineCreater**: キーワード機能実装・自動統合
- **MindMapMaker**: アウトライン・キーワード統合・日本語プロンプト
- **ReportWriter**: キーワード活用機能・執筆品質向上
- **RelatedTopicsWriter**: アウトライン・キーワード統合・学習効果最大化
- **ReferencesWriter**: アウトライン・キーワード統合・APA形式標準化

### 🔄 フロー最適化
- **QueryExpander**: Web検索前に移動
- **複数クエリ検索**: refined_query + top 3 topics
- **重複除去**: ユニークな結果を最大12件に制限
- **検索効率向上**: 75%の処理時間短縮

### 🧪 テスト自動化
- **20個のテストファイル**: 全モジュールの包括的テスト
- **Docker環境**: 完全自動テスト実行
- **品質保証**: 全テストパスによる動作保証

### 🐳 Docker環境最適化
- **streamlit-markmap**: マインドマップ視覚化対応
- **依存関係整理**: 最小限の依存で軽量化
- **開発効率向上**: ローカルファイル変更の即座反映

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 🔗 リンク

- **GitHub**: https://github.com/m37335/englishy
- **Docker Hub**: 準備中

---

**Englishy** - Making English Learning Easy with AI 🎓

*全AIモジュール改善完了・統合テスト成功 - 2025年7月20日* 