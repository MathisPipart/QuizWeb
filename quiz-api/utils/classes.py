class Answer():
     def __init__(self, text: str, isCorrect: bool):
          self.text = text
          self.isCorrect = isCorrect

class Question():
	def __init__(self, title: str, text: str, image: str, position: int, possibleAnswers: list[Answer], id: int = None):
          self.title = title
          self.text = text
          self.image = image
          self.position = position
          self.possibleAnswers = possibleAnswers
          self.id = id
          