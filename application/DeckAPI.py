from application.api import *

deck_fields = {
    'id':   fields.Integer,
    'title':    fields.String,
    'review_time':    fields.DateTime,
    'deck_score':     fields.Integer
    
}
create_deck_parser = reqparse.RequestParser()
create_deck_parser.add_argument('title', type=str, required=True)

update_deck_parser = reqparse.RequestParser()
update_deck_parser.add_argument('title', type=str, required=True)
class DeckAPI(Resource):
    
    @marshal_with(deck_fields)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise NotFoundError(status_code=404)
            
        decks = Deck.query.filter_by(user_id=user_id).all()
        if len(decks)==0:
            raise BusinessValidationError(
                status_code=400, error_code="DECK001", error_message="No deck created for the user")
        else:
            return decks
            

        

    def put(self, deck_id):
        deck= Deck.query.filter_by(id=deck_id).first()
        if not deck:
            raise NotFoundError(status_code=404)
        user_id = deck.user_id
        user = User.query.filter_by(id=user_id).first()
        args = update_deck_parser.parse_args()
        title = args.get('title',None)
        if title is None or type(title) is not str or len(title)==0:
            raise BusinessValidationError(
                status_code=400, error_code="DECK002", error_message="Title should be non-empty string")
        deck_exist =Deck.query.filter((Deck.title==title) & (Deck.user_id==user_id)).first()
        if deck_exist:
            raise AlreadyExistedError(status_code=409)
        
        deck.title=title
        db.session.commit()
        return {'id':deck.id,'title':deck.title,'username':user.username}
        


    def delete(self,deck_id):
        deck= Deck.query.filter_by(id=deck_id).first()
        if not deck:
            raise NotFoundError(status_code=404)
        cards = Card.query.filter_by(deck_id=deck_id).all()
        for card in cards:
            db.session.delete(card)
        db.session.delete(deck)
        db.session.commit()

    def post(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise BusinessValidationError(
                status_code=400, error_code="DECK001", error_message="INVALID USER ID")
        args = create_deck_parser.parse_args()
        title = args.get('title',None)
        if title is None or type(title) is not str or len(title)==0:
            raise BusinessValidationError(
                status_code=400, error_code="DECK002", error_message="Title should be non-empty string")
        deck_exist =Deck.query.filter((Deck.title==title) & (Deck.user_id==user_id)).first()
        if deck_exist:
            raise AlreadyExistedError(status_code=409)
        
        deck=Deck(title=title, user_id=user_id)
        db.session.add(deck)
        db.session.commit()
        return {'id':deck.id,'title':deck.title,'username':user.username}