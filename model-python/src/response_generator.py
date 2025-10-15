import random

TEMPLATES = {
    "greeting": [
        "Hello! How can I assist you today?",
        "Hi there! What would you like to do?"
    ],
    "complaint": [
        "I’m sorry to hear that. Could you please share more details?",
        "Thanks for letting me know — I’ll help you get this sorted."
    ],
    "positive_feedback": [
        "Glad to hear that! 😊",
        "That’s great — thank you for your feedback!"
    ],
    "negative_feedback": [
        "I appreciate the honesty. Let’s improve this together.",
        "Sorry about that — I’ll make sure it’s addressed."
    ],
    "question": [
        "That’s a good question! Let me explain...",
        "Sure! Here’s how it works:"
    ],
    "request_help": [
        "Absolutely, I’m here to help. What’s the issue?",
        "Sure, tell me more about what you need help with."
    ],
}

def generate_response(intent: str):
    return random.choice(TEMPLATES.get(intent, ["I'm here to assist you."]))
