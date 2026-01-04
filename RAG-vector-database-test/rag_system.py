import chromadb
import openai
import os
from dotenv import load_dotenv
from typing import List, Dict

# 環境変数の読み込み
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class RAGSystem:
    """
    RAG(Retrieval-Augmented Generation)システム
    """
    
    def __init__(self, collection_name: str = "tech_knowledge_base"):
        """
        RAGシステムを初期化
        
        Args:
            collection_name: 使用するChromaコレクション名
        """
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_collection(name=collection_name)
        print(f"✓ コレクション '{collection_name}' を読み込みました")
    
    def get_embedding(self, text: str) -> List[float]:
        """
        テキストをベクトル化
        """
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def retrieve(self, query: str, top_k: int = 3) -> Dict:
        """
        質問に関連する文書を検索
        
        Args:
            query: ユーザーの質問
            top_k: 取得する文書数
            
        Returns:
            検索結果(文書、メタデータ、スコア)
        """
        # 質問をベクトル化
        query_embedding = self.get_embedding(query)
        
        # Vector DBから類似文書を検索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return results
    
    def generate_answer(self, query: str, context: str, model: str = "gpt-4o-mini") -> str:
        """
        コンテキストに基づいて回答を生成
        
        Args:
            query: ユーザーの質問
            context: 検索で取得したコンテキスト
            model: 使用するGPTモデル
            
        Returns:
            生成された回答
        """
        # プロンプトの構築
        system_prompt = """あなたは親切で知識豊富なAIアシスタントです。
提供されたコンテキストに基づいて、ユーザーの質問に正確に回答してください。
コンテキストに情報がない場合は、その旨を正直に伝えてください。
回答は分かりやすく、簡潔にまとめてください。"""

        user_prompt = f"""以下のコンテキストを参考にして、質問に答えてください。

【コンテキスト】
{context}

【質問】
{query}

【回答】"""

        # OpenAI APIで回答を生成
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # 低めに設定して事実ベースの回答を促す
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def query(self, question: str, top_k: int = 3, verbose: bool = True) -> Dict:
        """
        RAGパイプライン全体を実行
        
        Args:
            question: ユーザーの質問
            top_k: 検索する文書数
            verbose: 詳細情報を表示するか
            
        Returns:
            回答と関連情報
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"質問: {question}")
            print(f"{'='*60}")
        
        # 1. 関連文書を検索
        if verbose:
            print("\n[ステップ1: 関連文書の検索]")
        
        search_results = self.retrieve(question, top_k)
        
        if verbose:
            print(f"✓ {len(search_results['documents'][0])}件の関連文書を取得しました")
            for i, (doc, meta) in enumerate(zip(
                search_results['documents'][0],
                search_results['metadatas'][0]
            ), 1):
                print(f"\n  文書{i}: {meta['title']}")
                print(f"  内容: {doc[:100]}...")
        
        # 2. コンテキストの構築
        context = "\n\n".join([
            f"【{meta['title']}】\n{doc}"
            for doc, meta in zip(
                search_results['documents'][0],
                search_results['metadatas'][0]
            )
        ])
        
        # 3. LLMで回答を生成
        if verbose:
            print("\n[ステップ2: 回答の生成]")
        
        answer = self.generate_answer(question, context)
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"回答:\n{answer}")
            print(f"{'='*60}")
            
            print("\n[参照した情報源]")
            for i, meta in enumerate(search_results['metadatas'][0], 1):
                print(f"  {i}. {meta['title']} ({meta['source']})")
        
        return {
            'answer': answer,
            'sources': search_results['documents'][0],
            'metadata': search_results['metadatas'][0]
        }

# テスト実行
if __name__ == "__main__":
    # RAGシステムを初期化
    rag = RAGSystem()
    
    # テスト質問
    test_questions = [
        "Pythonの特徴を教えてください",
        "機械学習とディープラーニングの違いは何ですか?",
        "RAGとは何ですか?どのように動作しますか?"
    ]
    
    for question in test_questions:
        result = rag.query(question, top_k=2)
        print("\n" + "="*60 + "\n")