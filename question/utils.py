import random



def randomQuestions(value: list, size: str):
     goal = random.choices(value, k=size)
     return goal


def randomShuffle(value: list):
     output=[]
     for i in range(value):
          a = random.choices(value, k=1)
          output.append(a[0])
     return 