function debounce(func, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(this, args), delay);
    };
}

const checkCredentials = debounce(function () {
    const username = document.querySelector('input[name="username"]').value;
    const password = document.querySelector('input[name="password"]').value;
    
    if (username.length < 3 || password.length < 3) return;

    const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    
    fetch('/login/check/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ username, password })
    })
        .then(response => response.json())
        .then(data => {
            const errorMessage = document.getElementById('error-message');
            if (data.success) {
                errorMessage.textContent = 'Inicio de sesión exitoso';
                errorMessage.style.color = 'green';
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 1000);
            } else {
                errorMessage.textContent = data.error;
                errorMessage.style.color = 'red';
            }
        });
}, 500); 


document.addEventListener('DOMContentLoaded', () => {
    const passwordInput = document.querySelector('input[name="password"]');
    const showPasswordDiv = document.getElementById('show-password');
    const showPasswordImg = showPasswordDiv.querySelector('img');

    const eyeOpen = showPasswordDiv.getAttribute('data-eye-open');
    const eyeClosed = showPasswordDiv.getAttribute('data-eye-closed');
    
    showPasswordImg.setAttribute('src', eyeOpen);

    showPasswordDiv.addEventListener('click', () => {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            showPasswordImg.setAttribute('src', eyeClosed);
        } else {
            passwordInput.type = 'password';
            showPasswordImg.setAttribute('src', eyeOpen);
        }
    });
});


document.querySelector('input[name="username"]').addEventListener('input', checkCredentials);
document.querySelector('input[name="password"]').addEventListener('input', checkCredentials);
