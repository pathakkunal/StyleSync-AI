import time
from agents.memory_agent import MemoryAgent

# Curated "StyleSync" Knowledge Base
DATASET = [
    {
        "id": "trend_streetwear_01",
        "text": "Oversized Acid Wash T-Shirt Heavyweight",
        "keywords": "streetwear, y2k fashion, distressed, vintage wash, boxy fit, urban aesthetic, 100% cotton, drop shoulder"
    },
    {
        "id": "trend_active_01",
        "text": "Seamless High-Waist Yoga Leggings",
        "keywords": "athleisure, squat-proof, moisture-wicking, four-way stretch, gym essentials, pilates gear, sculpting fit"
    },
    {
        "id": "trend_gorpcore_01",
        "text": "Waterproof Technical Shell Jacket",
        "keywords": "gorpcore, outdoor gear, gore-tex, tactical, utility pockets, rainwear, hiking essentials, techwear"
    },
    {
        "id": "trend_coquette_01",
        "text": "Satin Bow Ribbon Corset Top",
        "keywords": "coquette aesthetic, balletcore, soft girl, feminine, lace details, pastel vibes, ribbon bows"
    },
    {
        "id": "trend_oldmoney_01",
        "text": "Cable Knit Cashmere Sweater Polo",
        "keywords": "old money aesthetic, quiet luxury, preppy, tennis club, timeless, sophisticated, academia"
    }
]

def run_training():
    print("🚀 Starting Phase 3: Memory Training...")
    
    # 1. Initialize
    agent = MemoryAgent()
    if not hasattr(agent, 'index'):
        print("❌ Memory Agent failed to initialize. Check API keys.")
        return

    # 2. Upload Data
    print(f"\n📦 Seeding {len(DATASET)} trend concepts into Pinecone...")
    vectors = []
    for item in DATASET:
        embedding = agent._get_embedding(item['text'])
        # Handle simple list return or dictionary return from newer SDK versions if needed
        # The agent method returns list or [0.0]*768
        
        # Verify embedding format
        if isinstance(embedding, dict) and 'embedding' in embedding:
             vector_values = embedding['embedding']
        else:
             vector_values = embedding

        if vector_values and vector_values[0] != 0.0:
            vectors.append({
                "id": item['id'],
                "values": vector_values,
                "metadata": {"keywords": item['keywords'], "text": item['text']}
            })
    
    try:
        agent.index.upsert(vectors=vectors)
        print("✅ Upload complete!")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return

    # 3. Test Retrieval
    test_query = "vintage streetwear hoodie"
    print(f"\n🔎 Testing Recall for: '{test_query}'")
    time.sleep(2) # Wait for eventual consistency
    
    results = agent.retrieve_keywords(test_query)
    
    if results:
        print(f"✅ Memory Retrieved: {', '.join(results)}")
    else:
        print("⚠️  No results found. Index might still be indexing.")

if __name__ == "__main__":
    run_training()
