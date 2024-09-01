

class ExampleBase(object):
    def __init__(self, input: str, output: str) -> None:
        self.input = input
        self.output = output


    def __str__(self) -> str:
        return f"EXAMPLE TASK: {self.input} EXAMPLE OUTPUT: {self.output}\n"
    


if __name__ == "__main__":
    example = ExampleBase('xxx', 'xxx')
    print(example)
 