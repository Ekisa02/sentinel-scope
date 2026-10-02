import argparse
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from app.models.torch_model import SimpleClassifier

# This script demonstrates training a tiny model on synthetic data.
# The dataset is artificial and intended for demo/training purposes only.

def synthetic_dataset(n=2000):
    X = []
    y = []
    for _ in range(n):
        ttype = np.random.choice([0.1, 0.2, 0.8, 1.0])
        conf = np.random.rand() * 0.6 + 0.2
        features = [ttype, conf]
        # label heuristic: high severity when ttype is large and confidence > 0.6
        if ttype >= 0.8 and conf > 0.6:
            label = 2
        elif conf > 0.4:
            label = 1
        else:
            label = 0
        X.append(features)
        y.append(label)
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int64)


def train(epochs=5, out="models/demo_model.pt"):
    X, y = synthetic_dataset()
    model = SimpleClassifier()
    opt = optim.Adam(model.parameters(), lr=1e-2)
    loss_fn = nn.CrossEntropyLoss()

    for ep in range(epochs):
        model.train()
        idx = np.random.permutation(len(X))
        X = X[idx]
        y = y[idx]
        losses = []
        for i in range(0, len(X), 64):
            xb = torch.tensor(X[i:i+64])
            yb = torch.tensor(y[i:i+64])
            opt.zero_grad()
            out = model(xb)
            loss = loss_fn(out, yb)
            loss.backward()
            opt.step()
            losses.append(loss.item())
        print(f"Epoch {ep+1}/{epochs}, loss={float(sum(losses)/len(losses)):.4f}")

    torch.save(model.state_dict(), out)
    print(f"Saved model to {out}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--epochs", type=int, default=5)
    p.add_argument("--out", default="models/demo_model.pt")
    args = p.parse_args()
    train(epochs=args.epochs, out=args.out)
