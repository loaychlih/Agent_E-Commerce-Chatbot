# Synthetic Data Generator

This module generates human-like customer queries for your e-commerce chatbot using LangChain and OpenAI.

## Features

🎯 **Smart Query Generation**: Creates realistic customer queries based on your actual product data
📊 **Context-Aware**: Uses your product_reviews.csv to generate relevant questions
🤖 **LangChain Powered**: Leverages LangChain for structured prompt engineering
💾 **JSON Output**: Saves generated queries in structured JSON format

## How it Works

1. **Analyzes your product data** (product_reviews.csv)
2. **Extracts key information** (products, categories, features)
3. **Uses OpenAI to generate** human-like queries
4. **Enhances queries** with product context
5. **Saves structured data** for testing/evaluation

## Usage

```bash
# Navigate to project root
cd c:\Users\u_10018144\ecomagent\Agent_E-Commerce-Chatbot

# Run the generator
python data-generator/synthetic_data_generator.py
```

## Output

The generator creates:
- `synthetic_queries.json` - Generated queries with metadata
- Queries categorized by intent and product category
- Context about matched products and expected ratings

## Example Generated Queries

```json
{
  "query": "What's the best smartphone under $500?",
  "intent": "budget_search", 
  "category": "Smartphones",
  "matched_products": ["TechPro X20", "GalaxyWave S5"]
}
```

## Customization

Edit `config.py` to:
- Add new query patterns
- Modify budget ranges
- Update use cases
- Adjust categories

## Requirements

- OpenAI API key in `.env`
- LangChain installed
- Access to `product_reviews.csv`
