class ArrayStack:
    def is_empty(self):
        return len(self._data)==0
    def __len__(self):
        return len(self._data)
