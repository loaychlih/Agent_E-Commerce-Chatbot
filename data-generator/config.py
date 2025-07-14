# Synthetic Data Generator Configuration

## Query Types to Generate:
QUERY_TYPES = [
    "product_search",
    "comparison_request", 
    "budget_inquiry",
    "feature_specific",
    "use_case_specific",
    "problem_solving",
    "recommendation_request"
]

## Example Query Patterns:
QUERY_PATTERNS = [
    "What's the best {product_type} for {use_case}?",
    "Can you recommend {product_type} under ${budget}?",
    "Which {product_type} has the best {feature}?",
    "I need {product_type} for {use_case}, any suggestions?",
    "Compare {product1} vs {product2}",
    "What do people think about {specific_product}?",
    "Best {category} products with {feature}?",
    "Cheapest {product_type} with good {quality_aspect}?"
]

## Categories from your dataset:
CATEGORIES = ["Smartphones", "Laptops", "Audio", "Wearables", "Smart Home"]

## Common use cases:
USE_CASES = ["gaming", "work", "travel", "fitness", "home use", "outdoor activities", "studying"]

## Budget ranges:
BUDGET_RANGES = ["$100", "$200", "$500", "$1000", "budget-friendly", "under $300"]
