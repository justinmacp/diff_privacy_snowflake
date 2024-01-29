from postgresql_src.api.database import db


class User(db.Model):
    __table_name__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    role = db.Column(db.String(), default="data_analyst")
    privacy_budget = db.Column(db.Double, nullable=False)

    __table_args__ = (
        db.CheckConstraint(role.in_(['data_analyst']), name='role_types'),
    )

    def __init__(self, username, created_at, role, privacy_budget):
        self.username = username
        self.created_at = created_at
        self.role = role
        self.privacy_budget = privacy_budget

    def register_user_if_not_exist(self):
        db_user = User.query.filter(User.username == self.username).all()
        if not db_user:
            db.session.add(self)
            db.session.commit()
        return True

    def get_by_username(self):
        db_user = User.query.filter(User.username == self).first()
        return db_user

    def __repr__(self):
        return f"<User {self.username}>"
