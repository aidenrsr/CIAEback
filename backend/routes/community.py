

messages_ns = Namespace("messages")
message_model = messages_ns.model(
    "Message",
    {
        "message_id": fields.Integer(),
        "username": fields.String(),
        "text": fields.String(),
        "timestamp": fields.DateTime(),
    },
)



@messages_ns.route("/messages")
class MessagesResource(Resource):
    @messages_ns.marshal_list_with(message_model)
    def get(self):
        chat = Message.query.order_by(Message.timestamp.asc()).all()
        return chat

    @messages_ns.expect(message_model)
    @messages_ns.marshal_with(message_model)
    @jwt_required()
    def post(self):
        # get the user id from JWT
        user_id = get_jwt_identity()
        # fetch the user from the database
        user = User.query.get_or_404(user_id)
        # get the message text from the request body
        data = request.get_json()
        text = data.get('text', '').strip()
        if not text:
            return {'Message cannot be empty'}, 400
        # create and save the message
        message = Message(username = user.username, text = text)
        db.session.add(message)
        db.session.commit()

        return {'Message sent'}, 201

@messages_ns.route("/messages/<int:message_id>")
class MessageResource(Resource):
    @messages_ns.marshal_with(message_model)
    def get(self, message_id):
        message = Message.query.get_or_404(message_id)
        return message

    @jwt_required()
    def delete(self, message_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        message_to_delete = Message.query.get_or_404(message_id)
        # check if user and message writer match
        if user.username != message_to_delete.username:
            return {"error"}, 403
        
        db.session.delete(message_to_delete)
        db.session.commit()
        return {"Message deleted"}, 200