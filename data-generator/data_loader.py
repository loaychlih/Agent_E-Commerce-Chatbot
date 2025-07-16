"""
Data loading and saving utilities for the synthetic data generator
"""

import pandas as pd
import json
import os


class DataLoader:
    """Handles loading product review data and saving generated testsets"""
    
    @staticmethod
    def load_product_data(file_path="data/product_reviews.csv"):
        """
        Load the product reviews dataset
        
        Args:
            file_path (str): Path to the CSV file containing product reviews
            
        Returns:
            tuple: (products_df, unique_products, unique_categories, features)
        """
        try:
            products_df = pd.read_csv(file_path)
            print(f"Loaded {len(products_df)} product reviews")
            
            # Extract unique values for query generation context
            unique_products = products_df['product'].unique().tolist()
            unique_categories = products_df['category'].unique().tolist()
            features = products_df['feature_mentioned'].unique().tolist()
            
            print(f"Found {len(unique_products)} unique products")
            print(f"Categories: {unique_categories}")
            
            return products_df, unique_products, unique_categories, features
            
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
    
    @staticmethod
    def save_synthetic_testset(enhanced_testset, unique_categories, unique_products, 
                             personas_used, filename="ragas_synthetic_testset.json"):
        """
        Save the enhanced synthetic testset in both JSON and CSV formats
        
        Args:
            enhanced_testset (list): List of enhanced query dictionaries
            unique_categories (list): List of product categories
            unique_products (list): List of product names
            personas_used (list): List of persona names used
            filename (str): Output filename (will create both .json and .csv)
            
        Returns:
            tuple: (json_filepath, csv_filepath)
        """
        output_data = {
            "metadata": {
                "generator": "Ragas-based Synthetic Data Generator",
                "total_queries": len(enhanced_testset),
                "source_data": "product_reviews.csv",
                "categories": unique_categories,
                "products_count": len(unique_products),
                "personas_used": personas_used
            },
            "synthetic_testset": enhanced_testset
        }
        
        # Save JSON
        json_filepath = os.path.join("data-generator", filename)
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved synthetic testset to {json_filepath}")
        
        # Save CSV
        csv_filename = filename.replace('.json', '.csv')
        csv_filepath = os.path.join("data-generator", csv_filename)
        
        csv_data = []
        for item in enhanced_testset:
            csv_data.append({
                'query': item['query'],
                'category': item['category'],
                'query_type': item['query_type'],
                'related_products': ', '.join(item['related_products']),
                'product_properties': json.dumps(item['product_properties']) if item['product_properties'] else ""
            })
        
        df = pd.DataFrame(csv_data)
        df.to_csv(csv_filepath, index=False, encoding='utf-8')
        print(f"Also saved as CSV: {csv_filepath}")
        
        return json_filepath, csv_filepath
    
    @staticmethod
    def display_sample_queries(enhanced_testset, num_samples=5):
        """
        Display sample generated queries for verification
        
        Args:
            enhanced_testset (list): List of enhanced query dictionaries
            num_samples (int): Number of samples to display
        """
        print(f"\nSample Generated Queries (showing {num_samples}):")
        print("=" * 60)
        
        for i, query_data in enumerate(enhanced_testset[:num_samples], 1):
            print(f"\n{i}. Query: {query_data['query']}")
            print(f"   Category: {query_data['category']}")
            print(f"   Type: {query_data['query_type']}")
            if query_data['related_products']:
                print(f"   Related Products: {', '.join(query_data['related_products'])}")
            if query_data['product_properties']:
                print(f"   Properties: {json.dumps(query_data['product_properties'], indent=6)}")
            print("-" * 40)
