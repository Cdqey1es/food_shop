from flask_login import current_user
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Regexp, Length, Email, EqualTo

from app.validators.base import BaseForm


class LoginForm(BaseForm):
    login_name = StringField(validators=[DataRequired(message='用户名不允许为空')])
    #                                      Regexp(r'^1[0-9]{10}$', message='用户名码必须是11位手机号码')])
    login_pwd = PasswordField(validators=[DataRequired(message='密码不能为空'),
                                          Regexp(r'^[A-Za-z0-9_]{6,22}$',
                                                 message='密码格式不对，必须为6到22位字母，数字或下划线')
                                          ])


class EditForm(BaseForm):
    nickname = StringField(validators=[DataRequired(message='昵称不允许为空'),
                                       Length(3, 22, message='昵称必须为 3 - 22 个字符')])
    email = StringField(validators=[DataRequired(message='邮箱不能为空'), Email(message='电子邮件格式不符合规范')])


class ResetPwdForm(BaseForm):
    old_password = PasswordField(validators=[DataRequired(message='密码不能为空'),
                                             Regexp(r'^[A-Za-z0-9_]{6,22}$',
                                                    message='密码格式不对，必须为6到22位字母，数字或下划线')
                                             ])
    new_password = PasswordField(validators=[DataRequired(message='密码不能为空'),
                                             Regexp(r'^[A-Za-z0-9_]{6,22}$',
                                                    message='密码格式不对，必须为6到22位字母，数字或下划线')
                                             ])
    confirm_password = PasswordField(validators=[DataRequired(message='密码不能为空'),
                                                 EqualTo('new_password', message='两次输入的密码不相同')])

    def validate_old_password(self, field):
        result = current_user.check_password(field.data)
        if not result:
            raise ValidationError('原密码不正确')

    def validate_new_password(self, field):
        if self.old_password.data == field.data:
            raise ValidationError('新密码不能与原密码相同')
