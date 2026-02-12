from torch_geometric.datasets import Amazon
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt 

dataset = Amazon(root='/tmp/Amazon', name='Computers')
data = dataset[0]

print(f'Total Products (Nodes): {data.num_nodes}')
print(f'Total Co-Purchases (Edges): {data.num_edges}')
print(f'Features per Product: {dataset.num_node_features}')
print(f'Number of Categories to Predict: {dataset.num_classes}')


class AmazonGCN(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super(AmazonGCN, self).__init__()
        # First layer: Takes input features and compresses them into a hidden representation
        self.conv1 = GCNConv(num_features, 64)
        # Second layer: Produces the final category prediction
        self.conv2 = GCNConv(64, num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        
        # Pass through first layer with ReLU activation
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.5, training=self.training)
        
        # Pass through second layer
        x = self.conv2(x, edge_index)
        
        return F.log_softmax(x, dim=1)
    
model = AmazonGCN(num_features=dataset.num_node_features, num_classes=dataset.num_classes)
print(model)

# Set the optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

# Create indices
num_nodes = data.num_nodes
indices = np.arange(num_nodes)
np.random.shuffle(indices)

# Defining split size
train_size = int(0.6 * num_nodes)
val_size = int(0.2 * num_nodes)

# Create boolean masks
data.train_mask = torch.zeros(num_nodes, dtype=torch.bool)
data.val_mask = torch.zeros(num_nodes, dtype=torch.bool)
data.test_mask = torch.zeros(num_nodes, dtype=torch.bool)

data.train_mask[indices[:train_size]] = True
data.val_mask[indices[train_size:train_size+val_size]] = True
data.test_mask[indices[train_size+val_size:]] = True

def train():
    model.train()
    optimizer.zero_grad()
    out = model(data)
    
    loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()
    return loss.item()

def test():
    model.eval()
    logits, accs = model(data), []
    for mask in [data.train_mask, data.val_mask, data.test_mask]:
        pred = logits[mask].max(1)[1]
        acc = pred.eq(data.y[mask]).sum().item() / mask.sum().item()
        accs.append(acc)
    return accs

# Run training for 200 epochs and select the best epoch
best_val_acc = 0
for epoch in range(1, 201):
    loss = train()
    train_acc, val_acc, test_acc = test()
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), 'best_model.pth')
    
model.eval()
out = model(data)
pred = out[data.test_mask].max(1)[1].cpu().numpy()
true = data.y[data.test_mask].cpu().numpy()

cm = confusion_matrix(true, pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Category')
plt.ylabel('Actual Category')
plt.title('Amazon GCN: Confusion Matrix')
plt.savefig('confusion_matrix.png')
