import random, os, json, time
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW
from synthetic_data import INTENTS

LABELS = list(INTENTS.keys())
LABEL2ID = {l:i for i,l in enumerate(LABELS)}
ID2LABEL = {i:l for l,i in LABEL2ID.items()}

class TinyDataset(Dataset):
    def __init__(self, split="train"):
        xs, ys = [], []
        for intent, texts in INTENTS.items():
            aug = []
            for t in texts:
                aug += [t, t.capitalize(), f"please {t}", f"{t} !!!"]
            random.shuffle(aug)
            for t in aug[:int(0.8*len(aug))] if split=="train" else aug[int(0.8*len(aug)):]:
                xs.append(t); ys.append(LABEL2ID[intent])
        self.data = list(zip(xs, ys))

    def __len__(self): return len(self.data)
    def __getitem__(self, idx): return self.data[idx]

def collate(tokenizer, batch):
    texts = [x for x,_ in batch]
    labels = torch.tensor([y for _,y in batch])
    enc = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=64)
    return enc, labels

def train_save(checkpoint_dir="./checkpoints/intent"):
    os.makedirs(checkpoint_dir, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased", num_labels=len(LABELS), id2label=ID2LABEL, label2id=LABEL2ID
    )

    train_ds, val_ds = TinyDataset("train"), TinyDataset("val")
    train_dl = DataLoader(train_ds, batch_size=16, shuffle=True, collate_fn=lambda b: collate(tokenizer,b))
    val_dl   = DataLoader(val_ds, batch_size=16, shuffle=False, collate_fn=lambda b: collate(tokenizer,b))

    optim = AdamW(model.parameters(), lr=5e-5)
    model.train()
    for epoch in range(3):
      for enc, labels in train_dl:
        optim.zero_grad()
        out = model(**enc, labels=labels)
        out.loss.backward(); optim.step()

    # quick eval
    model.eval(); correct=total=0
    with torch.no_grad():
      for enc, labels in val_dl:
        logits = model(**enc).logits
        pred = torch.argmax(logits, dim=-1)
        correct += (pred==labels).sum().item(); total += labels.size(0)
    acc = correct/total if total else 0.0

    model.save_pretrained(checkpoint_dir)
    tokenizer.save_pretrained(checkpoint_dir)
    with open(os.path.join(checkpoint_dir,"metrics.json"),"w") as f:
      json.dump({"val_accuracy": acc, "time": time.time()}, f)
    print(f"Saved to {checkpoint_dir} (val_acc={acc:.2f})")

if __name__=="__main__":
    train_save()
