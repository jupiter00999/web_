from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from database import db, init_db, LoginUser, Product, CartItem  # 仅保留用到的模型
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/flask_data3'  # 请修改为你的数据库配置
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # 建议修改为随机字符串

# 文件上传配置（修复路径问题）
UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 初始化扩展
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return LoginUser.query.get(int(user_id))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 认证路由（保持不变）
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
            flash('用户名或密码错误', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        nickname = request.form.get('nickname')
        phone = request.form.get('phone')

        if LoginUser.query.filter_by(username=username).first():
            flash('用户名已存在', 'danger')
            return redirect(url_for('register'))
        if LoginUser.query.filter_by(phone=phone).first():
            flash('手机号已被注册', 'danger')
            return redirect(url_for('register'))

        # 处理头像上传
        avatar_filename = 'default_avatar.png'
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file.filename != '' and allowed_file(file.filename):
                avatar_filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))

        new_user = LoginUser(
            username=username,
            nickname=nickname,
            phone=phone,
            password=password,
            avatar=avatar_filename
        )
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已成功登出', 'info')
    return redirect(url_for('login'))


# 商品路由（核心修复）
@app.route('/')
@login_required
def index():
    products = Product.query.all()
    return render_template('index.html', products=products, current_user_profile=current_user.to_dict())


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    # 仅管理员可访问
    if current_user.username != 'admin':
        flash('没有权限添加商品', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # 获取表单数据
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))

        # 处理商品图片（修复上传逻辑）
        image_filename = 'default_product.png'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                image_filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        # 保存商品到数据库
        new_product = Product(
            name=name,
            description=description,
            price=price,
            image=image_filename
        )
        db.session.add(new_product)
        db.session.commit()
        flash('商品添加成功', 'success')
        return redirect(url_for('index'))

    return render_template('add_product.html')


@app.route('/product/<int:product_id>')
@login_required
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


# 加入购物车（核心修复：实现实际添加逻辑）
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])  # 修改为POST方法更规范
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    # 检查购物车中是否已有该商品
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if cart_item:
        # 已有则数量+1
        cart_item.quantity += 1
    else:
        # 没有则新增
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=1
        )
        db.session.add(cart_item)

    db.session.commit()  # 提交到数据库
    flash(f'{product.name} 已加入购物车', 'success')
    return redirect(url_for('product_detail', product_id=product_id))


# 查看购物车（新增功能）
@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.quantity * item.product.price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


# 其他数据接口（保持不变）
@app.route('/api/charts_data')
@login_required
def get_charts_data():
    from database import SalesData, AgeDistribution, ViewData, FollowData  # 延迟导入
    sales = SalesData.query.order_by(SalesData.date).all()
    sales_chart = {'dates': [s.date.strftime('%Y-%m-%d') for s in sales], 'amounts': [s.amount for s in sales]}
    age_dist = AgeDistribution.query.all()
    age_chart = {'groups': [a.age_group for a in age_dist], 'counts': [a.count for a in age_dist]}
    return jsonify({'sales': sales_chart, 'age': age_chart})


if __name__ == '__main__':
    app.run(debug=True)