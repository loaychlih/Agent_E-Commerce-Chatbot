# E-Commerce Chatbot with Synthetic Data Generation

Welcome to the E-Commerce Chatbot project! This advanced chatbot system is designed to assist users with their online shopping experience by providing intelligent product recommendations, answering questions, and handling various e-commerce inquiries. The project features a sophisticated **Synthetic Data Generation Pipeline** using the Ragas framework to create realistic test datasets for chatbot training and evaluation.

## Overview

The E-Commerce Chatbot combines traditional chatbot functionality with cutting-edge synthetic data generation capabilities:

### Core Chatbot Features
- Built using Python and Flask framework with natural language processing (NLP)
- Integrates with e-commerce product databases for personalized recommendations
- RAG (Retrieval-Augmented Generation) system for accurate product information retrieval

### Synthetic Data Generation System
- **Ragas Framework Integration**: Leverages the Ragas library for generating high-quality synthetic test datasets
- **Real Data-Driven Personas**: Customer personas based on actual product review patterns and sentiment analysis
- **Intelligent Query Classification**: LLM-powered query categorization (product, category, feature-based queries)
- **Knowledge Graph Construction**: Automated knowledge graphs from product catalogs and reviews
- **Multi-Modal Generation**: Supports various query types and complexity levels

## Key Features

### Chatbot Capabilities
- Interactive chat interface for seamless user interaction
- Advanced natural language processing for query understanding
- Product recommendation engine based on user preferences and browsing history
- Integration with e-commerce store's product database
- Handles inquiries about product availability, pricing, shipping, comparisons, and more

### Synthetic Data Generation Pipeline
- **Automated Dataset Creation**: Generate realistic customer queries from product review data
- **Persona-Driven Generation**: 6 distinct customer personas (Budget Shopper, Tech Enthusiast, Quality Seeker, etc.)
- **Context-Aware Queries**: Generated queries include product properties, sentiment, and category information
- **Evaluation Ready**: Compatible with Ragas evaluation metrics for chatbot performance testing
- **Modular Architecture**: Clean separation of concerns with dedicated modules for different functionalities

## Project Structure

```
├── app.py                          # Main Flask application
├── data/                           # Product and review datasets
│   ├── flipkart_product_review.csv
│   └── product_reviews.csv
├── data-generator/                 # Synthetic Data Generation System
│   ├── __init__.py                # Package initialization
│   ├── ragas_synthetic_generator.py  # Main orchestrator
│   ├── personas.py                # Customer persona definitions
│   ├── data_loader.py            # Data loading and I/O operations
│   ├── document_processor.py     # Knowledge graph construction
│   ├── query_classifier.py       # LLM-based query classification
│   └── ragas_config.py           # Configuration settings
├── ecommbot/                      # Core chatbot modules
│   ├── ingest.py                 # Data ingestion pipeline
│   ├── retrieval_generation.py  # RAG implementation
│   └── data_converter.py         # Data preprocessing
├── evaluate_with_ragas.py        # Evaluation pipeline
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Installation

To set up the E-Commerce Chatbot with Synthetic Data Generation locally, follow these steps:

### Prerequisites
- Python 3.8+ 
- OpenAI API key for LLM operations
- Git for version control

### Setup Instructions

1. **Clone the repository to your local machine:**
```bash
git clone https://github.com/loaychlih/Agent_E-Commerce-Chatbot.git
```

2. **Navigate to the project directory:**
```bash
cd Agent_E-Commerce-Chatbot
```

3. **Create and activate a virtual environment (recommended):**
```bash
python -m venv venv312
# On Windows:
venv312\Scripts\activate
# On macOS/Linux:
source venv312/bin/activate
```

4. **Install the required Python packages:**
```bash
pip install -r requirements.txt
```

5. **Set up environment variables:**
- Create a `.env` file in the project root directory
- Add the following environment variables:
```env
OPENAI_API_KEY=your_openai_api_key_here
# Add any other necessary API keys or configuration
```

6. **Run the chatbot application:**
```bash
python app.py
```

7. **Generate synthetic data (optional but recommended for testing):**
```bash
cd data-generator
python ragas_synthetic_generator.py
```

## Usage

### Running the Chatbot
After installation, access the chatbot through your web browser at `http://localhost:5000` (or the configured port).

### Generating Synthetic Data
The synthetic data generation system can be used to create test datasets:

```python
from data_generator import RagasSyntheticDataGenerator

# Initialize the generator
generator = RagasSyntheticDataGenerator()

# Generate synthetic test queries
testset_df = generator.generate_synthetic_testset(testset_size=20)

# Enhance with e-commerce context
enhanced_testset = generator.enhance_testset_with_ecommerce_context(testset_df)

# Save results
generator.save_synthetic_testset(enhanced_testset)
```

### Key Components

1. **Personas System**: Six distinct customer personas drive query generation:
   - Budget-conscious shoppers
   - Tech enthusiasts  
   - Quality-focused buyers
   - Quick decision makers
   - Research-oriented customers
   - Value seekers

2. **Query Classification**: Intelligent categorization of queries into:
   - Product-specific queries
   - Category browsing queries  
   - Feature comparison queries
   - General information requests

3. **Knowledge Graph**: Automated construction from product catalogs including:
   - Product hierarchies
   - Feature relationships
   - Category mappings
   - Review sentiment analysis

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Ragas](https://github.com/explodinggradients/ragas) for synthetic data generation
- Uses OpenAI GPT models for natural language processing
- Leverages LangChain for LLM orchestration
