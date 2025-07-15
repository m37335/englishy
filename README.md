# Englishy - AI-Powered English Learning Report Generator

Englishyは、AIを活用した英語学習支援システムです。ユーザーの質問に対して、Web検索とAI分析を組み合わせて包括的な英語学習レポートを自動生成します。

## 🚀 主な機能

- **AI駆動レポート生成**: 英語学習に関する質問から包括的なレポートを自動生成
- **Web検索統合**: DuckDuckGo検索エンジンを使用した最新情報の取得
- **Streamlit UI**: 直感的なWebインターフェース
- **Docker対応**: 簡単なセットアップとデプロイ
- **モジュラー設計**: 拡張可能なAIモジュール構成

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
│   ├── query_refiner.py   # クエリ改善
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

## 🔄 処理フロー

1. **クエリ改善**: ユーザーの質問を検索最適化
2. **Web検索**: 関連情報の自動取得
3. **アウトライン生成**: レポート構造の自動設計
4. **レポート執筆**: AIによる包括的な内容生成
5. **マインドマップ**: 視覚的な学習マップ作成

## 🧪 テスト

個別モジュールのテスト：

```bash
# 全モジュールテスト
python test_individual_modules.py

# Docker内でのテスト
docker-compose exec englishy python test_individual_modules.py
```

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
2. `src/app/research.py`でモジュールを統合
3. テストを追加

## 📊 現在の状況

- ✅ **安定動作**: Docker環境でエラーなく動作確認済み
- ✅ **全モジュール統合**: AIパイプラインが完全に機能
- ✅ **Streamlit UI**: 直感的なインターフェース
- ✅ **Web検索**: DuckDuckGo統合で最新情報取得
- 🔄 **継続改善**: 文法辞書統合などの機能拡張予定

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