from flask_script import Command, Option

from app.models import User, Adminlist, db

class CreateSuperUserCommand(Command):
    """Creates admin user"""
    
    option_list = (
        Option('--name', '-n', dest='name', required=True),
        Option('--lastname', '-l', dest='lastname', required=True),
        Option('--username', '-u', dest='username', required=True),
        Option('--email', '-e', dest='email', required=True),
        Option('--password', '-p', dest='password', required=True)
    )

    def run(self, name, lastname, username, email, password):
        user = User(
            name=name,
            lastname=lastname,
            username=username,
            email=email
        )
        user.set_password(password=password)
        db.session.add(user)
        db.session.commit()
        admin = Adminlist(user=user)
        db.session.add(admin)
        db.session.commit()
