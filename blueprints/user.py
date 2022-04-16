from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from app import mail
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
import string
import random
from datetime import datetime
from exts import db
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect('/')
            else:
                flash("邮箱和密码不匹配！")
                return redirect(url_for('user.login'))
        else:
            flash("邮箱或密码格式错误！")
            return redirect(url_for('user.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            final_pass = generate_password_hash(password)
            user_model = UserModel(username=username, email=email, password=final_pass)
            db.session.add(user_model)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('user.register'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))


@bp.route('/captcha', methods=["POST"])
def send_mail():
    email = request.form.get('email')
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))
    print(captcha)
    if email:
        message = Message(
            subject="邮箱测试",
            recipients=[email],
            body=f"您好，您收到的验证码是{captcha}，请不要告诉其他人"
        )
        mail.send(message)
        captchamodel = EmailCaptchaModel.query.filter_by(email=email).first()
        if captchamodel:
            captchamodel.captcha = captcha
            captchamodel.create_time = datetime.now()
            db.session.commit()
        else:
            captchamodel1 = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captchamodel1)
            db.session.commit()
        return jsonify({"code": 200})
    else:
        return jsonify({"code": 400, "message": "请先传递邮箱哦"})
