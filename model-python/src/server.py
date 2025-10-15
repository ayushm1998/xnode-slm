from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.metrics_store import metrics_store
import torch, time

# FastAPI setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model loading 
MODEL_PATH = "./models/intent_classifier"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

INTENTS = ["greeting", "complaint", "feedback", "inquiry", "request", "apology"]

#  Input schema 
class PredictIn(BaseModel):
    text: str

#  Prediction endpoint 
@app.post("/predict")
async def predict(data: PredictIn):
    start_time = time.time()  # start timer for latency
    inputs = tokenizer(data.text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        conf, pred = torch.max(probs, dim=1)

    idx = pred.item()
    confidence = float(conf.item())

    # Safe lookup
    intent = INTENTS[idx] if idx < len(INTENTS) else "unknown"

    # Response messages
    responses = {
        "greeting": "Hello there! How can I assist you today?",
        "complaint": "I understand your concern. Could you please provide more details?",
        "feedback": "Thank you for your feedback — it helps us improve!",
        "inquiry": "Sure, let me help answer your question.",
        "request": "Got it! I'll process your request shortly.",
        "apology": "No worries at all! How can I help you move forward?",
        "unknown": "I'm not entirely sure how to categorize that — could you rephrase?",
    }

    latency_ms = (time.time() - start_time) * 1000

    #Record metrics
    metrics_store.record(intent, confidence, latency_ms)

    return {
        "intent": intent,
        "confidence": confidence,
        "message": responses[intent],
    }


#  Metrics endpoint 
@app.get("/metrics")
async def get_metrics():
    return metrics_store.summary()


#  Health check 
@app.get("/")
async def root():
    return {"status": "Intent model server running"}
