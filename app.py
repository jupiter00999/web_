# app.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from database import db,LoginUser, Product, CartItem
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

        if user and check_password_hash(user.password, password):
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

        new_user = LoginUser(
            username=username,
            nickname=nickname,
            phone=phone,
            avatar=avatar_filename,
            password=generate_password_hash(password)  # 加密存储
        )
        db.session.add(new_user)
        db.session.commit()

        flash('注册成功！请登录。', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出。', 'info')
    return redirect(url_for('login'))


# --- 商品相关路由 ---
@app.route('/')
@login_required
def index():
    # 获取所有商品数据
    products = Product.query.all()
    product_list = []
    for p in products:
        product_list.append({
            'id': p.id,
            'name': p.name,
            'original_price': p.original_price,
            'current_price': p.current_price,
            'seller': p.seller,
            'images': url_for('static', filename=f'images/{p.images}')
        })

    current_profile = {
        'id': current_user.id,
        'name': current_user.nickname,
        'img': url_for('static', filename=f'images/{current_user.avatar}')
    }
    return render_template('index.html', current_user_profile=current_profile, products=product_list)


# --- 购物车相关路由 ---
@app.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    data = request.json
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return jsonify({'status': 'error', 'message': '商品ID不能为空'}), 400

    # # 检查商品是否存在
    # product = Product.query.get(product_id)
    # if not product:
    #     return jsonify({'status': 'error', 'message': '商品不存在'}), 404

    # 检查购物车中是否已有该商品
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        # 更新数量
        cart_item.quantity += quantity
    else:
        # 添加新商品
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({'status': 'success', 'message': '已添加到购物车'})


@app.route('/api/cart')
@login_required
def get_cart_data():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    cart_data = []
    total_price = 0
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            item_total = product.current_price * item.quantity
            total_price += item_total
            cart_data.append({
                'id': item.id,
                'product_id': product.id,
                'name': product.name,
                # 修复图片路径：使用url_for生成完整路径
                'images': url_for('static', filename=f'images/{product.images}'),
                'current_price': product.current_price,
                'quantity': item.quantity,
                'item_total': item_total
            })
    return jsonify(cart_data)



@app.route('/cart')
@login_required
def view_cart():
    # 获取当前用户的购物车商品
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    # 组装购物车数据（包含商品详情）
    cart_data = []
    total_price = 0

    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            item_total = product.current_price * item.quantity
            total_price += item_total
            cart_data.append({
                'id': item.id,
                'product_id': product.id,
                'name': product.name,
                'images': product.images,
                'current_price': product.current_price,
                'quantity': item.quantity,
                'item_total': item_total
            })

    current_profile = {
        'id': current_user.id,
        'name': current_user.nickname,
        'img': url_for('static', filename=f'images/{current_user.avatar}')
    }

    return render_template('cart.html',
                           current_user_profile=current_profile,
                           cart_items=cart_data,
                           total_price=total_price)


@app.route('/cart/update', methods=['POST'])
@login_required
def update_cart():
    data = request.json
    item_id = data.get('item_id')
    quantity = int(data.get('quantity', 1))

    if quantity <= 0:
        return jsonify({'status': 'error', 'message': '数量必须大于0'}), 400

    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not cart_item:
        return jsonify({'status': 'error', 'message': '购物车项不存在'}), 404

    cart_item.quantity = quantity
    db.session.commit()

    # 返回更新后的小计
    product = Product.query.get(cart_item.product_id)
    item_total = product.current_price * quantity if product else 0

    return jsonify({
        'status': 'success',
        'message': '已更新',
        'item_total': item_total
    })


@app.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not cart_item:
        return jsonify({'status': 'error', 'message': '购物车项不存在'}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'status': 'success', 'message': '已从购物车移除'})

# 在现有代码中添加商品列表API（用于前端加载商品）
@app.route('/api/products')
@login_required
def get_products():
    products = Product.query.all()
    product_list = []
    for p in products:
        product_list.append({
            'id': p.id,
            'name': p.name,
            'original_price': p.original_price,
            'current_price': p.current_price,
            'seller': p.seller,
            'images': p.images,
            'sales': p.sales,
        })
    return jsonify(product_list)


# 商品详情页路由
@app.route('/product/<int:product_id>')
@login_required
def product_detail(product_id):
    # 获取商品详情
    product = Product.query.get_or_404(product_id)
    # 组装商品数据
    product_data = {
        'id': product.id,
        'name': product.name,
        'original_price': product.original_price,
        'current_price': product.current_price,
        'seller': product.seller,
        'images': url_for('static', filename=f'images/{product.images}'),
        'sales': product.sales,
        'price_desc': product.price_desc
    }
    # 获取当前用户信息
    current_profile = {
        'id': current_user.id,
        'name': current_user.nickname,
        'img': url_for('static', filename=f'images/{current_user.avatar}')
    }
    return render_template('product.html',
                         product=product_data,
                         current_user_profile=current_profile)


@app.route('/api/sales-data')
@login_required
def get_sales_data():
    # 获取销量前10的商品
    products = Product.query.order_by(Product.sales.desc()).limit(10).all()

    sales_data = []
    for product in products:
        # 提取商品简称（去掉【河池特产】前缀）
        short_name = product.name.replace('【河池特产】', '')
        sales_data.append({
            'name': short_name,
            'sales': product.sales,
            'price': product.current_price
        })

    return jsonify(sales_data)


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