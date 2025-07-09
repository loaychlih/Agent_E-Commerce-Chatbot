"""
AstraDB Database Inspector
This script helps you explore what's stored in your AstraDB database
"""

from ecommbot.ingest import ingestdata
from dotenv import load_dotenv
import os

load_dotenv()

def inspect_database():
    """Get statistics and content overview of the database"""
    print("🔍 AstraDB Database Inspector")
    print("=" * 50)
    
    # Connect to vector store
    try:
        vstore = ingestdata("done")  # Connect without inserting new data
        print("✅ Successfully connected to AstraDB")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    # Get database info
    print(f"\n📊 Database Configuration:")
    print(f"   • API Endpoint: {os.getenv('ASTRA_DB_API_ENDPOINT')}")
    print(f"   • Keyspace: {os.getenv('ASTRA_DB_KEYSPACE')}")
    print(f"   • Collection: chatbotecomm")
    
    # Test search functionality
    print(f"\n🔎 Testing Search Functionality:")
    try:
        # Test a simple search
        results = vstore.similarity_search("bluetooth headphones", k=3)
        print(f"   • Found {len(results)} similar documents")
        
        if results:
            print(f"\n📝 Sample Search Results:")
            for i, doc in enumerate(results, 1):
                print(f"\n   Result {i}:")
                print(f"   • Product: {doc.metadata.get('product_name', 'Unknown')}")
                print(f"   • Review Preview: {doc.page_content[:100]}...")
                print(f"   • Metadata: {doc.metadata}")
                
    except Exception as e:
        print(f"   ❌ Search test failed: {e}")
    
    # Test different search queries
    print(f"\n🎯 Testing Various Product Searches:")
    test_queries = [
        "best bass headphones",
        "budget bluetooth earbuds", 
        "gaming headphones",
        "wireless earphones for sports"
    ]
    
    for query in test_queries:
        try:
            results = vstore.similarity_search(query, k=1)
            if results:
                product_name = results[0].metadata.get('product_name', 'Unknown')
                print(f"   • '{query}' → {product_name}")
            else:
                print(f"   • '{query}' → No results found")
        except Exception as e:
            print(f"   • '{query}' → Error: {e}")

def get_collection_stats():
    """Get detailed statistics about the collection"""
    print(f"\n📈 Collection Statistics:")
    
    try:
        vstore = ingestdata("done")
        
        # Try to get collection info (this might vary based on AstraDB version)
        print("   • Collection Name: chatbotecomm")
        print("   • Vector Dimension: 1536 (OpenAI ada-002 embeddings)")
        print("   • Data Type: Product reviews with vector embeddings")
        
        # Test multiple searches to estimate content
        sample_searches = ["headphones", "earbuds", "bluetooth", "audio", "sound"]
        unique_products = set()
        
        for search in sample_searches:
            try:
                results = vstore.similarity_search(search, k=10)
                for result in results:
                    if 'product_name' in result.metadata:
                        unique_products.add(result.metadata['product_name'])
            except:
                continue
        
        print(f"   • Estimated Unique Products: {len(unique_products)}")
        print(f"   • Products Found: {list(unique_products)[:5]}{'...' if len(unique_products) > 5 else ''}")
        
    except Exception as e:
        print(f"   ❌ Could not fetch collection stats: {e}")

if __name__ == "__main__":
    inspect_database()
    get_collection_stats()
    
    print(f"\n💡 Tips:")
    print(f"   • Check AstraDB Console for visual interface")
    print(f"   • Collection 'chatbotecomm' contains your product data")
    print(f"   • Each document has product_name metadata and review content")
    print(f"   • Vector embeddings enable semantic search")
