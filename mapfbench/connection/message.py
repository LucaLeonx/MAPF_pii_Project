class Message:
    def __init__(self, title="", content=""):
        self._title = title
        self._content = content

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    def to_dict(self):
        return {"title": self._title, "content": self._content}

    @staticmethod
    def from_dict(dictionary):
        return Message(dictionary["title"], dictionary["content"])
