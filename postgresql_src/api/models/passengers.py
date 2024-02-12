from postgresql_src.api.database import db


class Passengers(db.Model):
    __table_name__ = 'passengers'

    passenger_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survived = db.Column(db.Integer, nullable=False)
    p_class = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(), nullable=False)
    sex = db.Column(db.String(), nullable=False)
    age = db.Column(db.Float(), nullable=True)
    sib_sp = db.Column(db.Integer, nullable=False)
    parch = db.Column(db.Integer, nullable=False)
    ticket = db.Column(db.String(), nullable=False)
    fare = db.Column(db.Float(), nullable=True)
    cabin = db.Column(db.String(), nullable=True)
    embarked = db.Column(db.String(), nullable=False)

    def __init__(self, passenger_id, survived, p_class, name, sex, age, sib_sp, parch, ticket, fare, cabin, embarked):
        self.passenger_id = passenger_id
        self.survived = survived
        self.p_class = p_class
        self.name = name
        self.sex = sex
        self.age = age
        self.sib_sp = sib_sp
        self.parch = parch
        self.ticket = ticket
        self.fare = fare
        self.cabin = cabin
        self.embarked = embarked

    def to_dict(self):
        return {
            'passenger_id': self.passenger_id,
            'name': self.name
        }

    def __repr__(self):
        return f"<Passenger {self.age}>"
