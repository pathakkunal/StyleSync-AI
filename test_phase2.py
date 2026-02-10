import os
import asyncio
from agents.visual_analyst import VisualAnalyst
from agents.writer_agent import WriterAgent

# Dummy data to test Writer without burning Vision tokens if image is missing
MOCK_VISUAL_DATA = {
    "main_color": "Midnight Blue",
    "product_type": "Bomber Jacket",
    "design_style": "Cyberpunk Streetwear",
    "visual_features": ["High collar", "Metallic zippers", "Water-resistant texture"]
}

MOCK_KEYWORDS = ["urban techwear", "waterproof jacket", "futuristic fashion"]

async def run_test():
    print("🚀 Starting Phase 2: Intelligence Check...")
    
    # 1. Test Vision (If image exists)
    img_path = "test_image.jpg"
    visual_data = MOCK_VISUAL_DATA
    
    if os.path.exists(img_path):
        print(f"\n👁️  Testing Vision Agent on '{img_path}'...")
        try:
            vision = VisualAnalyst()
            visual_data = await vision.analyze_image(img_path)
            print("✅ Vision Result:", visual_data.get("product_type", "Unknown"))
        except Exception as e:
            print(f"❌ Vision Failed: {e}")
    else:
        print(f"\n⚠️  '{img_path}' not found. Using Mock Data for Writer test.")

    # 2. Test Writer (The Brain)
    print("\n🧠 Testing Writer Agent (Llama 3)...")
    try:
        writer = WriterAgent()
        copy = writer.write_listing(visual_data, MOCK_KEYWORDS)
        
        if "title" in copy:
            print(f"✅ Title: {copy['title']}")
            print(f"✅ Price Est: {copy.get('price_estimate', 'N/A')}")
            print("✅ Description Snippet:", copy['description'][:100] + "...")
        else:
            print("❌ Writer returned invalid JSON:", copy)
            
    except Exception as e:
        print(f"❌ Writer Failed: {e}")

    print("\n🎉 Phase 2 Complete.")

if __name__ == "__main__":
    asyncio.run(run_test())
