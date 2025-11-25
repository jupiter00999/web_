document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const nickname = document.getElementById('nickname');
    const phone = document.getElementById('phone');
    const avatar = document.getElementById('avatar');
    const preview = document.getElementById('preview');

    function validateUsername() {
        const regex = /^[a-zA-Z][a-zA-Z0-9_]{5,17}$/;
        if (regex.test(username.value)) {
            username.classList.remove('is-invalid');
            return true;
        } else {
            username.classList.add('is-invalid');
            return false;
        }
    }

    function validatePassword() {
        const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,16}$/;
        if (regex.test(password.value)) {
            password.classList.remove('is-invalid');
            return true;
        } else {
            password.classList.add('is-invalid');
            return false;
        }
    }

    function validateNickname() {
        if (nickname.value.trim() !== '') {
            nickname.classList.remove('is-invalid');
            return true;
        } else {
            nickname.classList.add('is-invalid');
            return false;
        }
    }

    function validatePhone() {
        const regex = /^1[3-9]\d{9}$/;
        if (regex.test(phone.value)) {
            phone.classList.remove('is-invalid');
            return true;
        } else {
            phone.classList.add('is-invalid');
            return false;
        }
    }

    username.addEventListener('blur', validateUsername);
    password.addEventListener('blur', validatePassword);
    nickname.addEventListener('blur', validateNickname);
    phone.addEventListener('blur', validatePhone);

    avatar.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
            }
            reader.readAsDataURL(file);
        }
    });

    form.addEventListener('submit', function(event) {
        if (!validateUsername() || !validatePassword() || !validateNickname() || !validatePhone()) {
            event.preventDefault();
            event.stopPropagation();
            alert('请修正表单中的错误后再提交。');
        }
    });
});
