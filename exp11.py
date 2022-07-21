from exp10 import db
from exp10 import User, Post

# user_1 = User(username = 'Corey', email= 'C@demo.com', password='password')
# db.session.add(user_1)
# user_2 = User(username = 'JohnDoe', email= 'jd@demo.com', password='password')
# db.session.add(user_2)
# db.session.commit()

# print(User.query.all())
# print(User.query.first())
# user  = User.query.filter_by(username='Corey').first()
# print(user.id)

user = User.query.get(1)
# post_1 = Post(title='Blog 1', content='First Post Content!', user_id=user.id)
# post_2 = Post(title='Blog 2', content='Second Post Content!', user_id=user.id)
# db.session.add(post_1)
# db.session.add(post_2)
# db.session.commit()

# print(user.posts)
# for post in user.posts:
#     print(post.title)
post = Post.query.first()
print(post)
print(user)
print(post.author)