"""
Query classification and enhancement utilities for e-commerce synthetic data
"""

import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


class QueryClassifier:
    """Handles query classification and context enhancement using LLM-based classification"""
    
    def __init__(self, llm=None):
        """Initialize with optional LLM for classification"""
        self.llm = llm or ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    
    def classify_query_type(self, query):
        """
        Classify query into e-commerce intent types using LLM
        
        Args:
            query (str): The user query to classify
            
        Returns:
            str: Query type classification
        """
        system_prompt = """You are an expert e-commerce query classifier. Classify the following query into one of these categories:

1. "category_queries" - Questions about product categories, general recommendations, or browsing multiple products
   Examples: "What are the best laptops?", "Show me smartphones", "Which category should I choose?"

2. "feature_queries" - Questions about specific product features, specifications, or capabilities
   Examples: "How's the battery life?", "What about the camera quality?", "Is the microphone good?"

3. "product_queries" - Questions about specific products, reviews, opinions, or individual product details
   Examples: "What do people think about iPhone?", "Is this product worth it?", "Tell me about this laptop"

Respond with ONLY the category name (category_queries, feature_queries, or product_queries)."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Classify this query: '{query}'")
        ]
        
        try:
            response = self.llm(messages)
            classification = response.content.strip().lower()
            
            # Validate response
            valid_types = ["category_queries", "feature_queries", "product_queries"]
            if classification in valid_types:
                return classification
            else:
                # Fallback to product queries if unclear
                return "product_queries"
                
        except Exception as e:
            print(f"Error in LLM classification: {e}")
            # Simple fallback classification
            return self._simple_fallback_classification(query)
    
    def _simple_fallback_classification(self, query):
        """Simple fallback classification if LLM fails"""
        query_lower = query.lower()
        
        # Simple heuristics as backup
        if any(word in query_lower for word in ['what', 'which', 'best', 'good', 'recommend']):
            if any(word in query_lower for word in ['laptops', 'smartphones', 'audio', 'wearables', 'category']):
                return "category_queries"
        
        if any(word in query_lower for word in ['how', 'quality', 'feature', 'performance', 'battery', 'camera']):
            return "feature_queries"
            
        # Default to product queries
        return "product_queries"
    
    @staticmethod
    def enhance_testset_with_ecommerce_context(testset_df, products_df, unique_products, unique_categories, llm=None):
        """
        Add e-commerce specific context to the generated testset
        
        Args:
            testset_df (pd.DataFrame): Generated testset from Ragas
            products_df (pd.DataFrame): Original product reviews data
            unique_products (list): List of unique product names
            unique_categories (list): List of unique categories
            llm: Optional LLM for classification
            
        Returns:
            list: Enhanced testset with e-commerce context
        """
        enhanced_testset = []
        classifier = QueryClassifier(llm) if llm else QueryClassifier()
        
        for _, row in testset_df.iterrows():
            query = row['user_input']
            context = row['reference_contexts'][0] if row['reference_contexts'] else ""
            
            # Product matching: Find products mentioned in query/context
            matched_products = []
            matched_category = "General"
            product_properties = {}
            
            # Search for product mentions in query and context
            for product in unique_products:
                if product.lower() in context.lower() or product.lower() in query.lower():
                    matched_products.append(product)
            
            # Determine the most relevant category
            for category in unique_categories:
                if category.lower() in context.lower() or category.lower() in query.lower():
                    matched_category = category
                    break
            
            # Extract product properties for matched products
            if matched_products:
                primary_product = matched_products[0]
                product_data = products_df[products_df['product'] == primary_product]
                if not product_data.empty:
                    product_properties = {
                        "product_name": primary_product,
                        "category": product_data.iloc[0]['category'],
                        "average_rating": product_data['rating'].mean(),
                        "total_reviews": len(product_data),
                        "features": product_data['feature_mentioned'].unique().tolist(),
                        "attributes": product_data['attribute_mentioned'].unique().tolist(),
                        "sentiment_distribution": {
                            "positive": len(product_data[product_data['sentiment'] == 'positive']),
                            "neutral": len(product_data[product_data['sentiment'] == 'neutral']),
                            "negative": len(product_data[product_data['sentiment'] == 'negative'])
                        }
                    }
            
            # For category queries, get category-level properties
            elif matched_category != "General":
                category_data = products_df[products_df['category'] == matched_category]
                if not category_data.empty:
                    product_properties = {
                        "category": matched_category,
                        "products_in_category": category_data['product'].unique().tolist(),
                        "average_category_rating": category_data['rating'].mean(),
                        "total_category_reviews": len(category_data),
                        "common_features": category_data['feature_mentioned'].unique().tolist(),
                        "common_attributes": category_data['attribute_mentioned'].unique().tolist()
                    }
            
            # Use LLM-based classification
            query_type = classifier.classify_query_type(query)
            
            # Create enriched query object with product properties
            enhanced_query = {
                "query": query,
                "context": context,
                "category": matched_category,
                "related_products": matched_products[:3],
                "query_type": query_type,
                "product_properties": product_properties,
                "synthesizer": row.get('synthesizer_name', 'unknown')
            }
            
            enhanced_testset.append(enhanced_query)
        
        return enhanced_testset
