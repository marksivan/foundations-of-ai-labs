import torch
import matplotlib.pyplot as plt


def generate_data(outcome_fn, N):
    data = []
    while len(data) < N:
        x = torch.randn(3)
        x[0] = 1.0
        y = outcome_fn(x)
        if y is not None:
            datum = (x, y)
            data.append(datum)
    return data


def compute_linear_outcome(x):
    raise NotImplementedError("Function compute_linear_outcome is not yet implemented.")


def compute_nonlinear_outcome(x):
    raise NotImplementedError(
        "Function compute_nonlinear_outcome is not yet implemented."
    )


def visualize(data):
    import seaborn as sns

    xs = [datum[0] for datum in data]
    ys = [datum[1] for datum in data]
    positives = [xs[i] for i in range(len(xs)) if ys[i] == 1]
    negatives = [xs[i] for i in range(len(xs)) if ys[i] == 0]
    sns.scatterplot(
        x=[x[1].item() for x in positives],
        y=[x[2].item() for x in positives],
        color="yellow",
    )
    sns.scatterplot(
        x=[x[1].item() for x in negatives],
        y=[x[2].item() for x in negatives],
        color="blue",
    )
    plt.ion()
    plt.show()
    plt.pause(0.2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate artificial data for machine learning."
    )
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        choices=["zeros", "ones", "linear", "nonlinear"],
        help="Type of data to generate: 'trivial', 'linear', or 'nonlinear'",
    )
    args = parser.parse_args()

    if args.type == "linear":
        outcome_fn = compute_linear_outcome
    elif args.type == "nonlinear":
        outcome_fn = compute_nonlinear_outcome
    elif args.type == "zeros":
        outcome_fn = lambda x: 0
    else:
        outcome_fn = lambda x: 1

    data = generate_data(outcome_fn, 5000)
    visualize(data)
    plt.show(block=True)
