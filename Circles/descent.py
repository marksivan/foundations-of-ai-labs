import torch
from torch.utils.data import DataLoader

def gradient_descent(model, data, num_iters=1, batch_size=None, report_progress_fn=None, learning_rate=0.1):
    if batch_size is None:
        batch_size = len(data)
    for _ in range(num_iters):
        loader = DataLoader(data, batch_size=batch_size)
        for i, (x, y) in enumerate(loader):
            preds, loss = model(x, y)
            loss.backward()
            for param in model.parameters():
                with torch.no_grad():
                    param -= learning_rate * param.grad
                    param.grad = None
            if report_progress_fn is not None:
                report_progress_fn(i, preds, loss)
    return loss
