class Akinator:

    def __init__(self, tree=None):
        if tree and not tree.root:
            raise ValueError("Tree has not been trained yet")
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

        return self.current_question

    @property
    def current_question(self):
        if self._current_question:
            done = self._current_question.is_leaf()
            question = self._current_question.value
            return {"question": question, "done": done}
