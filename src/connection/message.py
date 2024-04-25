class Message:
    def __init__(self, title="", content=""):
        self._title = title
        self._content = content

    def get_title(self):
        return self._title

    def get_content(self):
        return self._content
