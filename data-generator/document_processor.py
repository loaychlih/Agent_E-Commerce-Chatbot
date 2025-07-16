"""
Document processing and knowledge graph creation for product reviews
"""

from langchain.schema import Document
from ragas.testset.graph import KnowledgeGraph, Node, NodeType
from ragas.testset.transforms import apply_transforms
from ragas.testset.transforms import HeadlinesExtractor, HeadlineSplitter, KeyphrasesExtractor


class DocumentProcessor:
    """Handles document creation and knowledge graph construction"""
    
    def __init__(self, products_df, unique_products, unique_categories):
        """
        Initialize the document processor
        
        Args:
            products_df (pd.DataFrame): Product reviews dataframe
            unique_products (list): List of unique product names
            unique_categories (list): List of unique categories
        """
        self.products_df = products_df
        self.unique_products = unique_products
        self.unique_categories = unique_categories
        self.kg = KnowledgeGraph()
    
    def create_product_documents(self):
        """Create individual product documents from reviews"""
        print("Creating product documents for knowledge graph...")
        
        # Group reviews by product to create comprehensive product documents
        grouped_reviews = self.products_df.groupby('product')
        
        for product_name, product_reviews in grouped_reviews:
            product_info = product_reviews.iloc[0]
            category = product_info['category']
            
            # Aggregate all review data for this product
            all_reviews = product_reviews['review_text'].tolist()
            all_features = product_reviews['feature_mentioned'].unique().tolist()
            all_attributes = product_reviews['attribute_mentioned'].unique().tolist()
            avg_rating = product_reviews['rating'].mean()
            
            # Create structured document content with all product information
            doc_content = f"""Product: {product_name}
                                Category: {category}
                                Average Rating: {avg_rating:.1f}/5
                                Total Reviews: {len(product_reviews)}

                                Key Features: {', '.join(all_features)}
                                Key Attributes: {', '.join(all_attributes)}

                                Customer Reviews:
                                {chr(10).join([f"- {review}" for review in all_reviews[:5]])}

                                Product Summary:
                                This {category.lower()} product has received {len(product_reviews)} reviews with an average rating of {avg_rating:.1f} stars. 
                                Customers frequently mention features like {', '.join(all_features[:3])} and appreciate attributes such as {', '.join(all_attributes[:3])}.
                                """
            
            # Create LangChain document with metadata for enhanced context
            doc = Document(
                page_content=doc_content,
                metadata={
                    "product": product_name,
                    "category": category,
                    "rating": avg_rating,
                    "review_count": len(product_reviews),
                    "features": all_features,
                    "attributes": all_attributes
                }
            )
            
            # Add to knowledge graph as a document node
            self.kg.nodes.append(
                Node(
                    type=NodeType.DOCUMENT,
                    properties={
                        "page_content": doc.page_content,
                        "document_metadata": doc.metadata
                    }
                )
            )
    
    def create_category_documents(self):
        """Create category overview documents"""
        print("Creating category documents for knowledge graph...")
        
        for category in self.unique_categories:
            category_products = self.products_df[self.products_df['category'] == category]
            category_features = category_products['feature_mentioned'].unique().tolist()
            
            # Category-level summary document
            category_content = f"""Category Overview: {category}
                    Available Products: {', '.join(category_products['product'].unique())}
                    Common Features: {', '.join(category_features)}
                    Average Category Rating: {category_products['rating'].mean():.1f}/5

                    {category} products in our catalog offer various features and capabilities to meet different customer needs.
                    Popular features in this category include {', '.join(category_features[:5])}.
                    """
            
            category_doc = Document(
                page_content=category_content,
                metadata={
                    "type": "category_overview",
                    "category": category,
                    "product_count": len(category_products['product'].unique()),
                    "features": category_features
                }
            )
            
            # Add category document to knowledge graph
            self.kg.nodes.append(
                Node(
                    type=NodeType.DOCUMENT,
                    properties={
                        "page_content": category_doc.page_content,
                        "document_metadata": category_doc.metadata
                    }
                )
            )
    
    def build_knowledge_graph(self):
        """Build the complete knowledge graph with both product and category documents"""
        self.create_product_documents()
        self.create_category_documents()
        print(f"Created {len(self.kg.nodes)} documents in knowledge graph")
        return self.kg
    
    def apply_knowledge_graph_transforms(self, generator_llm):
        """
        Apply Ragas transforms to enhance the knowledge graph
        
        Args:
            generator_llm: The LangChain LLM wrapper for Ragas
        """
        print("Applying knowledge graph transformations...")
        
        # Initialize transforms with specific configurations
        headline_extractor = HeadlinesExtractor(llm=generator_llm, max_num=20)
        headline_splitter = HeadlineSplitter(max_tokens=1500)
        keyphrase_extractor = KeyphrasesExtractor(llm=generator_llm)
        
        transforms = [
            headline_extractor,    # Extract clear section titles
            headline_splitter,     # Split into manageable chunks
            keyphrase_extractor    # Extract semantic keyphrases
        ]
        
        # Apply all transforms to enhance the knowledge graph
        apply_transforms(self.kg, transforms=transforms)
        print(f"Knowledge graph now has {len(self.kg.nodes)} nodes after transforms")
        
        return self.kg
    
    def create_simplified_knowledge_graph(self):
        """Create a simplified knowledge graph with cleaner structure for fallback"""
        print("Creating simplified knowledge graph...")
        simplified_kg = KnowledgeGraph()
        
        # Use only first 10 products to reduce complexity
        sample_products = self.unique_products[:10]
        
        for product_name in sample_products:
            product_data = self.products_df[self.products_df['product'] == product_name]
            if not product_data.empty:
                product_info = product_data.iloc[0]
                category = product_info['category']
                avg_rating = product_data['rating'].mean()
                
                # Create minimal but sufficient content
                simple_content = f"""Product: {product_name}
                                    Category: {category}
                                    Rating: {avg_rating:.1f}/5
                                    This is a {category.lower()} product with good customer reviews."""
                
                simplified_kg.nodes.append(
                    Node(
                        type=NodeType.DOCUMENT,
                        properties={
                            "page_content": simple_content,
                            "document_metadata": {
                                "product": product_name,
                                "category": category,
                                "rating": avg_rating
                            }
                        }
                    )
                )
        
        print(f"Created simplified knowledge graph with {len(simplified_kg.nodes)} nodes")
        return simplified_kg
