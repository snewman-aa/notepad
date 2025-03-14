from notepad_app import db
import datetime


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    comments = db.relationship('Comment', backref='note',
                               cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f"<Note id={self.id}, name='{self.name}'>"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)

    def __repr__(self):
        return (f"<Comment id={self.id},"
                f" note_name='{self.note.name[:20]}...',"
                f" created_at={self.created_at}>")