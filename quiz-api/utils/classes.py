class Answer():
     def __init__(self, text: str, isCorrect: bool, id: int = None):
          self.text = text
          self.isCorrect = isCorrect
          self.id = id

class Question():
	def __init__(self, title: str, text: str, image: str, position: int, possibleAnswers: list[Answer], id: int = None):
          self.title = title
          self.text = text
          self.image = image
          self.position = position
          self.possibleAnswers = possibleAnswers
          self.id = id
          