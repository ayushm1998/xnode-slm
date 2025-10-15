import random


INTENTS = {
    "greeting": [
        "hi", "hello", "hey", "good morning", "good evening", "howdy",
        "hi there", "hey there", "what’s up", "yo", "greetings"
    ],
    "complaint": [
        "this is not working", "I have an issue", "bad service", "it keeps crashing",
        "unacceptable experience", "the app froze", "terrible response time",
        "it doesn’t load", "your support failed", "very disappointed"
    ],
    "feedback": [
        "great job", "I love this", "this could be better", "I like the update",
        "awesome design", "terrible UI", "love the new feature", "hate the update",
        "fantastic support", "could improve speed"
    ],
    "inquiry": [
        "how does this work?", "what is your return policy?", "can you help me?",
        "where can I find my invoice?", "how do I update my info?",
        "who can I contact?", "what are your hours?", "can you explain this?",
        "how much does it cost?", "do you ship internationally?"
    ],
    "request": [
        "please reset my password", "I need access", "send me the report",
        "could you share the file?", "give me an update", "assign me to the project",
        "approve my request", "schedule a meeting", "generate a summary", "forward me the details"
    ],
    "apology": [
        "sorry", "sorry about that", "my apologies", "I didn’t mean to",
        "please forgive me", "that was my mistake", "I apologize for the issue",
        "really sorry for the delay", "so sorry for any inconvenience",
        "I feel bad about that", "forgive me for the confusion", "apologies again"
    ]
}

def generate_samples(n_per_intent=120):
    """Generate synthetic training data by paraphrasing and shuffling."""
    samples = []
    for intent, examples in INTENTS.items():
        for _ in range(n_per_intent):
            text = random.choice(examples)
            if random.random() < 0.4:
                # small paraphrase trick
                text = text.capitalize()
            if random.random() < 0.3:
                text += random.choice(["!", ".", " please", " thank you"])
            samples.append({"intent": intent, "text": text})
    random.shuffle(samples)
    return samples


if __name__ == "__main__":
    samples = generate_samples()
    for s in samples[:10]:
        print(s)
