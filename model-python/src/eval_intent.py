import torch, json, time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from synthetic_data import INTENTS

CKPT = "./checkpoints/intent"
tok = AutoTokenizer.from_pretrained(CKPT)
mdl = AutoModelForSequenceClassification.from_pretrained(CKPT)

def dataset(split="test"):
    xs, ys = [], []
    labels = list(INTENTS.keys()); lab2id = {l:i for i,l in enumerate(labels)}
    for intent, texts in INTENTS.items():
        for t in texts[-2:]:  # simple held-out slices
            xs += [t, t.capitalize(), f"please {t}"]
            ys += [lab2id[intent]]*3
    return xs, ys, labels

def eval_acc():
    xs, ys, labels = dataset("test")
    correct = 0
    for x, y in zip(xs, ys):
        enc = tok(x, return_tensors="pt")
        with torch.no_grad():
            logits = mdl(**enc).logits
            pred = int(torch.argmax(logits, dim=-1).item())
        correct += int(pred==y)
    return correct/len(xs)

if __name__=="__main__":
    print("Test accuracy:", eval_acc())
