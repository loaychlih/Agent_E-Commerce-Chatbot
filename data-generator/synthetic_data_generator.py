"""
LangChain Synthetic Data Generator for E-commerce Queries
Generates human-like product queries based on the product_reviews.csv dataset
"""

import pandas as pd
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import random

load_dotenv()

class SyntheticDataGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7)  # Higher temperature for more creative queries
        self.products_df = None
        self.load_product_data()
        
    def load_product_data(self):
        """Load the product reviews dataset"""
        try:
            self.products_df = pd.read_csv("data/product_reviews.csv")
            print(f"📊 Loaded {len(self.products_df)} product reviews")
            
            # Get unique products and categories for inspiration
            self.unique_products = self.products_df['product'].unique().tolist()
            self.unique_categories = self.products_df['category'].unique().tolist()
            self.features = self.products_df['feature_mentioned'].unique().tolist()
            
            print(f"🎯 Found {len(self.unique_products)} unique products")
            print(f"📱 Categories: {self.unique_categories}")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
    
    def create_query_generation_prompt(self):
        """Create a prompt template for generating human-like queries"""
        
        prompt_template = """
        You are generating realistic customer queries for an e-commerce chatbot. 
        
        Based on the following product information, generate diverse, human-like questions that real customers would ask:
        
        AVAILABLE PRODUCTS: {products}
        CATEGORIES: {categories}  
        COMMON FEATURES: {features}
        
        Generate queries that include:
        - Specific product inquiries
        - Comparison requests
        - Feature-based searches
        - Budget-conscious questions
        - Use case specific needs
        - Problem-solving queries
        
        Make the queries sound natural and conversational, like real customers would ask.
        Vary the language style (formal, casual, detailed, brief).
        
        Generate exactly {num_queries} unique queries in this JSON format:
        {{
            "queries": [
                {{"query": "What's the best smartphone under $500?", "intent": "budget_search", "category": "Smartphones"}},
                {{"query": "I need headphones for gaming, any recommendations?", "intent": "use_case_specific", "category": "Audio"}}
            ]
        }}
        
        GENERATE {num_queries} DIVERSE QUERIES NOW:
        """
        
        return ChatPromptTemplate.from_template(prompt_template)
    
    def generate_synthetic_queries(self, num_queries=20):
        """Generate synthetic user queries"""
        
        print(f"🚀 Generating {num_queries} synthetic queries...")
        
        # Prepare data for the prompt
        sample_products = random.sample(self.unique_products, min(10, len(self.unique_products)))
        sample_features = random.sample(self.features, min(15, len(self.features)))
        
        prompt = self.create_query_generation_prompt()
        
        # Create the chain
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            # Generate queries
            response = chain.invoke({
                "products": ", ".join(sample_products),
                "categories": ", ".join(self.unique_categories),
                "features": ", ".join(sample_features),
                "num_queries": num_queries
            })
            
            print("🤖 Generated response:")
            print(response)
            
            # Parse the JSON response
            try:
                queries_data = json.loads(response)
                return queries_data["queries"]
            except json.JSONDecodeError:
                print("⚠️ Response wasn't valid JSON, attempting to extract queries...")
                # Fallback: try to extract queries from text
                return self.extract_queries_from_text(response)
                
        except Exception as e:
            print(f"❌ Error generating queries: {e}")
            return []
    
    def extract_queries_from_text(self, text):
        """Fallback method to extract queries from text response"""
        queries = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and ('?' in line or 'recommend' in line.lower() or 'best' in line.lower()):
                # Clean up the line
                query = line.replace('"', '').replace('- ', '').strip()
                if len(query) > 10:  # Filter out very short lines
                    queries.append({
                        "query": query,
                        "intent": "general",
                        "category": "Unknown"
                    })
        
        return queries[:20]  # Limit to 20 queries
    
    def enhance_queries_with_context(self, queries):
        """Add more context to generated queries based on actual product data"""
        
        enhanced_queries = []
        
        for query_data in queries:
            query = query_data["query"]
            
            # Try to match with actual products
            matched_products = []
            for product in self.unique_products:
                if any(word.lower() in product.lower() for word in query.split()):
                    matched_products.append(product)
            
            # Get ratings for context
            if matched_products:
                product_ratings = []
                for product in matched_products[:3]:  # Top 3 matches
                    product_reviews = self.products_df[self.products_df['product'] == product]
                    avg_rating = product_reviews['rating'].mean()
                    product_ratings.append(f"{product}: {avg_rating:.1f}/5")
                
                enhanced_query = {
                    **query_data,
                    "matched_products": matched_products[:3],
                    "expected_context": product_ratings
                }
            else:
                enhanced_query = query_data
            
            enhanced_queries.append(enhanced_query)
        
        return enhanced_queries
    
    def save_synthetic_data(self, queries, filename="synthetic_queries.json"):
        """Save generated queries to a file"""
        
        output_data = {
            "metadata": {
                "total_queries": len(queries),
                "generated_from": "product_reviews.csv",
                "categories_available": self.unique_categories,
                "products_count": len(self.unique_products)
            },
            "synthetic_queries": queries
        }
        
        filepath = os.path.join("data-generator", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(queries)} synthetic queries to {filepath}")
        
        # Also save as CSV for comparison
        csv_filename = filename.replace('.json', '.csv')
        csv_filepath = os.path.join("data-generator", csv_filename)
        
        # Extract just the queries for CSV
        query_data = []
        for query in queries:
            query_data.append({'query': query['query']})
        
        # Save as CSV
        import csv
        with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['query']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(query_data)
        
        print(f"📊 Also saved as CSV: {csv_filepath}")
        
        return filepath

def main():
    """Main function to generate synthetic data"""
    
    print("🎯 Starting Synthetic Data Generation...")
    print("=" * 50)
    
    # Initialize generator
    generator = SyntheticDataGenerator()
    
    # Generate queries
    synthetic_queries = generator.generate_synthetic_queries(num_queries=20)
    
    if synthetic_queries:
        print(f"\n✅ Generated {len(synthetic_queries)} queries")
        
        # Enhance with context
        enhanced_queries = generator.enhance_queries_with_context(synthetic_queries)
        
        # Save to file
        output_file = generator.save_synthetic_data(enhanced_queries)
        
        # Display some examples
        print("\n🎯 Sample Generated Queries:")
        print("-" * 30)
        for i, query in enumerate(enhanced_queries[:5], 1):
            print(f"{i}. {query['query']}")
            if 'matched_products' in query:
                print(f"   → Related products: {', '.join(query['matched_products'])}")
            print()
        
        print(f"📄 All queries saved to: {output_file}")
    else:
        print("❌ No queries were generated")

if __name__ == "__main__":
    main()
