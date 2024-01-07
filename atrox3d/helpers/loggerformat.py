class LoggerFormat:

    def __init__(self, *items) -> None:
        self.items = list(items)

    @classmethod
    def from_string(cls, format: str):
        obj = cls()
        obj.format = format
        return obj

    def __str__(self) -> str:
        return self.format


format = LoggerFormat.from_string('hello')
print(format)

