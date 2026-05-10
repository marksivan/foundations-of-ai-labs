from dataset import load_dataset

X, y = load_dataset("dataset.pkl")

print("samples:", len(X))

print("\nfirst sample board:")
print(X[0])

print("\nfirst label (move):")
print(y[0])