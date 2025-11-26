document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const nickname = document.getElementById('nickname');
    const phone = document.getElementById('phone');
    const avatar = document.getElementById('avatar');
    const preview = document.getElementById('preview');

    // 验证逻辑
    function validate() {
        let isValid = true;

        // 用户名验证（字母开头，6-18位字母/数字/下划线）
        const usernameRegex = /^[a-zA-Z][a-zA-Z0-9_]{5,17}$/;
        if (!usernameRegex.test(username.value)) {
            username.classList.add('is-invalid');
            isValid = false;
        } else {
            username.classList.remove('is-invalid');
        }

        // 密码验证（8-16位，含大小写字母+数字）
        const pwdRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,16}$/;
        if (!pwdRegex.test(password.value)) {
            password.classList.add('is-invalid');
            isValid = false;
        } else {
            password.classList.remove('is-invalid');
        }

        // 昵称验证（非空）
        if (nickname.value.trim() === '') {
            nickname.classList.add('is-invalid');
            isValid = false;
        } else {
            nickname.classList.remove('is-invalid');
        }

        // 手机号验证（11位有效手机号）
        const phoneRegex = /^1[3-9]\d{9}$/;
        if (!phoneRegex.test(phone.value)) {
            phone.classList.add('is-invalid');
            isValid = false;
        } else {
            phone.classList.remove('is-invalid');
        }

        return isValid;
    }

    // 输入框失焦验证（保留，实时反馈错误）
    [username, password, nickname, phone].forEach(input => {
        input.addEventListener('blur', validate);
    });

    // 头像预览（核心功能，保留）
    avatar.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = e => preview.src = e.target.result;
            reader.readAsDataURL(file);
        }
    });

    // 表单提交验证（简化逻辑）
    form.addEventListener('submit', function(event) {
        if (!validate()) {
            event.preventDefault();
            event.stopPropagation();
            alert('请修正表单中的错误后再提交。');
        }
    });
});