import torch
from toe.tictactoe import compile_playbook
from toe.tictactoe import optimal_player_fn
from toe.tictactoe import play_tournament


def convert_board_state_to_vector(board, next_move):
    x = []

    # bias
    x.append(1.0)

    #  Move (9 positions)
    for i in range(9):
        if i == next_move:
            x.append(1.0)
        else:
            x.append(0.0)

    for cell in board:
        if cell == 0:      # empty
            x += [1.0, 0.0, 0.0]
        elif cell == 1:    # X
            x += [0.0, 1.0, 0.0]
        else:              # O
            x += [0.0, 0.0, 1.0]

    return torch.tensor(x)


def load_training_data(playbook):
    X = []
    y = []

    for board, good_moves in playbook.items():
        for move in range(9):
            # only consider empty cells
            if board[move] == 0:
                # create feature vector
                vec = convert_board_state_to_vector(board, move)
                X.append(vec)

                #  1 if good move, else 0
                if move in good_moves:
                    y.append(1.0)
                else:
                    y.append(0.0)

    # convert to tensors
    X = torch.stack(X)          # shape (N, 37)
    y = torch.tensor(y)         # shape (N,)

    return X, y


def initialize_params(input_dim=37, hidden_dim=64):
    theta1 = torch.zeros(hidden_dim, input_dim)
    theta2 = torch.zeros(hidden_dim, hidden_dim)
    theta3 = torch.zeros(1, hidden_dim)
    for theta in [theta1, theta2, theta3]:
        theta.uniform_(-0.4, 0.4)
        theta.requires_grad = True
    return {"theta1": theta1, "theta2": theta2, "theta3": theta3}



def run_neural_net(parameters, X):
    theta1 = parameters["theta1"]
    theta2 = parameters["theta2"]
    theta3 = parameters["theta3"]

    # layer 1
    z1 = X @ theta1.T
    a1 = torch.relu(z1)

    # layer 2
    z2 = a1 @ theta2.T
    a2 = torch.relu(z2)

    # output layer
    z3 = a2 @ theta3.T
    output = torch.sigmoid(z3)

    return output.squeeze()

def compute_loss(output, y):
    # to avoid log(0)
    eps = 1e-8

    loss = - (y * torch.log(output + eps) + 
              (1 - y) * torch.log(1 - output + eps))

    return loss.mean()


def evaluate_neural_net(parameters, x, y):
    accuracy = compute_nn_accuracy(parameters, x, y)
    ai_player_fn = create_nn_player_fn(parameters)
    wins, losses, ties = play_tournament(50, ai_player_fn, optimal_player_fn)
    accuracy_msg = f"Train accuracy: {accuracy: .3f}"
    tournament_msg = f"Tournament performance: {wins}-{losses}-{ties}"
    print(accuracy_msg + "; " + tournament_msg)


def compute_nn_accuracy(parameters, x, y):
    # get predictions (probabilities)
    output = run_neural_net(parameters, x)

    # convert to 0 or 1
    preds = (output >= 0.5).float()

    # compare with true labels
    correct = (preds == y).float()

    return correct.mean().item()


def create_nn_player_fn(parameters):
    def player_fn(board):
        best_move = None
        best_score = -1

        for move in range(9):
            if board[move] == 0:  # legal move
                vec = convert_board_state_to_vector(board, move).unsqueeze(0)
                score = run_neural_net(parameters, vec).item()

                if score > best_score:
                    best_score = score
                    best_move = move

        return best_move

    return player_fn



def train_model(num_steps=100000, learning_rate=0.02, batch_size=128):
    X_train, y_train = load_training_data(compile_playbook())
    parameters = initialize_params()
    batch_start = 0
    for step in range(num_steps):
        if step % 5000 == 0:  # we evaluate every 5000 steps
            evaluate_neural_net(parameters, X_train, y_train)
        X_batch = X_train[batch_start : batch_start + batch_size, :]
        vy_batch = y_train[batch_start : batch_start + batch_size]
        output = run_neural_net(parameters, X_batch)
        loss = compute_loss(output, y_batch)
        loss.backward()
        with torch.no_grad():
            for theta in parameters.values():
                theta -= learning_rate * theta.grad
                theta.grad = None
        batch_start = (batch_start + batch_size) % X_train.shape[0]


if __name__ == "__main__":
    train_model()
