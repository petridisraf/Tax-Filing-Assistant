from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TaxInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    income = db.Column(db.Float, nullable=False)
    expenses = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<TaxInfo {self.id}>"
