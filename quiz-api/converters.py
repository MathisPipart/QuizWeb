import classes

def questionToJSON(question):
    return {
        "id": question.id,
        "text": question.text,
        "title": question.title,
        "image": question.image,
        "position": question.position,
        "possibleAnswers": [
            {
                "text": answer.text,
                "isCorrect": bool(answer.isCorrect)
            } for answer in question.possibleAnswers
        ]
    }
    
def JSONToQuestion(json):
    return classes.Question(
        json["title"],
        json["text"],
        json["image"],
        json["position"],
        [
            classes.Answer(answer["text"], answer["isCorrect"])
            for answer in json["possibleAnswers"]
        ]
    )