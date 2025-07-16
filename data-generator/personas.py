"""
E-commerce customer personas for synthetic query generation
Based on real customer review patterns and language from product_reviews.csv
"""

from ragas.testset.persona import Persona


class EcommercePersonas:
    """Customer personas derived from actual e-commerce review data"""
    
    @staticmethod
    def get_persona_definitions():
        """Get the raw persona definitions as dictionaries"""
        return [
            {
                "name": "Budget-Conscious Shopper",
                "description": "A practical customer who looks for value and worries about waste. Based on reviews mentioning 'waste of money' and disappointment, asks questions like 'Is this worth it?', 'Will I regret buying this?', 'Does this justify the cost?', and 'Are there better alternatives for the price?'. Often concerned about products that 'constantly fail' or have poor quality."
            },
            {
                "name": "Tech Enthusiast", 
                "description": "An advanced user focused on specific technical features like facial recognition, fast charging, automation capabilities, app integration, and performance. Reviews show interest in features working 'perfectly' and being 'exceptional'. Asks 'How well does the facial recognition work?', 'Is the fast charging reliable?', 'How's the app integration?', and 'Does the automation work as advertised?'"
            },
            {
                "name": "First-Time Buyer",
                "description": "A newcomer seeking simple guidance and avoiding complex issues. Based on reviews mentioning ease of use and setup process, asks basic questions like 'Which laptop is good for beginners?', 'What's the easiest to set up?', 'Is this user-friendly?', and 'What should a first-time buyer know about wearables?'. Wants products that are 'amazing' and 'work perfectly' without complications."
            },
            {
                "name": "Quality-Focused Customer",
                "description": "A reliability-conscious buyer concerned about long-term performance and build quality. Reviews show complaints about products that 'stopped working properly' or have 'poor build quality'. Asks 'How's the build quality?', 'Does this last long?', 'Do people have durability issues?', and 'Is this reliable over time?'. Values products with 'exceptional' quality and 'top-notch' construction."
            },
            {
                "name": "Comparison Shopper", 
                "description": "A thorough researcher who wants to understand relative performance before deciding. Based on reviews comparing products and mentioning 'exceeded expectations', asks 'How does this compare to other smartphones?', 'Which is better - this laptop or others?', 'What are the pros and cons compared to alternatives?', and 'Which wearable gives the best overall experience?'"
            },
            {
                "name": "Feature-Focused User",
                "description": "A user interested in specific functionality like battery life, sound quality, comfort, microphone performance, health tracking, and connectivity. Reviews show detailed mentions of features 'working perfectly' or 'being frustrating'. Asks 'How's the battery life?', 'Is the sound quality good?', 'How comfortable is it?', 'Does the microphone work well?', and 'How accurate is the health tracking?'"
            }
        ]
    
    @classmethod
    def get_ragas_personas(cls):
        """Get Ragas Persona objects ready for use in TestsetGenerator"""
        persona_defs = cls.get_persona_definitions()
        return [
            Persona(
                name=persona["name"],
                role_description=persona["description"]
            )
            for persona in persona_defs
        ]
    
    @staticmethod
    def get_persona_names():
        """Get just the persona names for reference"""
        return [persona["name"] for persona in EcommercePersonas.get_persona_definitions()]
