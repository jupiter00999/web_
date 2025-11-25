document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const historyDropdown = document.getElementById('historyDropdown');
    const historyList = document.getElementById('historyList');
    const clearHistoryBtn = document.getElementById('clearHistory');

    // 从本地存储获取历史记录
    function getHistory() {
        const history = localStorage.getItem('loginHistory');
        return history ? JSON.parse(history) : [];
    }

    // 保存历史记录
    function saveHistory(username) {
        let history = getHistory();
        // 去重并保持最新在前
        history = history.filter(item => item !== username);
        history.unshift(username);
        // 限制最多保存10条记录
        if (history.length > 10) {
            history = history.slice(0, 10);
        }
        localStorage.setItem('loginHistory', JSON.stringify(history));
    }

    // 显示历史记录
    function showHistory() {
        const history = getHistory();
        historyList.innerHTML = '';

        if (history.length === 0) {
            historyDropdown.style.display = 'none';
            return;
        }

        history.forEach(item => {
            const div = document.createElement('div');
            div.className = 'history-item';
            div.textContent = item;
            div.addEventListener('click', () => {
                username.value = item;
                historyDropdown.style.display = 'none';
                password.focus();
            });
            historyList.appendChild(div);
        });

        historyDropdown.style.display = 'block';
    }

    // 隐藏历史记录
    function hideHistory() {
        // 延迟隐藏，避免点击历史项时被立即隐藏
        setTimeout(() => {
            if (!historyDropdown.matches(':hover') &&
                document.activeElement !== username) {
                historyDropdown.style.display = 'none';
            }
        }, 200);
    }

    // 清除历史记录
    function clearHistory() {
        localStorage.removeItem('loginHistory');
        historyList.innerHTML = '';
        historyDropdown.style.display = 'none';
    }

    // 验证函数
    function validateUsername() {
        if (username.value.trim() !== '') {
            username.classList.remove('is-invalid');
            return true;
        } else {
            username.classList.add('is-invalid');
            return false;
        }
    }

    function validatePassword() {
        if (password.value.trim() !== '') {
            password.classList.remove('is-invalid');
            return true;
        } else {
            password.classList.add('is-invalid');
            return false;
        }
    }

    // 事件监听
    username.addEventListener('focus', showHistory);
    username.addEventListener('blur', hideHistory);
    username.addEventListener('input', () => {
        // 输入时也显示匹配的历史记录
        showHistory();
    });

    historyDropdown.addEventListener('mouseleave', hideHistory);
    clearHistoryBtn.addEventListener('click', clearHistory);

    username.addEventListener('blur', validateUsername);
    password.addEventListener('blur', validatePassword);

    // 表单提交时保存用户名到历史记录
    form.addEventListener('submit', function(event) {
        if (validateUsername() && validatePassword()) {
            saveHistory(username.value.trim());
        } else {
            event.preventDefault();
            event.stopPropagation();
            alert('请填写完整的登录信息');
        }
    });
});