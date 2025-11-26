# init_db.py（完整修改后）
from app import app
from database import db, LoginUser, Product, CartItem  # 直接从database导入模型

def custom_init_db(app):
    with app.app_context():
        db.drop_all()  # 清空现有表
        db.create_all()  # 创建所有模型表

        print("正在填充数据库...")

        # 创建测试用户（保持不变）
        demo_users = [
            LoginUser(username='admin', nickname='管理员', phone='13800138000', password='password',
                      avatar='ad123456_1__.jpg'),
            LoginUser(username='user2', nickname='用户2', phone='13800138001', password='password',
                      avatar='avatar2.jpg'),
            LoginUser(username='user3', nickname='用户3', phone='13800138002', password='password',
                      avatar='avatar3.jpg'),
            LoginUser(username='user4', nickname='用户4', phone='13800138003', password='password',
                      avatar='avatar4.jpg'),
            LoginUser(username='user5', nickname='用户5', phone='13800138004', password='password',
                      avatar='avatar5.jpg'),
        ]
        db.session.add_all(demo_users)

        # 创建初始商品数据（保持不变）
        products = [
            {
                'name': '【闪耀暖暖】明星梦礼系列毛绒挂件',
                'original_price': 129.0,
                'current_price': 99.0,
                'seller': '叠纸心意旗舰店',
                'image': '挂件.jpg'
            },
            # ... 其他商品数据（保持不变）
        ]

        # 添加商品到数据库
        for p in products:
            product = Product(
                name=p['name'],
                original_price=p['original_price'],
                current_price=p['current_price'],
                seller=p['seller'],
                image=p['image']
            )
            db.session.add(product)

        db.session.commit()
        print("数据库初始化并填充数据完成！")
        print("默认登录账号: admin, 密码: password (明文存储)")

if __name__ == '__main__':
    with app.app_context():
        print("正在手动初始化数据库...")
        custom_init_db(app)
        print("数据库初始化完成！")
        print("默认登录账号: admin, 密码: password")