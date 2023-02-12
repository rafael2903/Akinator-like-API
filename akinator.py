from tree import BinaryDecisionTreeClassifier, Node


class Akinator:
    id = 0

    def __init__(self, tree=None):
        if tree and not tree.root:
            raise ValueError("Tree has not been trained yet")

        self.id = Akinator.id
        Akinator.id += 1

        self._current_question = tree.root if tree else None
        self.not_sure_nodes = []

    def answer_question(self, answer):
        if answer not in [-1, 1, 0]:
            raise ValueError("Answer must be -1, 1 or 0")

        if self._current_question.is_leaf():
            return self.current_question

        if answer == 1:
            self._current_question = self._current_question.right
        elif answer == -1:
            self._current_question = self._current_question.left
        else:
            direction, node = BinaryDecisionTreeClassifier.get_deepest_subtree(
                self._current_question)
            self.not_sure_nodes.append((direction, self._current_question))
            self._current_question = node

        return self.current_question

    def add_person(self, name, feature):
        if not self._current_question.is_leaf():
            return

        old_person = Node(self._current_question.value)
        new_person = Node(name)

        self._current_question.value = f"É {feature.lower()}?"
        self._current_question.left = old_person
        self._current_question.right = new_person

    def get_progress(self):
        sub_tree_depth = BinaryDecisionTreeClassifier.get_max_depth_from_node(
            self._current_question) - 1
        total_depth = self._current_question.depth + sub_tree_depth
        progress = self._current_question.depth / total_depth
        return round(progress, 2)

    def continue_game(self):
        if not self.not_sure_nodes:
            return {"question": None, "done": True, "progress": 1.0}

        if not self._current_question.is_leaf():
            return self.current_question

        taken_direction, not_sure_node = self.not_sure_nodes.pop()

        if taken_direction == 'left':
            self._current_question = not_sure_node.right
        else:
            self._current_question = not_sure_node.left

        return self.current_question

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
        "t": 0
    }

    while True:
        print(f"É {akinator.current_question['question']}?")
        answer = input('s/n/t: ')
        answer = possible_answers[answer]
        akinator.answer_question(answer)

        if akinator.current_question['done']:
            print(
                f"Eu acho que você pensou em... {akinator.current_question['question']}")
            confirm = input('É essa pessoa? (s/n): ')
            if confirm == 's':
                print('Acertei!')
                break
            else:
                if akinator.continue_game()['done']:
                    print('Não sei quem é essa pessoa :(')
                    name = input('Qual o nome dessa pessoa? ')
                    feature = input('Qual característica essa pessoa tem? ')
                    akinator.add_person(name, feature)
                    break
                else:
                    print('Vamos continuar')
