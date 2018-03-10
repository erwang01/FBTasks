from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Task(db.Model):
	__tablename__ = 'test_app'
	ID = db.Column(db.Integer, primary_key = True)
	task_title = db.Column(db.String, nullable=False)

	def __init__(self, ID, task_title):
		self.ID = ID
		self.task_title = task_title

	def __repr__(self):
		return '<title{}'.format(self.name)


