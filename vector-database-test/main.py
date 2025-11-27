import chromadb
from chromadb.config import Settings
import openai
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Chromaクライアントの初期化
client = chromadb.Client(Settings(
    anonymized_telemetry=False
))

# コレクションの作成
collection = client.create_collection(
    name="tech_articles",
    metadata={"description": "技術記事のコレクション"}
)

# サンプル文書データ
documents = [
    "Pythonは機械学習やデータ分析に広く使われるプログラミング言語です",
    "JavaScriptはWebブラウザ上で動作するスクリプト言語で、フロントエンド開発に不可欠です",
    "機械学習では、大量のデータからパターンを学習してモデルを構築します",
    "データベースは構造化されたデータを効率的に管理するためのシステムです",
    "Vector Databaseは類似度検索に特化したデータベースで、生成AIと相性が良いです"
]

# 文書IDとメタデータの準備
ids = [f"doc_{i}" for i in range(len(documents))]
metadatas = [
    {"category": "programming", "language": "Python"},
    {"category": "programming", "language": "JavaScript"},
    {"category": "AI", "topic": "machine_learning"},
    {"category": "database", "type": "general"},
    {"category": "database", "type": "vector"}
]

# 文書をコレクションに追加
collection.add(
    documents=documents,
    ids=ids,
    metadatas=metadatas
)

print("文書の登録が完了しました!")