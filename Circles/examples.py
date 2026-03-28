import torch
from torch.nn import Parameter
from descent import gradient_descent


class ExampleFunctionGraph1(torch.nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, u, v):
        x = u + 0
        y = u + v
        z = x + y
        return z


class ExampleFunctionGraph2(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.theta = Parameter(torch.tensor([-2.0, 100.0], requires_grad=True))

    def forward(self, x, y):
        predictions = self.theta @ x.t()
        loss = ((predictions - y) ** 2).sum()
        return predictions, loss


def compute_gradients_for_example1():
    g = ExampleFunctionGraph1()
    u = torch.tensor(3.0, requires_grad=True)
    v = torch.tensor(4.0, requires_grad=True)
    y = g(u, v)
    y.backward()
    print(f"y = {y}")
    print(f"dy/du = {u.grad}")
    print(f"dy/dv = {v.grad}")


def compute_gradients_for_example2():
    g = ExampleFunctionGraph2()
    x = torch.tensor([[0.72, 0.06], [0.34, 0.25], [0.17, 0.57]])
    y = torch.tensor([20.0, 28.0, 41.0])
    preds, loss = g(x, y)
    print(f"preds      = {preds}")
    print(f"l          = {loss}")
    loss.backward()
    print(f"dl/d_theta = {g.theta.grad}")


def optimize_example2(num_iters):
    def report_progress(iteration, preds, loss):
        print(f"loss at iter {iteration}: {loss:.2f}")
        preds = [float(f"{p:.2f}") for p in preds.tolist()]
        print(f"  age predictions: {preds}")

    data = [
        (torch.tensor([0.72, 0.06]), torch.tensor(20.0)),
        (torch.tensor([0.34, 0.25]), torch.tensor(28.0)),
        (torch.tensor([0.17, 0.57]), torch.tensor(41.0)),
    ]
    model = ExampleFunctionGraph2()
    gradient_descent(
        model, data, num_iters=num_iters, report_progress_fn=report_progress
    )
    print(f"final parameters: {model.theta}")


DISEASE_DATA = [
    (torch.tensor([1.0, 6.4, 1.20]), torch.tensor(1)),
    (torch.tensor([1.0, 6.0, 2.00]), torch.tensor(0)),
    (torch.tensor([1.0, 5.5, 1.20]), torch.tensor(0)),
    (torch.tensor([1.0, 5.0, 2.50]), torch.tensor(0)),
    (torch.tensor([1.0, 6.6, 2.60]), torch.tensor(0)),
    (torch.tensor([1.0, 7.0, 1.50]), torch.tensor(1)),
]


def optimize_disease_data(num_iters):
    def report_progress(iteration, preds, loss):
        print(f"loss at iter {iteration}: {loss:.2f}")
        preds = [float(f"{p:.2f}") for p in preds.tolist()]
        print(f"  predictions: {preds}")

    from models import LogisticRegressionModel

    model = LogisticRegressionModel()
    gradient_descent(
        model, DISEASE_DATA, num_iters=num_iters, report_progress_fn=report_progress
    )
    print(f"final parameters: {model.theta}")


if __name__ == "__main__":
    optimize_disease_data(2000)
