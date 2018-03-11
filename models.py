from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
	__tablename__ = 'tasks'
	task_ID = db.Column(db.Integer, primary_key = True)
	task_title = db.Column(db.String, nullable=False)
	task_detail = db.Column(db.String, nullable=False)
	assigned_ID = db.Column(db.String, nullable=False)
	deadline = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	completed = db.Column(db.Boolean, nullable=False, default=False)

	def __init__(self, task_ID, task_title, task_detail, assigned_ID, deadline):
		self.task_ID = task_ID
		self.task_title = task_title
		self.task_detail = task_detail
		self.assigned_ID = assigned_ID
		self.deadline = deadline

	def __repr__(self):
		return '<title{}'.format(self.name)

class User(db.Model):
	__tablename__ = 'users'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	fullname = db.Column(db.String)
	groups = db.Column(postgresql.ARRAY(db.Integer))

	def __init__(self, user_id, user_name, user_fullname):
		self.id = user_id
		self.name = user_name
		self.fullname = user_fullname

    def __repr__(self):
        return "<User(name='%s', fullname='%s')>" % (self.name, self.fullname)


