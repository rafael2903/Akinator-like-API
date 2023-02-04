from collections import Counter

import numpy as np
import pandas as pd


class Node:
    def __init__(self, value=None, left=None, right=None, feature=None):
        # self.feature = feature
        self.left = left
        self.right = right
        self.value = value

    def is_leaf(self):
        return self.right is None and self.left is None


class DecisionTree:
    def __init__(self, features=None):
        print("features:", features)
        self.features = features
        pass

    def fit(self, X, y):
        self.root = self._build_tree(X, y)

    def predict(self, X):
        print("X:", X)
        return np.array([self._traverse_tree(x, self.root) for x in X])


    def print_tree(self, node, depth=0):
        if node is None:
            return

        if node.is_leaf():
            print("  "*depth + "Leaf Node:", node.value)
            return

        print("  "*depth + "Left:")
        self.print_tree(node.left, depth+1)
        print("  "*depth + "Right:")
        self.print_tree(node.right, depth+1)
        print("  "*depth + "depth:", depth)

    def _build_tree(self, X, y, depth=0):
        print("X_shape:", X.shape)
        n_samples, n_features = X.shape
        best_feature = self._choose_split_feature(X)

        if (len(y) == 0 and n_features == 0):
            print("entrou 1")
            return None

        if (n_features == 0 and len(y) > 0):
            print('entrou 2')
            return Node(value=y[0])

        if (n_samples == 1):
            print("entrou 3")
            return Node(value=y[0])

        # divide os dados baseado na característica e limiar selecionados
        X_left, y_left, X_right, y_right = self._split_data(X, y, best_feature)
        left_subtree = self._build_tree(X_left, y_left, depth + 1)
        right_subtree = self._build_tree(X_right, y_right, depth + 1)
        return Node(best_feature, left_subtree, right_subtree)

    def _choose_split_feature(self, X):
        best_feature = None
        best_entropy = float('inf')

        for feature in range(X.shape[1]):
            values = X[:, feature]
            entropy = abs(sum(values))

            if entropy < best_entropy:
                best_feature = feature
                best_entropy = entropy

        return best_feature

    def _split_data(self, X, y, best_feature):
        left_idx = np.where(X[:, best_feature] == -1)
        right_idx = np.where(X[:, best_feature] == 1)
        X = np.delete(X, best_feature, axis=1)

        X_left, y_left = X[left_idx], y[left_idx]
        X_right, y_right = X[right_idx], y[right_idx]

        return X_left, y_left, X_right, y_right

    def _traverse_tree(self, x, node):
        if node.is_leaf():
            return node.value
        print([node.value])
        # if x[node.value] == -1:
        #     return self._traverse_tree(x, node.left)
        # else:
        #     return self._traverse_tree(x, node.right)


ds = pd.read_csv('data copy.csv')


features = ds.columns[:-1].values
X = ds[:-1]
y = ds['name'].values

# print(X)
# print(y)

clf = DecisionTree(features)
clf.fit(X, y)

# y_pred = clf.predict(X)

# print(y)
# print(y_pred)

# clf.print_tree(clf.root)
