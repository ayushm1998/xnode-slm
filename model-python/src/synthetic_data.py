# src/synthetic_data.py
import random

INTENTS = {
    "greeting": [
        "hi", "hello", "hey", "good morning", "good evening", "howdy"
    ],
    "complaint": [
        "this is not working", "I have an issue", "it keeps crashing", "bad service"
    ],
    "feedback": [
        "great job", "I love this", "this could be better", "I like the update"
    ],
    "inquiry": [
        "how does this work?", "what is your return policy?", "can you help me?"
    ],
    "request": [
        "please reset my password", "I need access", "send me the report"
    ],
    "apology": [
        "sorry", "sorry about that", "my apologies", "I didn’t mean to", 
        "please forgive me", "that was my mistake", "I apologize for the issue"
    ],
}

def generate_samples(n_per_intent=200):
    data = []
    for intent, examples in INTENTS.items():
        for _ in range(n_per_intent):
            text = random.choice(examples)
            data.append({"text": text, "intent": intent})
    random.shuffle(data)
    return data


if __name__ == "__main__":
    samples = generate_samples()
    for s in samples[:10]:
        print(s)
