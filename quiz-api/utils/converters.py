from utils.classes import Question, Answer

def questionToJSON(question):
    return {
        "id": question.id,
        "text": question.text,
        "title": question.title,
        "image": question.image,
        "position": question.position,
        "possibleAnswers": [
            {
                "id": answer.id,
                "text": answer.text,
                "isCorrect": bool(answer.isCorrect)
            } for answer in question.possibleAnswers
        ]
    }
    
def JSONToQuestion(json):
    return Question(
        json["title"],
        json["text"],
        json["image"],
        json["position"],
        [
            Answer(answer["text"], answer["isCorrect"])
            for answer in json["possibleAnswers"]
        ]
    )