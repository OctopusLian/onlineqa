import os

from flask import current_app
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

from models import Question, db, QuestionTags


class WriteQuestionForm(FlaskForm):
    """ 写文章\问题 """
    img = FileField(label='上传图片', render_kw={
        'accept': ".jpeg, .jpg, .png"
    }, validators=[
        FileAllowed(['png', 'jpg', 'jpeg'], '请选择合适的图片类型')
    ])
    title = StringField(label='标题', render_kw={
        'class': "form-control",
        'placeholder': "请输入标题（最多50个字）"
    }, validators=[DataRequired('请输入标题'),
                   Length(min=5, max=50, message='标题长度为5-50字')])
    tags = StringField(label='标签', render_kw={
        'class': "form-control",
        'placeholder': "输入标签，用,分隔"
    })
    desc = TextAreaField(label='描述', render_kw={
        'class': "form-control",
        'placeholder': "简述"
    }, validators=[Length(max=150, message='描述最长为150字')])
    content = CKEditorField(label='文章内容', render_kw={
        'class': "form-control",
        'placeholder': "请输入正文"
    }, validators=[DataRequired('请输入正文'),
                   Length(min=5, message='不能少于5个字符')])

    def save(self):
        """ 发布问题 """
        # 1. 获取图片
        img = self.img.data
        img_name = ''
        if img:
            img_name = secure_filename(img.filename)
            img_path = os.path.join(current_app.config['MEDIA_ROOT'], img_name)
            img.save(img_path)
        # 2. 保存问题
        title = self.title.data
        desc = self.desc.data
        content = self.content.data
        que_obj = Question(
            title=title,
            desc=desc,
            img=img_name,
            content=content,
            user=current_user
        )
        db.session.add(que_obj)
        # 3. 保存标签
        tags = self.tags.data
        for tag_name in tags.split('，'):
            if tag_name:
                tag_obj = QuestionTags(tag_name=tag_name, question=que_obj)
                db.session.add(tag_obj)
        db.session.commit()
        return que_obj
