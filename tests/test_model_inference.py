import pytest
from app.models.torch_model import TorchModel

def test_predict_severity():
    model = TorchModel()
    # low severity example
    label, conf = model.predict_severity([0.1, 0.1])
    assert label in ("low", "medium", "high")
    assert 0.0 <= conf <= 1.0

    # higher feature values should not crash
    label2, conf2 = model.predict_severity([1.0, 0.9])
    assert label2 in ("low", "medium", "high")
    assert 0.0 <= conf2 <= 1.0
