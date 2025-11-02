import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import KFold
from dataset import CustomVTKDataset
from model import SimpleClassifier

# Set up KFold cross-validation
n_splits = 5
kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

dataset = CustomVTKDataset(root_dir='data')

# Define hyperparameters
num_epochs = 10
batch_size = 30
learning_rate = 0.001

# Cross-validation loop
fold_results = []
input_size = dataset[0][0].shape[0]

for fold, (train_idx, val_idx) in enumerate(kf.split(dataset)):
    print(f'Fold {fold+1}/{n_splits}')
    
    # Create data loaders for the current fold
    train_subset = Subset(dataset, train_idx)
    val_subset = Subset(dataset, val_idx)
    
    train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_subset, batch_size=batch_size, shuffle=False)
    
    # Initialize the model, loss function, and optimizer
    model = SimpleClassifier(input_size=input_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Training loop
    for epoch in range(num_epochs):
        model.train()
        for features, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(features)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
    
        print(f'Fold {fold+1}, Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}')

    # Validation
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for features, labels in val_loader:
            outputs = model(features)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    accuracy = 100 * correct / total
    fold_results.append(accuracy)
    print(f'Fold {fold+1}, Accuracy: {accuracy}%\n')

# Final cross-validated accuracy
average_accuracy = sum(fold_results) / len(fold_results)
print(f'Average Accuracy across {n_splits} folds: {average_accuracy}%')

# Save the trained model
torch.save(model.state_dict(), 'simple_classifier.pth')
print("Model saved as simple_classifier.pth")
