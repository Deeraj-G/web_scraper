"""
This module contains the prompts for the content processor.
"""

from loguru import logger

def get_prompts(headings: list, text: str, text_limit: int = 4000, heading_limit: int = 10):
    """
    Static system and user prompts for the LLM
    """

    example_raw_text = """
    Introduction to Machine Learning ( ML ) represents a fundamental shift in how computers operate. Instead of following explicit programming instructions, these systems learn patterns from data. This revolutionary approach has transformed various industries and continues to drive innovation in technology. The field combines statistics, computer science, and data analysis to create powerful predictive models.

    Among the various approaches in machine learning, Supervised Learning Methods stands as one of the most widely used techniques. In this method, algorithms learn from labeled datasets where the desired output is known. For instance, when training a model to recognize spam emails, we provide examples of both spam and legitimate emails. The algorithm learns to identify patterns and features that distinguish between these categories. Common algorithms include decision trees, which make sequential decisions based on data features, and support vector machines, which find optimal boundaries between different classes of data.

    The impact of Deep Learning Applications on modern technology cannot be overstated. In healthcare, deep learning models analyze medical images to detect diseases with remarkable accuracy. Self-driving cars use deep learning to interpret their environment and make real-time decisions. Natural language processing applications powered by deep learning have made machine translation and voice assistants part of our daily lives.

    Neural Networks and Deep Learning are at the core of these advances. These networks consist of layers of interconnected nodes, each performing specific computations. The \" deep \" in deep learning refers to the multiple layers that allow these networks to learn increasingly complex features. For example, in image recognition, early layers might detect simple edges, while deeper layers recognize complex objects like faces or vehicles.
    """

    example_input = [
        {"Introduction to Machine Learning": "h1"},
        {"Supervised Learning Methods": "h2"},
        {"Deep Learning Applications": "h3"},
        {"Neural Networks and Deep Learning": "h2"},
    ]

    example_output = {
        "information": {
            "headings": {
                "Introduction to Machine Learning": "Machine learning represents a fundamental shift in how computers operate, enabling systems to learn patterns from data rather than following explicit programming instructions. This field combines statistics, computer science, and data analysis to create powerful predictive models.",
                "Supervised Learning Methods": "Supervised learning algorithms learn from labeled datasets where the desired output is known, using techniques like decision trees and support vector machines to identify patterns and make predictions. This approach is widely used for classification tasks like spam detection.",
                "Deep Learning Applications": "Deep learning has revolutionized multiple sectors, from healthcare (medical image analysis) to autonomous vehicles and natural language processing, enabling sophisticated real-time decision making and analysis.",
                "Neural Networks and Deep Learning": "Neural networks are mathematical models inspired by the human brain, consisting of multiple layers of interconnected nodes that process information with increasing complexity. These layers progress from detecting simple features to recognizing complex patterns in data.",
            }
        }
    }

    system_prompt = """
        You are a professional content analyst and information specialist who excels at extracting key information from documents.
    
        You are provided with both the full text and a structured list of headings from the document.
    
        Your role is to carefully analyze the content under each heading and produce clear, concise summaries that capture the essential information and main points.
    """

    user_prompt = f"""
        Your task is to analyze the following text and extract key information for each heading:

        ### CURRENT CONTENT TO ANALYZE ###
        TEXT: {text[:text_limit]}

        HEADINGS: The document contains {len(headings)} headings.
        First {heading_limit} headings for reference: ```{headings[:heading_limit]}```

        ### EXAMPLES ###
        EXAMPLE RAW TEXT:
        {example_raw_text}

        EXAMPLE INPUT:
        {example_input}

        EXAMPLE OUTPUT:
        {example_output}

        ### REQUIREMENTS ###
        For each heading:
        1. Create a clear, factually accurate summary (1-2 sentences) that captures key points
        2. Prioritize content based on heading importance (h1 > h2 > h3 etc.)
        3. Ensure output follows the exact JSON structure shown in the example
        4. Exclude any additional text or formatting
    """

    logger.info(f"System Prompt: {system_prompt}")
    logger.info(f"User Prompt: {user_prompt}")

    return system_prompt, user_prompt