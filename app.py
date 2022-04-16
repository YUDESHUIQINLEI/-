from flask import Flask, render_template, session, g
import config
from exts import db, mail
from blueprints import user_bp
from blueprints import qa_bp
from flask_migrate import Migrate
from models import UserModel


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(user_bp)
app.register_blueprint(qa_bp)

@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 设置了一个整个项目都能访问的变量
            g.user = user
        except:
            g.user = None

# 一个请求来了，先请求before_request 再执行视图函数 返回模板 执行context_processor
# 所有的模板都会执行context_processor
@app.context_processor
def context_processor():
    if hasattr(g, 'user'):
        return {"user1": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
