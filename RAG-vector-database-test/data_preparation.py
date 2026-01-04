import chromadb
from chromadb.config import Settings
import openai
import os
from dotenv import load_dotenv
import re

# 環境変数の読み込み
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_documents(file_path):
    """
    テキストファイルから文書を読み込み、セクションごとに分割
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # デバッグ: ファイル内容の確認
    print(f"\nファイル全体の文字数: {len(content)}")
    print(f"改行文字の数: {content.count(chr(10))}")
    
    # "===" で区切られたセクションを正規表現で抽出
    # パターン: === タイトル === 改行 本文
    pattern = r'===\s*([^=]+?)\s*===\s*\n(.*?)(?=\n===|$)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    documents = []
    metadatas = []
    
    print(f"\n正規表現で{len(matches)}個のセクションを検出")
    
    for i, (title, content_text) in enumerate(matches):
        title = title.strip()
        content_text = content_text.strip()
        
        if content_text:
            documents.append(content_text)
            metadatas.append({
                'title': title,
                'length': len(content_text),
                'source': 'sample_docs.txt'
            })
            print(f"  {i+1}. {title} ({len(content_text)}文字)")
    
    # 正規表現でうまくいかない場合の代替方法
    if len(documents) == 0:
        print("\n正規表現での抽出に失敗しました。代替方法を試します...")
        
        # より単純な分割方法
        sections = content.split('===')
        
        for i in range(len(sections)):
            section = sections[i].strip()
            if not section:
                continue
            
            # セクションの最初の行をタイトルとして扱う
            lines = section.split('\n')
            
            if len(lines) >= 1:
                # 最初の行がタイトル
                title = lines[0].strip()
                # 残りが本文
                content_text = '\n'.join(lines[1:]).strip()
                
                if content_text and len(content_text) > 10:  # 最低10文字以上
                    documents.append(content_text)
                    metadatas.append({
                        'title': title,
                        'length': len(content_text),
                        'source': 'sample_docs.txt'
                    })
                    print(f"  {len(documents)}. {title} ({len(content_text)}文字)")
    
    return documents, metadatas

def get_embedding(text):
    """
    OpenAI APIを使ってテキストをベクトル化
    """
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def prepare_vector_database():
    """
    Vector Databaseを準備し、文書を格納
    """
    print("="*60)
    print("Vector Database準備スクリプト")
    print("="*60)
    
    # ファイルの存在確認
    file_path = 'documents/sample_docs.txt'
    if not os.path.exists(file_path):
        print(f"\nエラー: {file_path} が見つかりません")
        print("documentsディレクトリとsample_docs.txtファイルを作成してください")
        return
    
    print(f"\n文書ファイルを読み込んでいます: {file_path}")
    documents, metadatas = load_documents(file_path)
    
    print(f"\n{'='*60}")
    print(f"合計 {len(documents)}個の文書を読み込みました")
    print(f"{'='*60}")
    
    if len(documents) == 0:
        print("\nエラー: 文書が読み込まれませんでした")
        print("\nsample_docs.txtの形式を確認してください:")
        print("期待される形式:")
        print("=== タイトル1 ===")
        print("本文1の内容...")
        print("")
        print("=== タイトル2 ===")
        print("本文2の内容...")
        return
    
    print("\nChromaクライアントを初期化しています...")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # 既存のコレクションがあれば削除
    try:
        client.delete_collection(name="tech_knowledge_base")
        print("✓ 既存のコレクションを削除しました")
    except:
        pass
    
    # 新しいコレクションを作成
    collection = client.create_collection(
        name="tech_knowledge_base",
        metadata={"description": "技術知識ベース"}
    )
    print("✓ 新しいコレクションを作成しました")
    
    print("\n文書をベクトル化しています...")
    embeddings = []
    for i, doc in enumerate(documents):
        print(f"  {i+1}/{len(documents)}: {metadatas[i]['title'][:30]}...")
        embedding = get_embedding(doc)
        embeddings.append(embedding)
    
    # Vector Databaseに追加
    print("\nVector Databaseに文書を追加しています...")
    ids = [f"doc_{i}" for i in range(len(documents))]
    
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"\n{'='*60}")
    print(f"✓ 完了! {len(documents)}個の文書をVector Databaseに格納しました")
    print(f"  保存場所: ./chroma_db")
    print(f"{'='*60}")
    
    # 動作確認
# 動作確認
    print("\n動作確認: テスト検索を実行...")
    test_query = "Pythonについて"
    test_query_embedding = get_embedding(test_query)  # Embeddingを生成
    
    test_results = collection.query(
        query_embeddings=[test_query_embedding],  # query_textsではなくquery_embeddings
        n_results=1
    )
    if test_results['documents']:
        print(f"✓ テスト検索成功")
        print(f"  検索結果: {test_results['metadatas'][0][0]['title']}")
    
    return collection

if __name__ == "__main__":
    prepare_vector_database()