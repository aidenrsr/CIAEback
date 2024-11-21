# from flask import request, jsonify
# from flask_restx import Namespace, Resource
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from models import Thread, Post, Comment, User
# from ext import db
# 
# community = Namespace("community")
# 
# # thread
# @community.route("/threads")
# class ThreadsResource(Resource):
#     def get(self):
#         threads = Thread.query.all()
#         return jsonify([
#             {
#                 "id": c.id,
#                 "title": c.title
#             } 
#             for c in threads]), 200
# 
#     @jwt_required()
#     # just to add new thread for new book
#     def post(self):
#         data = request.get_json()
#         title = data.get("title", "").strip()
#         book_id = data.get("book_id")
#         if not title:
#             return jsonify({"error": "title empty"}), 400
#         thread = Thread(title=title, book_id=book_id)
#         thread.save()
# 
# 
# # Post
# @community.route("/threads/<int:thread_id>/posts")
# class PostsResource(Resource):
#     def get(self, thread_id):
#         posts = Post.query.filter_by(thread_id=thread_id).order_by(Post.created_at.desc()).all()
#         return jsonify([
#             {
#                 "post_id": p.id,
#                 "thread_id": p.thread_id,
#                 "title": p.title,
#                 "content": p.content,
#                 "username": p.username,
#                 "created_at": p.created_at
#             }
#             for p in posts]), 200
# 
#     @jwt_required()
#     def post(self, thread_id):
#         user_id = get_jwt_identity()
#         user = User.query.get_or_404(user_id)
# 
#         data = request.get_json()
#         title = data.get("title", "").strip()
#         content = data.get("content", "").strip()
#         if not title or not content:
#             return jsonify({"error": "empty"}), 400
# 
#         new_post = Post(thread_id=thread_id, title=title, content=content, username=user.username)
#         new_post.save()
#         return jsonify({"post successfully saved"})
# 
# 
# # Endpoints for Comments on a Post
# @community.route("/posts/<int:post_id>/comments")
# class CommentsResource(Resource):
#     def get(self, post_id):
#         comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()
#         return jsonify([
#             {
#                 "comment_id": c.id,
#                 "post_id": c.post_id,
#                 "username": c.username,
#                 "content": c.content,
#                 "created_at": c.created_at
#             } for c in comments]), 200
# 
#     @jwt_required()
#     def post(self, post_id):
#         user_id = get_jwt_identity()
#         user = User.query.get_or_404(user_id)
# 
#         data = request.get_json()
#         content = data.get("content", "").strip()
#         if not content:
#             return jsonify({"error": "empty"}), 400
# 
#         new_comment = Comment(post_id=post_id, content=content, username=user.username)
#         new_comment.save()
#         return jsonify({"comment successfully saved"})
# 
# 
# # @community.route("/posts/<int:post_id>/comments")
# # class LikeResource(Resource):
