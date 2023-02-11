from tree import BinaryDecisionTreeClassifier, Node


class Akinator:
    id = 0

    def __init__(self, tree=None):
        if tree and not tree.root:
            raise ValueError("Tree has not been trained yet")

        self.id = Akinator.id
        Akinator.id += 1

        self.current_node_depth = 0
        self._current_question = tree.root if tree else None

    def answer_question(self, answer):
        if answer not in [-1, 1]:
            raise ValueError("Answer must be -1 or 1")

        if self.current_question['done']:
            return self.current_question

        if answer == -1:
            self._current_question = self._current_question.left
        else:
            self._current_question = self._current_question.right

        self.current_node_depth += 1

        return self.current_question

    def add_person(self, name, feature):
        if not self.current_question['done']:
            return

        old_person = Node(self._current_question.value)
        new_person = Node(name)

        self._current_question.value = feature
        self._current_question.left = old_person
        self._current_question.right = new_person

    def get_progress(self):
        sub_tree_depth = BinaryDecisionTreeClassifier.get_max_depth_from_node(
            self._current_question) - 1
        total_depth = self.current_node_depth + sub_tree_depth
        progress = self.current_node_depth / total_depth
        return round(progress, 2)

    @property
    def current_question(self):
        if self._current_question:
            done = self._current_question.is_leaf()
            question = self._current_question.value
            progress = self.get_progress()
            return {"question": question, "done": done, "progress": progress}


if __name__ == "__main__":

    tree = BinaryDecisionTreeClassifier('tree.json')
    akinator = Akinator(tree)

    possible_answers = {
        "n": -1,
        "s": 1,
    }

    while True:
        print(f"É {akinator.current_question['question']}?")
        answer = input('s/n: ')
        answer = possible_answers[answer]
        akinator.answer_question(answer)

        if akinator.current_question['done']:
            print(akinator.current_question['question'])
            break
