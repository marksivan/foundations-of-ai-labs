import torch
from torch.nn import Parameter
from datagen import generate_data, visualize
from datagen import compute_linear_outcome
from datagen import compute_nonlinear_outcome
from descent import gradient_descent


class LogisticRegressionModel(torch.nn.Module):
    def __init__(self, random_init=True):
        super().__init__()
        if random_init:
            self.theta = Parameter(torch.empty(3))
            for param in self.parameters():
                torch.nn.init.uniform_(param, a=-1.3, b=1.3)
        else:
            self.theta = Parameter(torch.tensor([3.0, 4.0, 5.0]))

    def forward(self, x, y=None):
        raise NotImplementedError(
            "The forward method of LogisticRegressionModel has not been implemented."
        )


def run_gradient_descent(model, data, test_data=None, batch_size=4, num_iters=1):
    def report_progress(iteration, preds, loss):
        if test_data is not None and iteration % 5 == 0:  # visualize every 5 steps
            xs = [datum[0] for datum in test_data]
            xs_pt = torch.stack([datum[0] for datum in test_data])
            predictions, _ = model.forward(xs_pt)
            visualize(list(zip(xs, predictions)))

    gradient_descent(
        model,
        data,
        batch_size=batch_size,
        report_progress_fn=report_progress,
        num_iters=num_iters,
    )


if __name__ == "__main__":
    from examples import DISEASE_DATA

    model = LogisticRegressionModel()
    run_gradient_descent(model, DISEASE_DATA, batch_size=3, num_iters=1000)
    exit()
    import argparse

    parser = argparse.ArgumentParser(description="Train machine learning models.")
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        choices=["linear", "nonlinear"],
        help="Type of data to generate: 'linear', or 'nonlinear'",
    )
    args = parser.parse_args()

    if args.type == "linear":
        data = generate_data(compute_linear_outcome, 50000)
        test_data = generate_data(compute_linear_outcome, 5000)
    else:
        data = generate_data(compute_nonlinear_outcome, 50000)
        test_data = generate_data(compute_nonlinear_outcome, 5000)

    model = LogisticRegressionModel()
    run_gradient_descent(model, data, test_data)
