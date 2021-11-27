
from application.api import *

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username', type=str, required=True)
create_user_parser.add_argument('password')

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('username', type=str, required=True)
update_user_parser.add_argument('password')


user_fields = {
    'id':   fields.Integer,
    'username':    fields.String,
    'password':     fields.String,
    'active':    fields.Integer
}


class UserAPI(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user
        else:
            raise NotFoundError(status_code=404)
    
    @marshal_with(user_fields)
    def put(self, user_id):
        args = update_user_parser.parse_args()
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            raise NotFoundError(status_code=404)
        username = args.get('username',None)
        password = args.get('password',None)
        if username is None or type(username) is not str:
            raise BusinessValidationError(
                status_code=400, error_code="USER001", error_message="Username is required and should be String")
            
        if password is None:
            raise BusinessValidationError(
                status_code=400, error_code="USER002", error_message="Password is required and should be String")
        user_exist = User.query.filter_by(username=username).first()
        if user_exist:
            raise AlreadyExistedError(
                status_code=409)
        user.username = username
        user.password = bcrypt.generate_password_hash(password)
        # db.session.add(user)
        db.session.commit()
        return user

    def delete(self,user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            decks = Deck.query.filter_by(user_id=user_id).all()
            
            for deck in decks:
                cards = Card.query.filter_by(deck_id=deck.id).all()
                for card in cards:
                    db.session.delete(card)
                db.session.delete(deck)
            db.session.delete(user)
            db.session.commit()
        else:
            raise NotFoundError(status_code=404)
    
    @marshal_with(user_fields)
    def post(self):
        args = create_user_parser.parse_args()
        username = args.get('username',None)
        password = args.get('password',None)
        if username is None or type(username) is not str:
            raise BusinessValidationError(
                status_code=400, error_code="USER001", error_message="Username is required and should be String")
            
        if password is None:
            raise BusinessValidationError(
                status_code=400, error_code="USER002", error_message="Password is required")
        user_exist = User.query.filter_by(username=username).first()
        if user_exist:
            raise AlreadyExistedError(
                status_code=409)
        user = User(username=username)
        db.session.add(user)
        user.password=bcrypt.generate_password_hash(password)
        db.session.commit()
        return user


