# Gemini RAG AIアシスタント for GAS & Gemini API

これは、Google Apps Script (GAS) と Gemini API の公式ドキュメントを知識源とする、対話型のAI開発アシスタントです。
Gemini File Search API を活用したRAG（Retrieval-Augmented Generation）システムを構築し、特定の技術分野に関する正確で信頼性の高いコード生成や質問応答を実現します。

## ✨ 主な機能

- **専門知識に特化:** GASとGemini APIに関する質問に対し、公式ドキュメントに基づいた正確な回答を生成します。
- **高品質なコード生成:** 具体的な指示を与えることで、すぐに使えるコードスニペットを生成し、開発を加速させます。
- **ガードレール機能:** GASと関係ない質問には応答しないように設計されており、専門性を維持します。
- **引用元の表示:** 回答の根拠となったドキュメントの箇所を明示し、情報の信頼性を担保します。
- **知識の自動更新:** GitHub Actionsを利用して、定期的に公式ドキュメントを再取得し、知識ベースを最新の状態に保ちます。

## 🔧 仕組み

このアプリケーションは、以下のステップで構築・運用されます。

1.  **データ収集:** Pythonスクリプト (`py_wget.py`) を使い、指定されたドキュメントサイトから再帰的にHTMLファイルをダウンロードします。
2.  **データ前処理:** ダウンロードしたHTMLから、RAGに適したプレーンテキスト形式の知識ソースを生成します (`local_html2text.py`)。
3.  **知識ベースの構築:** Gemini File Search APIを使い、生成されたテキストファイルをアップロードして、ベクトル化された検索可能な「ファイル検索ストア」を構築します (`setup_rag_store.py`)。
4.  **対話インターフェース:** 構築したストアを知識源として参照し、ユーザーからの質問に答える対話型アプリケーションを実行します (`query_rag.py`)。

## 🚀 使い方

### 1. 初期設定

#### a. リポジトリのクローン
```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name```

#### b. 必要なライブラリのインストール
Python環境（3.9以上を推奨）で、以下のコマンドを実行します。
```bash
pip install -r requirements.txt
```

#### c. APIキーの設定
プロジェクトのルートディレクトリに `.env` ファイルを新規作成し、ご自身のGemini APIキーを設定します。

```
# .env
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

### 2. 知識ベース（RAGストア）の構築

このプロジェクトのAIに、知識源となるドキュメントを学習させます。この作業は**最初に一度だけ**行います。

#### a. ドキュメントのダウンロードとテキスト化
以下のスクリプトを実行し、GASとGemini APIの公式ドキュメントをダウンロードし、テキストファイルに変換します。
（この処理には数分〜数十分かかる場合があります）
```bash
python py_wget.py
python local_html2text.py
```

#### b. RAGストアの作成
次に、テキスト化されたドキュメントをGemini File Search APIにアップロードし、知識ベースを構築します。
```bash
python setup_rag_store.py
```
実行が完了すると、コンソールに `fileSearchStores/xxxxxxxx` のような**ストア名（ID）**が表示されます。このIDをコピーしておきます。

### 3. AIアシスタントの実行

いよいよAIアシスタントと対話します。

#### a. ストア名の設定
`query_rag.py` ファイルを開き、`FILE_SEARCH_STORE_NAME` の値を、先ほどコピーしたストア名に書き換えます。

```python
# query_rag.py

# ...
FILE_SEARCH_STORE_NAME = "fileSearchStores/xxxxxxxxxxxx" # ← ここを書き換える
# ...
```

#### b. アプリケーションの起動
ターミナルで以下のコマンドを実行すると、AIとの対話が始まります。
```bash
python query_rag.py
``````
GASに関する質問を入力してください (終了するには Enter のみ): 
```
GASやGemini APIに関する質問を自由に入力してください。

## 🤖 GitHub Actionsによる知識の自動更新

このリポジトリには、ドキュメントを自動で更新するためのGitHub Actionsワークフロー (`.github/workflows/update-docs.yml`) が含まれています。

- **実行タイミング:**
  - GitHubのActionsタブから手動での実行 (`workflow_dispatch`)
  - (`update-docs.yml`内の`schedule`のコメントを外せば) 定期実行も可能
- **動作内容:**
  1. `py_wget.py` と `local_html2text.py` を実行し、ドキュメントを再取得・再処理します。
  2. 生成されたファイル群に差分があれば、自動でコミット＆プッシュします。

これにより、リポジトリ内の知識ソースは常に最新の状態に保たれます。ローカルで`git pull`するだけで、最新の知識を手に入れることができます。

## 💡 今後の展望

- **知識ベースの拡張:** `py_wget.py` に新しいドキュメントサイトのURLを追加するだけで、AIの専門分野をさらに広げることが可能です（例：Google Cloud、Firebaseなど）。
- **Web UIの実装:** StreamlitやGradio、Flaskなどを使って、より使いやすいWebアプリケーション化する。
- **ストア管理の高度化:** `add_docs_to_store.py`のようなスクリプトを拡充し、既存ストアへのドキュメントの追加・削除・更新を柔軟に行えるようにする。

---
このREADMEが、あなたの素晴らしいプロジェクトの一助となれば幸いです。