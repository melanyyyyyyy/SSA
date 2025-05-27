function openModal() {
    document.getElementById('logout-modal').classList.add('modal--show');
}

function closeModal() {
    document.getElementById('logout-modal').classList.remove('modal--show');
}

function logout(logoutUrl) {
    window.location.href = logoutUrl;
}

function addMessage(text, type) {
    const messageContainer = document.getElementById("messages");

    const div = document.createElement("div");
    div.className = `alert alert-${type}`;
    div.textContent = text;
    messageContainer.appendChild(div);

    while (messageContainer.children.length > 3) {
        messageContainer.firstChild.remove();
    }

    setTimeout(() => {
        div.classList.add("fade-out");
        setTimeout(() => {
            if (div.parentNode) div.remove();
        }, 500);
    }, 3000);
}

document.addEventListener("DOMContentLoaded", function() {
    if (window.data?.messages?.length) {
        window.data.messages.forEach(msg => addMessage(msg.text, msg.tag));
    }
});