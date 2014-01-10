from collections import deque
class Story:
    def __init__(self, story_id, title, first_word):
        self._story_id = story_id
        self._title = title
        self._first_word = first_word
        self._story = []

        # Recursive tree building
        todo = deque(self._first_word])
        while todo:
            current = todo.popleft()
    def _build_tree(self,word):
        for child in word.children():
            # _build_tree
    def story_id(self):
        return self._story_id
    def title(self):
        return self._title
    
    def story(self):
        return ' '.join(self._story)
