from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Thread, Post, Comment, User

community_ns = Namespace("community", description="Namespace for Community board")

# Thread
@community_ns.route("/threads")
class ThreadsResource(Resource):
    # to get all the threads(for starting page of community)
    def get(self):
        threads = Thread.query.all()
        return jsonify([
            {
                "id": c.id,
                "title": c.title,
                "book_id": c.book_id
            }
            for c in threads
        ]), 200

    @jwt_required()
    # just to add new thread for new book
    def post(self):
        data = request.get_json()
        title = data.get("title", "").strip()
        book_id = data.get("book_id")

        if not title:
            return jsonify({"error": "title empty"}), 400
        
        thread = Thread(title=title, book_id=book_id)
        thread.save()

        return jsonify({"thread created successfully"}), 201

@community_ns.route("/threads/<int:thread_id>/posts")
class PostResource(Resource):
    # this for single thread with all the posts
    def get(self, thread_id):
        posts = Post.query.filter_by(thread_id=thread_id).order_by(Post.created_at.desc()).all()

        result = [
            {
                "post_id": p.id,
                "title": p.title,
                "content": p.content,
                "username": p.username,
                "created_at": p.created_at
            }
            for p in posts]

        return jsonify(result)
    
    # this is for new post in the thread
    @jwt_required()
    def post(self, thread_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        data = request.get_json()
        title = data.get("title", "").strip()
        content = data.get("content", "").strip()
        if not title or not content:
            return jsonify({"Title and content cannot be empty"}), 400

        new_post = Post(thread_id=thread_id, title=title, content=content, username=user.username)
        new_post.save()

        return jsonify({"Post created successfully"})

@community_ns.route("/posts/<int:post_id>")
class PostDetailResource(Resource):
    @jwt_required()
    def delete(self, post_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        post = Post.query.get_or_404(post_id)

        if post.username != user.username:
            return jsonify({"User not authorized to delete this post"}), 403

        post.delete()
        return jsonify({"Post deleted successfully"}), 200
    

@community_ns.route("/posts/<int:post_id>/comments")
class CommentsResource(Resource):
    # get post's comments
    def get(self, post_id):
        comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()

        result = [
            {
                "comment_id": c.id,
                "content": c.content,
                "username": c.username,
                "created_at": c.created_at
            } for c in comments]

        return jsonify(result)
    

    @jwt_required()
    def post(self, post_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        data = request.get_json()
        content = data.get("content", "").strip()
        if not content:
            return jsonify({"Comment cannot be empty"}), 400

        new_comment = Comment(post_id=post_id, content=content, username=user.username)
        new_comment.save()

        return jsonify({"Comment created successfully"}), 201
    
@community_ns.route("/comments/<int:comment_id>")
class CommentResource(Resource):
    def delete(self, comment_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        comment = Comment.query.get_or_404(comment_id)

        if comment.username != user.username:
            return jsonify({"User not authorized to delete this comment"}), 403

        comment.delete()
        return jsonify({"Comment deleted successfully"}), 200
    
