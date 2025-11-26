# app.py

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
# --- 修改：删除对 LotteryUser 的导入 ---
from database import db, init_db, LoginUser
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os

# --- 基础应用配置 ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/flask_data3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a-very-secret-key-that-you-should-change'

# --- 文件上传配置 ---
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- 初始化扩展 ---
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录以访问此页面。'


# --- Flask-Login 回调函数 ---
@login_manager.user_loader
def load_user(user_id):
    return LoginUser.query.get(int(user_id))


# --- 辅助函数 ---
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- 认证相关路由 ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = LoginUser.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            flash(f'欢迎回来，{user.nickname}！', 'success')
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误。', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        nickname = request.form.get('nickname')
        phone = request.form.get('phone')

        if LoginUser.query.filter_by(username=username).first():
            flash('用户名已存在。', 'danger')
            return redirect(url_for('register'))
        if LoginUser.query.filter_by(phone=phone).first():
            flash('手机号已被注册。', 'danger')
            return redirect(url_for('register'))

        avatar_filename = 'default_avatar.png'
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                avatar_filename = f"{username}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))

        new_user = LoginUser(username=username, nickname=nickname, phone=phone, avatar=avatar_filename,
                             password=password)
        db.session.add(new_user)
        db.session.commit()

        # --- 删除为新用户创建LotteryUser的代码 ---
        flash('注册成功！请登录。', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出。', 'info')
    return redirect(url_for('login'))


# --- 主要功能路由 ---
@app.route('/')
@login_required
def index():
    current_profile = {
        'id': current_user.id,
        'name': current_user.nickname,
        'img': url_for('static', filename=f'images/{current_user.avatar}')
    }
    return render_template('index.html', current_user_profile=current_profile)

# --- 应用入口 ---
if __name__ == '__main__':
    try:
        print("正在启动Flask开发服务器...")
        print("如果数据库不存在或需要重置，请手动运行初始化脚本。")
        app.run(debug=True)
    except Exception as e:
        print("=" * 50)
        print("!!! 发生致命错误，程序无法启动 !!!")
        print(f"错误详情: {e}")
        print("=" * 50)
        input("按任意键退出...")
