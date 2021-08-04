from app import db

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False,unique=True)



#     marvel_id = db.Column(db.Integer, nullable=True, unique=True)
#     hero_description = db.Column(db.String(500), nullable=True, unique=True)
#     stories = db.relationship('Story', backref='hero', lazy=True)

# class Story(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     story_title = db.Column(db.String(500), nullable=False)
#     hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
# >>> from app import db
# >>> from app.models import Hero, Story
# >>> db.create_all()
