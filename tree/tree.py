import jsons
import numpy as np


class Node:

    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.right is None and self.left is None

    def print_node(self, depth=0):
        if self is None:
            return

        if self.is_leaf():
            print("  "*depth + "Leaf Node:", self.value)
            return

        print("  "*depth + "Left:")
        self.left.print_node(depth+1)
        print("  "*depth + "Right:")
        self.right.print_node(depth+1)
        print("  "*depth + "depth:", depth)
        print("  "*depth + "value:", self.value)

    @staticmethod
    def from_dict(dict):
        if dict is None:
            return None

        node = Node(dict['value'])
        node.right = Node.from_dict(dict['right'])
        node.left = Node.from_dict(dict['left'])
        return node


class BinaryDecisionTreeClassifier:

    def __init__(self, filename=None):
        self.root = None

        if filename is not None:
            self.load(filename)

    def fit(self, X, y):
        self.root = self._build_tree(X, y)

    def predict(self, X):
        return np.array([self._traverse_tree(X.iloc[i], self.root) for i in range(len(X))])

    def print_tree(self):
        if self.root is None:
            return
        self.root.print_node()

    def _drop_features_with_same_values(self, X):
        for feature in X.columns:
            if len(set(X[feature])) == 1:
                X = X.drop(columns=feature)
        return X

    def _build_tree(self, X, y, depth=0):
        X = self._drop_features_with_same_values(X)
        n_samples, n_features = X.shape

        if n_features == 0 and len(y) > 0:
            return BinaryDecisionTreeClassifier.create_subtree_from_names_list(y)

        if n_features == 0 and len(y) == 1:
            return Node(y[0])

        if len(y) == 0:
            return Node()

        if n_samples == 1:
            return Node(y[0])

        best_feature = self._choose_split_feature(X)
        X_left, y_left, X_right, y_right = self._split_data(X, y, best_feature)

        left_subtree = self._build_tree(X_left, y_left, depth + 1)
        right_subtree = self._build_tree(X_right, y_right, depth + 1)

        return Node(best_feature, left_subtree, right_subtree)

    @staticmethod
    def create_subtree_from_names_list(names_list):
        if len(names_list) == 0:
            return Node()

        if len(names_list) == 1:
            return Node(names_list[0])

        left_subtree = BinaryDecisionTreeClassifier.create_subtree_from_names_list(
            names_list[1:])
        right_subtree = BinaryDecisionTreeClassifier.create_subtree_from_names_list(
            names_list[:1])

        return Node(names_list[0], left_subtree, right_subtree)

    def _choose_split_feature(self, X):
        best_feature = None
        best_entropy = float('inf')

        for feature in X.columns:
            values = X[feature].values
            entropy = abs(sum(values))

            if entropy < best_entropy:
                best_feature = feature
                best_entropy = entropy

        return best_feature

    def _split_data(self, X, y, best_feature):
        left_idx, = np.where(X[best_feature] == -1)
        right_idx, = np.where(X[best_feature] == 1)

        X = X.drop(columns=best_feature)

        X_left = X.iloc[left_idx]
        X_right = X.iloc[right_idx]

        y_left = y[left_idx]
        y_right = y[right_idx]

        return X_left, y_left, X_right, y_right

    def _traverse_tree(self, x, node):
        if node.is_leaf():
            return node.value

        if x[node.value] == -1:
            return self._traverse_tree(x, node.left)
        else:
            return self._traverse_tree(x, node.right)

    def load(self, filename='tree.json'):
        with open(filename, 'r') as f:
            dict = jsons.loads(f.read())

        self.root = Node.from_dict(dict['root'])

    def dump(self, filename='tree.json'):
        json = jsons.dumps(self)
        with open(filename, 'w') as f:
            f.write(str(json))

    def drop(self):
        self.root = None
