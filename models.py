from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """ 用户模型 """
    __tablename__ = 'accounts_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    # 用户名，用于登录
    username = db.Column(db.String(64), unique=True, nullable=False)
    # 用户昵称
    nickname = db.Column(db.String(64))
    password = db.Column(db.String(256), nullable=False)
    # 用户的头像地址
    avatar = db.Column(db.String(256))
    # 是否有效，无效用户将不能登录系统
    status = db.Column(db.String(db.SmallInteger()), default=1)
    # 是否是超级管理员，管理员可以对所有内容进行管理
    is_super = db.Column(db.String(db.SmallInteger()), default=1)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime,default=datetime.now, onupdate=datetime.now)

class UserProfile(db.Model):
    """ 用户详细信息 """
    __tablename__ = 'accounts_user_profile'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    # 用户名，用于登录
    username = db.Column(db.String(64), unique=True, nullable=False)
    # 用户真实姓名
    real_name = db.Column(db.String(64))
    # 用户的格言
    maxim = db.Column(db.String(128))
    # 性别
    sex = db.Column(db.String(16))
    # 地址
    address = db.Column(db.String(256))
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime,default=datetime.now, onupdate=datetime.now)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 建立用户的一对一关系属性user.profile  profile.user
    user = db.relationship('User', backref=db.backref('profile', uselist=False))

class Question(db.Model):
    """ 问题 """
    __tablename__ = 'qa_question'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    # 问题标题
    title = db.Column(db.String(128), nullable=False)
    # 问题描述
    desc = db.Column(db.String(256))
    # 问题图片
    img = db.Column(db.String(256))
    # 问题详情
    content = db.Column(db.Text, nullable=False)
    # 浏览人数
    view_count = db.Column(db.Integer, default=0)
    # 逻辑删除
    is_valid = db.Column(db.Boolean, default=True)
    # 排序
    reorder = db.Column(db.Integer, default=0)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 建立与用户的一对多属性,user.question_list
    user = db.relationship('User', backref=db.backref('question_list', lazy='dynamic'))

class QuestionTags(db.Model):
    """ 问题下的标签 """
    __tablename__ = 'qa_question_tags'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    # 标签名称
    tag_name = db.Column(db.String(16), nullable=False)
    # 逻辑删除
    is_valid = db.Column(db.Boolean, default=True)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('tag_list', lazy='dynamic'))

class Answer(db.Model):
    """  问题的回答 """
    __tablename__ = 'qa_answer'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    # 回答的内容详情
    content = db.Column(db.Text, nullable=False)
    # 逻辑删除
    is_valid = db.Column(db.Boolean, default=True)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    # 建立与用户的一对多属性
    user = db.relationship('User', backref=db.backref('answer_list', lazy='dynamic'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('answer_list', lazy='dynamic'))

class AnswerComment(db.Model):
    """ 回答的评论 """
    __tablename__ = 'qa_answer_comment'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    # 评论内容
    content = db.Column(db.String(512), nullable=False)
    # 赞同人数
    love_count = db.Column(db.Integer, default=0)
    # 评论是否公开
    is_public = db.Column(db.Boolean, default=True)
    # 逻辑删除
    is_valid = db.Column(db.Boolean, default=True)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 回复ID
    reply_id = db.Column(db.Integer, db.ForeignKey('qa_answer_comment.id'), nullable=True)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 关联答案
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))

    # 建立与用户的一对多属性
    user = db.relationship('User', backref=db.backref('answer_comment_list', lazy='dynamic'))
    # 建立与答案的一对多属性
    answer = db.relationship('Answer', backref=db.backref('answer_comment_list', lazy='dynamic'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('question_comment_list', lazy='dynamic'))

class AnswerLove(db.Model):
    """ 回答点赞 """
    __tablename__ = 'qa_answer_love'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 关联答案
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))

    # 建立与用户的一对多属性
    user = db.relationship('User', backref=db.backref('answer_love_list', lazy='dynamic'))
    # 建立与答案的一对多属性
    answer = db.relationship('Answer', backref=db.backref('answer_love_list', lazy='dynamic'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('question_love_list', lazy='dynamic'))

class AnswerCollect(db.Model):
    """ 收藏的回答 """
    __tablename__ = 'qa_answer_collect'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 逻辑删除
    is_valid = db.Column(db.Boolean, default=True)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    # 关联答案
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))

    # 建立与用户的一对多属性
    user = db.relationship('User', backref=db.backref('answer_collect_list', lazy='dynamic'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('question_collect_list', lazy='dynamic'))
    # 建立与答案的一对多属性
    answer = db.relationship('Answer', backref=db.backref('answer_collect_list', lazy='dynamic'))

class QuestionFollow(db.Model):
    """ 关注的问题 """
    __tablename__ = 'qa_question_follow'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    created_at = db.Column(db.DateTime)
    is_valid = db.Column(db.Boolean, default=True, comment='逻辑删除')
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))

    # 建立与用户的一对多属性
    user = db.relationship('User', backref=db.backref('question_follow_list', lazy='dynamic'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('question_follow_list', lazy='dynamic'))