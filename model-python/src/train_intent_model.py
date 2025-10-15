import os
import random
import torch
import numpy as np
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
from sklearn.model_selection import train_test_split
from synthetic_data import generate_samples, INTENTS
from config import config
from sklearn.metrics import accuracy_score


#Generate synthetic dataset
data = generate_samples(n_per_intent=40)
texts = [d["text"] for d in data]
labels = [list(INTENTS.keys()).index(d["intent"]) for d in data]

# Split data
train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

#Tokenizer
tokenizer = AutoTokenizer.from_pretrained(config["model_name"])

def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True, max_length=config["max_length"])

train_dataset = Dataset.from_dict({"text": train_texts, "label": train_labels})
val_dataset = Dataset.from_dict({"text": val_texts, "label": val_labels})
train_dataset = train_dataset.map(tokenize, batched=True)
val_dataset = val_dataset.map(tokenize, batched=True)

#Model initialization
num_labels = len(INTENTS)
model = AutoModelForSequenceClassification.from_pretrained(
    config["model_name"], num_labels=num_labels
)

torch.manual_seed(42)
np.random.seed(42)
random.seed(42)

model.config.hidden_dropout_prob = 0.2
model.config.attention_probs_dropout_prob = 0.2

#Training arguments
args = TrainingArguments(
    output_dir="./models/intent_classifier",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=config["learning_rate"],
    per_device_train_batch_size=config["batch_size"],
    per_device_eval_batch_size=config["batch_size"],
    num_train_epochs=config["epochs"],
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    logging_dir="./logs",
    logging_steps=10,
)

#Compute accuracy
def compute_metrics(eval_pred):
    preds, labels = eval_pred
    preds = preds.argmax(-1)
    return {"accuracy": accuracy_score(labels, preds)}

#Trainer
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

#Train
trainer.train()

#Save model
save_dir = "./models/intent_classifier"
os.makedirs(save_dir, exist_ok=True)
trainer.save_model(save_dir)
tokenizer.save_pretrained(save_dir)

print(f"✅ Model saved at {save_dir}")
