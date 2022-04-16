import wtforms
from wtforms.validators import email, EqualTo, length
from models import EmailCaptchaModel, UserModel


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        emailcaptcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        print(captcha.lower())
        if not emailcaptcha_model or captcha.lower() != emailcaptcha_model.captcha.lower():
            print("中招")
            raise wtforms.ValidationError("邮箱验证码有误！")

    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        print(user_model)
        if user_model:
            raise wtforms.ValidationError("该邮箱已经存在！")


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=6, max=100)])
    content = wtforms.StringField(validators=[length(min=3)])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])