// 超极简版本（仅保留提交时验证）
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const username = document.getElementById('username');
    const password = document.getElementById('password');

    function validate() {
        const userValid = username.value.trim() !== '';
        const pwdValid = password.value.trim() !== '';
        username.classList.toggle('is-invalid', !userValid);
        password.classList.toggle('is-invalid', !pwdValid);
        return userValid && pwdValid;
    }

    form.addEventListener('submit', function(event) {
        if (!validate()) {
            event.preventDefault();
            alert('请填写完整的登录信息');
        }
    });
});