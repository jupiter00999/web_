// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 加载商品列表
    loadProducts();
    // 加载购物车数量
    loadCartCount();
    // 绑定购物车按钮事件
    document.getElementById('cart-btn').addEventListener('click', showCart);
    document.getElementById('close-cart').addEventListener('click', hideCart);
});

// 加载商品列表
function loadProducts() {
    fetch('/api/products')
        .then(res => res.json())
        .then(products => {
            const list = document.getElementById('product-list');
            products.forEach(product => {
                const li = document.createElement('li');
                li.className = 'good_li';
                li.innerHTML = `
                    <a href="#">
                        <img src="${product.image}" alt="${product.name}">
                        <div class="gname">${product.name}</div>
                        <div class="gprice">
                            ${product.original_price ? `<span id="old">￥${product.original_price}</span>` : ''}
                            <span id="new">￥${product.current_price}</span>  <!-- 修复：price → current_price -->
                        </div>
                        <div class="gseller">${product.seller}</div>
                        <button class="add-to-cart-btn" data-id="${product.id}" style="margin-top: 10px; width: 100%; padding: 5px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">
                            加入购物车
                        </button>
                    </a>
                `;
                list.appendChild(li);
            });

            // 绑定加入购物车按钮事件
            document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.preventDefault();
                    const productId = this.getAttribute('data-id');
                    addToCart(productId);
                });
            });
        });
}

// 添加到购物车
function addToCart(productId) {
    fetch('/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productId, quantity: 1 })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        loadCartCount(); // 更新购物车数量
    });
}

// 加载购物车数量
function loadCartCount() {
    fetch('/cart')
        .then(res => res.json())
        .then(items => {
            const count = items.reduce((total, item) => total + item.quantity, 0);
            document.getElementById('cart-count').textContent = count;
        });
}

// 显示购物车
function showCart() {
    fetch('/cart')  // 修复：API路径与app.py对应
        .then(res => res.json())
        .then(items => {
            const cartItems = document.getElementById('cart-items');
            cartItems.innerHTML = '';

            if (items.length === 0) {
                cartItems.innerHTML = '<p>购物车是空的</p>';
                document.getElementById('cart-total').textContent = '';
                return;
            }

            let total = 0;
            items.forEach(item => {
                total += item.item_total;
                const div = document.createElement('div');
                div.style.padding = '10px 0';
                div.style.borderBottom = '1px solid #eee';
                div.innerHTML = `
                    <img src="${item.image}" style="width: 50px; height: 50px; object-fit: cover;">
                    <span style="margin-left: 10px;">${item.name}</span>
                    <span style="margin-left: 10px; color: red;">￥${item.current_price}</span> 
                    <span style="margin-left: 10px;">数量: ${item.quantity}</span>
                    <span style="margin-left: 10px;">小计: ￥${item.item_total}</span>  
                `;
                cartItems.appendChild(div);
            });

            document.getElementById('cart-total').textContent = `总计: ￥${total.toFixed(2)}`;
            document.getElementById('cart-modal').style.display = 'block';
        });
}

// 隐藏购物车
function hideCart() {
    document.getElementById('cart-modal').style.display = 'none';
}