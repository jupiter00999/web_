# init_db.py（完整修改后）
from werkzeug.security import generate_password_hash

from app import app
from database import db, LoginUser, Product, CartItem  # 直接从database导入模型

def custom_init_db(app):
    with app.app_context():
        db.drop_all()  # 清空现有表
        db.create_all()  # 创建所有模型表

        print("正在填充数据库...")

        # 创建测试用户（保持不变）
        demo_users = [
            LoginUser(
                username='admin',
                nickname='管理员',
                phone='13800138000',
                password=generate_password_hash('password'),  # 加密
                avatar='ad123456_1__.jpg'
            ),
            # 其他用户同理...
        ]
        # demo_users = [
        #     LoginUser(username='admin', nickname='管理员', phone='13800138000', password='password',
        #               avatar='ad123456_1__.jpg'),
        #     LoginUser(username='user2', nickname='用户2', phone='13800138001', password='password',
        #               avatar='avatar2.jpg'),
        #     LoginUser(username='user3', nickname='用户3', phone='13800138002', password='password',
        #               avatar='avatar3.jpg'),
        #     LoginUser(username='user4', nickname='用户4', phone='13800138003', password='password',
        #               avatar='avatar4.jpg'),
        #     LoginUser(username='user5', nickname='用户5', phone='13800138004', password='password',
        #               avatar='avatar5.jpg'),
        # ]
        db.session.add_all(demo_users)

        # 创建初始商品数据（保持不变）
        products = [
            {
                'name': '【河池特产】环江香牛 精品牛肉礼盒',
                'original_price': 168.0,
                'current_price': 128.0,
                'seller': '环江农家直销',
                'images': '农产品 (13).png',
                'price_desc': '￥128/盒',
                'sales': 156  # 添加销量数据
            },
            {
                'name': '【河池特产】南丹瑶鸡 散养土鸡',
                'original_price': 98.0,
                'current_price': 78.0,
                'seller': '瑶乡生态农场',
                'images': '农产品 (12).png',
                'price_desc': '￥78/只',
                'sales': 89
            },
            # ... 其他商品也添加sales字段
            {
                'name': '【河池特产】大化大头鱼 生态活鱼',
                'original_price': 68.0,
                'current_price': 48.0,
                'seller': '大化渔夫码头',
                'images': '农产品 (11).png',
                'price_desc': '￥48/千克',
                'sales': 234
            },
            {
                'name': '【河池特产】东兰墨米 营养黑糯米',
                'original_price': 45.0,
                'current_price': 35.0,
                'seller': '东兰稻香人家',
                'images': '农产品 (9).png',
                'price_desc': '￥35/袋',
                'sales': 167
            },
            {
                'name': '【河池特产】都安山羊 精品羊肉',
                'original_price': 188.0,
                'current_price': 158.0,
                'seller': '都安牧业合作社',
                'images': '农产品 (8).png',
                'price_desc': '￥158/千克',
                'sales': 78
            },
            {
                'name': '【河池特产】巴马香猪 迷你烤乳猪',
                'original_price': 298.0,
                'current_price': 238.0,
                'seller': '巴马长寿村特产',
                'images': '农产品 (6).png',
                'price_desc': '￥238/只',
                'sales': 45
            },
            {
                'name': '【河池特产】河池板栗 甜糯板栗',
                'original_price': 38.0,
                'current_price': 28.0,
                'seller': '桂北山货铺',
                'images': '农产品 (7).png',
                'price_desc': '￥28/斤',
                'sales': 289
            },
            {
                'name': '【河池特产】罗城野生毛葡萄 新鲜采摘',
                'original_price': 35.0,
                'current_price': 25.0,
                'seller': '罗城果香园',
                'images': '农产品 (5).png',
                'price_desc': '￥25/斤',
                'sales': 312
            },
            {
                'name': '【河池特产】天峨珍珠李 甜脆李子',
                'original_price': 42.0,
                'current_price': 32.0,
                'seller': '天峨山珍',
                'images': '农产品 (1).png',
                'price_desc': '￥32/斤',
                'sales': 198
            },
            {
                'name': '【河池特产】凤山核桃 薄壳核桃',
                'original_price': 68.0,
                'current_price': 52.0,
                'seller': '凤山坚果坊',
                'images': '农产品 (2).png',
                'price_desc': '￥52/袋',
                'sales': 145
            },
            {
                'name': '【河池特产】宜州桑蚕丝 优质蚕丝被',
                'original_price': 388.0,
                'current_price': 298.0,
                'seller': '宜州丝绸坊',
                'images': '农产品 (3).png',
                'price_desc': '￥298/床',
                'sales': 67
            },
            {
                'name': '【测试机哦】宜州桑蚕丝 优质蚕丝被',
                'original_price': 388.0,
                'current_price': 298.0,
                'seller': '宜州丝绸坊',
                'images': '农产品 (3).png',
                'price_desc': '￥298/床',
                'sales': 67
            }

        ]

        # 添加商品到数据库
        for p in products:
            product = Product(
                name=p['name'],
                original_price=p['original_price'],
                current_price=p['current_price'],
                seller=p['seller'],
                images=p['images'],
                price_desc=p['price_desc'],
                sales=p['sales']  # 添加销量
            )
            db.session.add(product)

        db.session.commit()
        print("数据库初始化并填充数据完成！")
        print("默认登录账号: admin, 密码: password (文存储)")

if __name__ == '__main__':
    with app.app_context():
        print("正在手动初始化数据库...")
        custom_init_db(app)
        print("数据库初始化完成！")
        print("默认登录账号: admin, 密码: password")