from akinator import Akinator
from fastapi import FastAPI

from tree import BinaryDecisionTreeClassifier

app = FastAPI()

tree = BinaryDecisionTreeClassifier('tree.json')

executions = {}

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/start")
def start():
    akinator = Akinator(tree)
    executions[akinator.id] = akinator

    return {"id": akinator.id, "question": akinator.current_question}


@app.post("/answer/{id}")
def answer(id: int, answer: int):
    akinator = executions[id]
    return akinator.answer_question(answer)
