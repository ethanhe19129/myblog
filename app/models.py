from . import db

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    cate_name = db.Column(db.String(50), nullable=False)
    topics = db.relationship('Topic', backref='category', lazy='dynamic')

class BlogType(db.Model):
    __tablename__ = "blogtype"
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(20), nullable=False)
    topics = db.relationship('Topic', backref='blogType', lazy='dynamic')

class Recommend(db.Model):
    __tablename__ = "recommend"
    id = db.Column(db.Integer, primary_key=True)
    reco_type = db.Column(db.String(20), nullable=False)
    topics = db.relationship('Topic', backref='recommend', lazy='dynamic')

    def to_dic(self):
        dic = {
            "id":self.id,
            "reco_type":self.reco_type,
        }
        return dic

class User(db.Model):
    __tablename__ = "user"
    ID = db.Column(db.Integer, primary_key=True)
    loginname = db.Column(db.String(50), nullable=False)
    uname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200))
    upwd = db.Column(db.String(30), nullable=False)
    is_author = db.Column(db.Boolean, default=False)
    topics = db.relationship('Topic', backref='user', lazy='dynamic')
    replies = db.relationship('Reply', backref='user', lazy='dynamic')
    messages = db.relationship('Message', backref='user', lazy='dynamic')
    reply_messages = db.relationship('ReplyMessage', backref='user', lazy='dynamic')
    voke_topics = db.relationship(
        'Topic',
        secondary='voke',
        lazy='dynamic',
        backref=db.backref(
            'voke_users',
            lazy='dynamic'
        )
    )

class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    read_num = db.Column(db.Integer, default=0)
    content = db.Column(db.Text, nullable=False)
    images = db.Column(db.Text)
    blogtype_id = db.Column(db.Integer, db.ForeignKey('blogtype.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.ID'), )
    replies = db.relationship('Reply', backref='topic', lazy='dynamic')
    recommend_id = db.Column(db.Integer, db.ForeignKey('recommend.id'))

class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    reply_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.ID'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

class Voke(db.Model):
    __tablename__ = "voke"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.ID'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.ID'))
    reply_messages = db.relationship('ReplyMessage', backref='message', lazy='dynamic')

    def to_dic(self):
        dic = {
            "id":self.id,
            "content":self.content,
            "pub_date":self.pub_date.__str__(),
            "user_uname":self.user.uname
        }
        return dic

class ReplyMessage(db.Model):
    __tablename__ = 'replymessage'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.ID'))
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))

    def to_dic(self):
        dic = {
            "id":self.id,
            "content":self.content,
            "pub_date":self.pub_date.__str__(),
            "user_uname":self.user.uname,
            "message_id":self.message_id
        }
        return dic



