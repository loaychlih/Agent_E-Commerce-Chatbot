"""
Ragas-based Synthetic Data Generator for E-commerce Queries
Generates human-like product queries using Ragas framework based on the product_reviews.csv dataset
"""

import pandas as pd
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import Document

# Ragas imports
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.testset.graph import KnowledgeGraph, Node, NodeType
from ragas.testset.synthesizers.single_hop.specific import SingleHopSpecificQuerySynthesizer
from ragas.testset import TestsetGenerator

# Local imports
from personas import EcommercePersonas
from data_loader import DataLoader
from document_processor import DocumentProcessor
from query_classifier import QueryClassifier

load_dotenv()

class RagasSyntheticDataGenerator:
    def __init__(self):
        """Initialize the Ragas-based synthetic data generator"""
        # Initialize LLM and embeddings - core AI models for generation
        self.generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini", temperature=0.7))
        self.generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))
        
        # Initialize OpenAI LLM for query classification
        self.openai_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        
        # Initialize data pipeline using new modules
        self.data_loader = DataLoader()
        self.products_df = None
        self.unique_products = None
        self.unique_categories = None
        self.features = None
        
        # Load data
        self.load_product_data()
        
        # Initialize document processor and personas
        self.doc_processor = DocumentProcessor(self.products_df, self.unique_products, self.unique_categories)
        self.personas = EcommercePersonas.get_ragas_personas()
        
        # Build knowledge graph
        self.kg = self.doc_processor.build_knowledge_graph()
        
        print(f"Created {len(self.personas)} customer personas")
        
    def load_product_data(self):
        """Load the product reviews dataset using DataLoader"""
        self.products_df, self.unique_products, self.unique_categories, self.features = self.data_loader.load_product_data()
    
    def setup_query_distribution(self):
        """Set up query synthesizers with distribution"""
        query_distribution = [
            (
                SingleHopSpecificQuerySynthesizer(
                    llm=self.generator_llm, 
                    property_name="headlines"  # Focus on extracted headlines
                ),
                0.5,  # 50% of queries from headlines
            ),
            (
                SingleHopSpecificQuerySynthesizer(
                    llm=self.generator_llm, 
                    property_name="keyphrases"  # Focus on extracted keyphrases
                ),
                0.5,  # 50% of queries from keyphrases
            ),
        ]
        
        return query_distribution
    
    def generate_synthetic_testset(self, testset_size=20):
        """Generate synthetic test set using Ragas"""
        print(f"Generating synthetic testset with {testset_size} samples...")
        
        # Step 1: Enhance knowledge graph with AI transforms
        self.kg = self.doc_processor.apply_knowledge_graph_transforms(self.generator_llm)
        query_distribution = self.setup_query_distribution()
        
        # Step 2: Create the main testset generator
        generator = TestsetGenerator(
            llm=self.generator_llm,
            embedding_model=self.generator_embeddings,
            knowledge_graph=self.kg,
            persona_list=self.personas,
        )
        
        # Step 3: Primary generation attempt with full configuration
        try:
            testset = generator.generate(
                testset_size=testset_size, 
                query_distribution=query_distribution
            )
            
            testset_df = testset.to_pandas()
            print(f"Generated {len(testset_df)} synthetic queries")
            
            return testset_df
            
        except Exception as e:
            print(f"Error generating testset: {e}")
            print("Trying basic generation without query distribution...")
            
            # Fallback 1: Basic generation without distribution
            try:
                testset = generator.generate(testset_size=testset_size)
                testset_df = testset.to_pandas()
                print(f"Generated {len(testset_df)} synthetic queries (basic method)")
                return testset_df
                
            except Exception as e2:
                print(f"Basic generation also failed: {e2}")
                
                # Fallback 2: Simplified knowledge graph approach
                print("Trying with simplified knowledge graph...")
                try:
                    simplified_kg = self.doc_processor.create_simplified_knowledge_graph()
                    
                    simple_generator = TestsetGenerator(
                        llm=self.generator_llm,
                        embedding_model=self.generator_embeddings,
                        knowledge_graph=simplified_kg,
                        persona_list=self.personas,
                    )
                    
                    testset = simple_generator.generate(testset_size=testset_size)
                    testset_df = testset.to_pandas()
                    print(f"Generated {len(testset_df)} synthetic queries (simplified KG)")
                    return testset_df
                    
                except Exception as e3:
                    print(f"All generation methods failed: {e3}")
                    return None
    
    def enhance_testset_with_ecommerce_context(self, testset_df):
        """Add e-commerce specific context to the generated testset using QueryClassifier"""
        return QueryClassifier.enhance_testset_with_ecommerce_context(
            testset_df, self.products_df, self.unique_products, self.unique_categories, llm=self.openai_llm
        )
    
    def save_synthetic_testset(self, enhanced_testset, filename="ragas_synthetic_testset.json"):
        """Save the enhanced synthetic testset using DataLoader"""
        return self.data_loader.save_synthetic_testset(
            enhanced_testset, 
            self.unique_categories, 
            self.unique_products,
            EcommercePersonas.get_persona_names(),
            filename
        )
    
    def display_sample_queries(self, enhanced_testset, num_samples=5):
        """Display sample generated queries using DataLoader"""
        self.data_loader.display_sample_queries(enhanced_testset, num_samples)

def main():
    """Main function to generate synthetic data using Ragas"""
    print("Starting Ragas-based Synthetic Data Generation...")
    print("=" * 60)
    
    try:
        # Initialize the main generator class
        generator = RagasSyntheticDataGenerator()
        
        # Generate synthetic testset with specified size
        testset_df = generator.generate_synthetic_testset(testset_size=10)
        
        if testset_df is not None and not testset_df.empty:
            # Enhance with e-commerce specific metadata
            enhanced_testset = generator.enhance_testset_with_ecommerce_context(testset_df)
            
            # Save results in both JSON and CSV formats
            json_file, csv_file = generator.save_synthetic_testset(enhanced_testset)
            
            # Display sample queries for quick verification
            generator.display_sample_queries(enhanced_testset)
            
            # Success summary
            print(f"\nSuccessfully generated {len(enhanced_testset)} synthetic queries")
            print(f"Results saved to:")
            print(f"   - JSON: {json_file}")
            print(f"   - CSV: {csv_file}")
            
        else:
            print("No testset was generated")
            
    except Exception as e:
        print(f"Error in main execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
