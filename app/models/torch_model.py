import torch
import torch.nn as nn
import numpy as np
from typing import Sequence, Tuple
from app.utils.logging import logger


class SimpleClassifier(nn.Module):
    def __init__(self, in_features: int = 2, hidden: int = 8):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 3),  # 3 classes: low, medium, high
            nn.Softmax(dim=-1)
        )

    def forward(self, x):
        return self.net(x)


class TorchModel:
    LABELS = ["low", "medium", "high"]

    def __init__(self, model_path: str = None):
        self.device = torch.device("cpu")
        self.model = SimpleClassifier()
        if model_path:
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                logger.info("Loaded model from %s", model_path)
            except Exception as exc:
                logger.warning("Failed to load model %s: %s. Using fresh weights.", model_path, exc)
        self.model.to(self.device)
        self.model.eval()

    def predict_severity(self, features: Sequence[float]) -> Tuple[str, float]:
        arr = np.array(features, dtype=np.float32).reshape(1, -1)
        with torch.no_grad():
            t = torch.from_numpy(arr).to(self.device)
            out = self.model(t).cpu().numpy().flatten()
        idx = int(out.argmax())
        confidence = float(out[idx])
        label = self.LABELS[idx]
        return label, confidence
