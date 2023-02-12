from akinator import Akinator
from fastapi import FastAPI
from pydantic import BaseModel

from tree import BinaryDecisionTreeClassifier

app = FastAPI()

tree = BinaryDecisionTreeClassifier('tree.json')

sessions = {}


class AnswerBody(BaseModel):
    answer: int


class AddPersonBody(BaseModel):
    name: str
    feature: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/start")
def start():
    akinator = Akinator(tree)
    sessions[akinator.id] = akinator

    return {"session_id": akinator.id, "question": akinator.current_question}


@app.post("/answer/{session_id}")
def answer(session_id: int, body: AnswerBody):
    akinator = sessions[session_id]
    return akinator.answer_question(body.answer)


@app.post("/person/{session_id}")
def add_person(session_id: int, body: AddPersonBody):
    akinator = sessions[session_id]
    akinator.add_person(body.name, body.feature)

@app.post("/continue/{session_id}")
def continue_game(session_id: int):
    akinator = sessions[session_id]
    return akinator.continue_game()
