import numpy as np
from sklearn.tree import DecisionTreeClassifier
from collections import Counter
from asciitree import LeftAligned
from asciitree.drawing import BoxStyle, BOX_LIGHT

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, label=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.label = label

    def is_leaf(self):
        return self.right is None and self.left is None

class CharacterDecisionTree:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth

    def fit(self, X, y):
        self.root = self._build_tree(X, y)

    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])

    def print_tree(self, node, depth=0):
        if node is None:
            return

        if node.is_leaf():
            print("  "*depth + "Leaf Node:", node.label)
            return

        print("  "*depth + "Feature:", node.feature)
        print("  "*depth + "Threshold:", node.threshold)
        print("  "*depth + "Left:")
        self.print_tree(node.left, depth+1)
        print("  "*depth + "Right:")
        self.print_tree(node.right, depth+1)
        print("  "*depth + "depth:", depth)

    def _build_tree(self, X, y, depth=0):

        n_samples, n_features = X.shape

        n_labels = len(np.unique(y))
        print ("X:", X)
        print ("y:", y)
        print("Xshape:", X.shape)

        print(depth)
        # print("n_samples:", n_samples)
        print("n_features:", n_features)
        # print("n_labels:", n_labels)
        # print("set(y):", set(y))

        # caso base 1: atingimos o limite de profundidade
        if self.max_depth is not None and depth >= self.max_depth:
            return Node(label=np.max(Counter(y)))

        # caso base 2: todas as amostras pertencem a mesma classe
        if len(set(y)) == 1:
            return Node(label=y[0])

        if (n_features == 1):
            print("n_features == 1")

        if (n_features == 1 and len(set(X[:0])) == 1):
            return Node(label=y[0])

        if n_samples == 0:
            return None

        # caso base 3: não há mais características para dividir
        if n_features == 0:
            return Node(label=y[0])


        # seleciona a melhor característica e limiar para dividir os dados
        best_feature, best_threshold = self._choose_split_feature(X, y)

        print("best_feature:", best_feature)
        print("best_threshold:", best_threshold)

        # divide os dados baseado na característica e limiar selecionados
        left_idx, right_idx = self._split_data(X[:, best_feature], best_threshold)
        X = np.delete(X, best_feature, axis=1)

        X_left, y_left = X[left_idx, :], y[left_idx]
        X_right, y_right = X[right_idx, :], y[right_idx]
        print("X_left:", X_left)
        print("X_right:", X_right)

        # constrói a subárvore recursivamente
        left_subtree = self._build_tree(X_left, y_left, depth + 1)
        right_subtree = self._build_tree(X_right, y_right, depth + 1)

        # retorna a raiz da subárvore construída
        return Node(best_feature, best_threshold, left_subtree, right_subtree)

    def _choose_split_feature(self, X, y):
        best_feature = None
        best_threshold = None
        best_entropy = float('inf')

        for feature in range(X.shape[1]):
            values = X[:, feature]
            for threshold in set(values):
                left_idx, right_idx = self._split_data(values, threshold)

                left_entropy = self._calculate_entropy(y[left_idx])
                right_entropy = self._calculate_entropy(y[right_idx])

                total_entropy = (len(left_idx) / len(y)) * left_entropy + (len(right_idx) / len(y)) * right_entropy

                if total_entropy < best_entropy:
                    best_feature = feature
                    best_threshold = threshold
                    best_entropy = total_entropy

        return best_feature, best_threshold

    def _split_data(self, values, threshold):
        left_idx = np.where(values <= threshold)[0]
        right_idx = np.where(values > threshold)[0]
        return left_idx, right_idx

    def _calculate_entropy(self, labels):
        n_labels = len(labels)
        if n_labels <= 1:
            return 0
        counts = dict(Counter(labels))
        probs = [counts[i]/n_labels for i in counts]
        entropy = -np.sum([p * np.log2(p) for p in probs if p != 0])
        return entropy

        # counts = np.count_nonzero(y == x)
        # labels = labels.astype(np.int)

    def _traverse_tree(self, x, node):
        if node.is_leaf():
            return node.label

        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        else:
            return self._traverse_tree(x, node.right)

import json
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd
# Carregar os dados do arquivo JSON
# with open('characters.json', 'r') as f:
    # data = json.load(f)

ds = pd.read_csv('data copy.csv')


X = ds.iloc[:, 0:5].values
y = ds['name'].values

print(X)
print(y)
# Separar características e rótulos
# X = [[character['height'], character['weight'], character['age'], character['gender'] == 'male'] for character in data['characters']]
# y = [character['name'] for character in data['characters']]

# Dividir os dados em conjunto de treinamento e teste
# X = np.array(X)
# y = np.array(y)

# Treinar a árvore de decisão
clf = CharacterDecisionTree()
clf.fit(X, y)

# Testar a precisão da árvore
y_pred = clf.predict(X)

print(y)
print(y_pred)

# print(accuracy_score(y, y_pred))

clf.print_tree(clf.root)
# tree.plot_tree(clf)
