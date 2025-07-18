# Englishy - AI-Powered English Learning Report Generator

Englishyは、AIを活用した英語学習支援システムです。ユーザーの質問に対して、Web検索とAI分析を組み合わせて包括的な英語学習レポートを自動生成します。

## 🚀 主な機能

- **AI駆動レポート生成**: 英語学習に関する質問から包括的なレポートを自動生成
- **Web検索統合**: DuckDuckGo検索エンジンを使用した最新情報の取得
- **Streamlit UI**: 直感的なWebインターフェース
- **Docker対応**: 簡単なセットアップとデプロイ
- **モジュラー設計**: 拡張可能なAIモジュール構成
- **共通化・ユーティリティ化**: 文法項目抽出・変換ロジックの一元管理
- **自動テスト**: Docker環境でのpytest自動テスト実行

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
├── ai/                    # AIモジュール
│   ├── grammar_utils.py   # 共通文法ユーティリティ（新規）
│   ├── query_refiner.py   # クエリ改善（共通化済み）
│   ├── grammar_analyzer.py # 文法解析
│   ├── query_expander.py  # クエリ拡張
│   ├── outline_creater.py # アウトライン生成
│   ├── mind_map_maker.py  # マインドマップ生成
│   └── stream_writer.py   # レポート執筆
├── app/                   # Streamlitアプリケーション
│   ├── app.py            # メインアプリ
│   └── research.py       # リサーチ処理
├── retriever/            # 情報検索
│   ├── web_search/       # Web検索
│   └── article_search/   # 記事検索
└── utils/                # ユーティリティ
```

### 🔄 処理フロー

1. **クエリ改善**: ユーザーの質問を検索最適化（grammar_utils.py活用）
2. **Web検索**: 関連情報の自動取得
3. **文法解析**: 文法構造の自動検出・分類（grammar_utils.py活用）
4. **アウトライン生成**: レポート構造の自動設計
5. **レポート執筆**: AIによる包括的な内容生成
6. **マインドマップ**: 視覚的な学習マップ作成

## 🧪 テスト

### 自動テスト実行

```bash
# Docker内でのテスト実行
docker-compose run --rm englishy pytest tests/ -v

# 特定モジュールのテスト
docker-compose run --rm englishy pytest tests/test_query_refiner.py -v
```

### テスト内容

- ✅ **QueryRefinerテスト**: 文法項目抽出・日本語→英語変換
- ✅ **共通化テスト**: grammar_utils.pyの動作確認
- ✅ **複数文法項目テスト**: 文中の複数文法語の同時検出

## 📝 使用例

### 入力例
```
「I wish I were better at」の使い方を教えて
```

### 出力例
- 仮定法過去の完全ガイド
- 具体的な例文と解説
- 中学生・高校生向けの指導法
- 練習問題
- 関連トピック

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

## 📊 現在の状況

- ✅ **安定動作**: Docker環境でエラーなく動作確認済み
- ✅ **全モジュール統合**: AIパイプラインが完全に機能
- ✅ **Streamlit UI**: 直感的なインターフェース
- ✅ **Web検索**: DuckDuckGo統合で最新情報取得
- ✅ **共通化完了**: QueryRefinerのgrammar_utils.py活用
- ✅ **Docker最適化**: ビルド時間短縮（1484秒→225秒）
- ✅ **テスト自動化**: pytest環境構築・全テストパス
- 🔄 **継続改善**: GrammarAnalyzer等の他モジュール共通化予定

## 🆕 最新の改善内容（2025年7月）

### 共通化・ユーティリティ化
- **grammar_utils.py新規作成**: 文法項目変換辞書・抽出関数の一元管理
- **QueryRefinerリファクタ**: 重複コード削除・共通ロジック活用
- **複数文法項目対応**: 文中の複数文法語を同時検出・変換

### Docker環境最適化
- **依存関係整理**: pyproject.tomlから不要な依存を削除
- **ビルド時間短縮**: 75%の時間短縮を実現
- **イメージ軽量化**: 最小限の依存関係で軽量なイメージ

### テスト自動化
- **pytest環境構築**: Docker環境での自動テスト実行
- **テストケース追加**: 単一・複数文法項目の変換テスト
- **継続的品質保証**: 全テストパスによる動作保証

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