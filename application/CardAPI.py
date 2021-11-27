from application.api import *

card_fields = {
    'id':   fields.Integer,
    'front':    fields.String,
    'back':    fields.String,
    'review':     fields.Integer
    
}
create_card_parser = reqparse.RequestParser()
create_card_parser.add_argument('front', required=True)
create_card_parser.add_argument('back',  required=True)

update_card_parser = reqparse.RequestParser()
update_card_parser.add_argument('front', required=True)
update_card_parser.add_argument('back',  required=True)
class CardAPI(Resource):
    
    @marshal_with(card_fields)
    def get(self, deck_id):
        deck = Deck.query.filter_by(id=deck_id).first()
        print(deck)
        if not deck:
            raise NotFoundError(status_code=404)
            
        cards = Card.query.filter_by(deck_id=deck_id).all()
        if len(cards)==0:
            raise BusinessValidationError(
                status_code=400, error_code="CARD001", error_message="No card created for the deck")
        else:
            return cards
            

        
    @marshal_with(card_fields)
    def put(self, card_id):
        card= Card.query.filter_by(id=card_id).first()
        if not card:
            raise NotFoundError(status_code=404)
        deck_id = card.deck_id
        deck = Deck.query.filter_by(id=deck_id).first()
        args = update_card_parser.parse_args()
        front = args.get('front',None)
        back= args.get('back',None)
        if front is None or len(front)==0:
            raise BusinessValidationError(
                status_code=400, error_code="CARD002", error_message="Front of the card should be non-empty")
        if back is None or len(back)==0:
            raise BusinessValidationError(
                status_code=400, error_code="CARD003", error_message="Back of the card should be non-empty")
        card_exist =Card.query.filter_by(front=front,back=back,deck_id=deck_id).first()
        if card_exist:
            raise AlreadyExistedError(status_code=409)
        
        card.front=front
        card.back=back
        card.review=0
        db.session.commit()
        return card
        


    def delete(self,card_id):
        card= Card.query.filter_by(id=card_id).first()
        if not card:
            raise NotFoundError(status_code=404)
        
        db.session.delete(card)
        db.session.commit()

    @marshal_with(card_fields)
    def post(self, deck_id):
        deck = Deck.query.filter_by(id=deck_id).first()
        if not deck:
            raise BusinessValidationError(
                status_code=400, error_code="CARD001", error_message="INVALID DECK ID")
        args = create_card_parser.parse_args()
        front = args.get('front',None)
        back= args.get('back',None)
        if front is None or len(front)==0:
            raise BusinessValidationError(
                status_code=400, error_code="CARD002", error_message="Front of the card should be non-empty")
        if back is None or len(back)==0:
            raise BusinessValidationError(
                status_code=400, error_code="CARD003", error_message="Back of the card should be non-empty")
        card_exist =Card.query.filter_by(front=front,back=back,deck_id=deck_id).first()
        if card_exist:
            raise AlreadyExistedError(status_code=409)
        
        card=Card(front=front, back=back, deck_id=deck_id)
        db.session.add(card)
        db.session.commit()
        return card
class CardsAPI(Resource):
    @marshal_with(card_fields)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise NotFoundError(status_code=404)
        
        decks = Deck.query.filter_by(user_id=user_id).all()
        if len(decks)==0:
            raise BusinessValidationError(
                status_code=400, error_code="DECK001", error_message="No deck created for the user")
        allcards=[]
        for deck in decks:
            cards = Card.query.filter_by(deck_id=deck.id).all()
            allcards+=cards
        if len(allcards)==0:
            raise BusinessValidationError(
                status_code=400, error_code="CARD004", error_message="No card created for the user")
        else:
            return allcards