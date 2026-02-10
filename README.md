# StyleSync AI

![Python 3.10](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi&logoColor=white)
![Google Gemini 1.5](https://img.shields.io/badge/Google%20Gemini-1.5-4285F4?logo=google&logoColor=white)
![Llama 3](https://img.shields.io/badge/Llama%203-Groq-orange)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-black)

**Turn raw product photos into market-ready listings in seconds.**

---

## 🏗️ Architecture: The Agentic Workflow

StyleSync AI leverages a multi-agent system to automate e-commerce content creation.

*   **👁️ Visual Analyst (Gemini 1.5):** Extracts 20+ visual features such as color, style, and material from product images.
*   **🧠 Memory Core (Pinecone):** Recalls successful market trends and high-converting SEO keywords using Vector Search (`stylesync-index-v2`).
*   **✍️ Copywriter (Llama 3 via Groq):** Synthesizes visual data and market trends into luxury sales copy, focusing on benefits and storytelling.
*   **📱 Social Agent:** Generates engaging Instagram captions and relevant hashtags to maximize social reach.

---

## 🚀 Getting Started

### Prerequisites

You will need the following API keys:
*   **GEMINI_API_KEY**: For visual analysis and embeddings.
*   **GROQ_API_KEY**: For the Llama 3 copywriter.
*   **PINECONE_API_KEY**: For vector memory storage.

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/stylesync-ai.git
    cd stylesync-ai
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Set up your `.env` file with the required API keys.

### Running Locally

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000` (or the port specified in your output).

### Docker

Build and run the container:

```bash
docker build -t stylesync-ai .
docker run -p 7860:7860 --env-file .env stylesync-ai
```

---

## 📚 API Documentation

### Generate Catalog

**Endpoint:** `POST /generate-catalog`

Upload a product image to generate a complete marketing package.

**Request:** `multipart/form-data` with a `file` field.

**Sample Response:**

```json
{
  "status": "success",
  "visual_analysis": {
    "main_color": "Midnight Blue",
    "product_type": "Evening Gown",
    "design_style": "Elegant",
    "visual_features": ["Silk chiffon", "Floor-length", "V-neck"]
  },
  "market_trends": [
    "luxury evening wear",
    "formal gala dress",
    "summer wedding guest"
  ],
  "final_listing": {
    "title": "Midnight Blue Silk Chiffon Evening Gown - Elegant V-Neck Floor-Length Dress",
    "description": "Step into the spotlight with this breathtaking Midnight Blue Evening Gown. Crafted from the finest silk chiffon, it drapes effortlessly...",
    "features": [
      "Luxurious silk chiffon fabric for a soft, flowing silhouette",
      "Elegant V-neckline accentuates the décolletage",
      "Floor-length design perfect for black-tie events"
    ],
    "price_estimate": "$250 - $400"
  }
}
```

---

## ☁️ Deployment

### Hugging Face Spaces

This project is configured for easy deployment to Hugging Face Spaces.

1.  Create a new Space (Select **Docker** as the SDK).
2.  Upload the code (or connect your GitHub repo).
3.  Add your API keys (`GEMINI_API_KEY`, `GROQ_API_KEY`, `PINECONE_API_KEY`) in the Space **Settings > Variables**.
4.  The application will automatically build and launch on port `7860`.

---

*StyleSync AI - Autonomous E-Commerce Agent*
