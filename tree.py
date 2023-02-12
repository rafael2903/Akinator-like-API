import jsons
import numpy as np
from treelib import Node, Tree


class Node:

    def __init__(self, value=None, left=None, right=None, depth=0):
        self.value = value
        self.left = left
        self.right = right
        self.depth = depth

    def is_leaf(self):
        return self.right is None and self.left is None

    @staticmethod
    def from_dict(dict, depth=0):
        if dict is None:
            return None

        node = Node(dict['value'], depth=depth)
        node.right = Node.from_dict(dict['right'], depth=depth + 1)
        node.left = Node.from_dict(dict['left'], depth=depth + 1)
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

        treelibTree = Tree()
        BinaryDecisionTreeClassifier.createTreelibTree(treelibTree, self.root)
        treelibTree.show()

    @staticmethod
    def createTreelibTree(tree, node, parent=None):
        if parent is None:
            tree.create_node(node.value, node)
        else:
            tree.create_node(node.value, node, parent=parent)
        if node.left is not None:
            BinaryDecisionTreeClassifier.createTreelibTree(
                tree, node.left, node)
        if node.right is not None:
            BinaryDecisionTreeClassifier.createTreelibTree(
                tree, node.right, node)

    def _drop_features_with_same_values(self, X):
        for feature in X.columns:
            if len(set(X[feature])) == 1:
                X = X.drop(columns=feature)
        return X

    def _build_tree(self, X, y, depth=0):
        X = self._drop_features_with_same_values(X)
        n_samples, n_features = X.shape

        if n_features == 0 and len(y) > 0:
            return BinaryDecisionTreeClassifier.create_subtree_from_names_list(y, depth=depth)

        if n_features == 0 and len(y) == 1:
            return Node(y[0], depth=depth)

        if len(y) == 0:
            return Node()

        if n_samples == 1:
            return Node(y[0], depth=depth)

        best_feature = self._choose_split_feature(X)
        X_left, y_left, X_right, y_right = self._split_data(X, y, best_feature)

        left_subtree = self._build_tree(X_left, y_left, depth + 1)
        right_subtree = self._build_tree(X_right, y_right, depth + 1)

        return Node(best_feature, left_subtree, right_subtree, depth=depth)

    @staticmethod
    def create_subtree_from_names_list(names_list, depth=0):
        if len(names_list) == 0:
            return Node()

        if len(names_list) == 1:
            return Node(names_list[0], depth=depth)

        left_subtree = BinaryDecisionTreeClassifier.create_subtree_from_names_list(
            names_list[1:], depth=depth+1)
        right_subtree = BinaryDecisionTreeClassifier.create_subtree_from_names_list(
            names_list[:1], depth=depth+1)

        return Node(f"É {names_list[0]}?", left_subtree, right_subtree, depth=depth)

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

    @staticmethod
    def get_max_depth_from_node(node):
        if node.value is None:
            return 0

        if node.is_leaf():
            return 1

        return 1 + max(BinaryDecisionTreeClassifier.get_max_depth_from_node(node.left),
                       BinaryDecisionTreeClassifier.get_max_depth_from_node(node.right))

    @staticmethod
    def get_deepest_subtree(node):
        if node.is_leaf():
            return node

        left = BinaryDecisionTreeClassifier.get_max_depth_from_node(node.left)
        right = BinaryDecisionTreeClassifier.get_max_depth_from_node(
            node.right)

        if left > right:
            return 'left', node.left
        else:
            return 'right', node.right
