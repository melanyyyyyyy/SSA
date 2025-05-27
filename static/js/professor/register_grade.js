document.getElementById('submit-button').addEventListener('click', function(e) {
    e.preventDefault();
    const form = document.getElementById("form-action");
    const formData = new FormData(form);
    const formAction = form.getAttribute("action");
    const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value;

    fetch(formAction, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": csrfToken },
        credentials: "include",
    })
    .then(response => response.json())
    .then(data => {
        if (data.messages?.length) {
            data.messages.forEach(msg => addMessage(msg.text, msg.tag));
        }
        if (data.success && data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    })
    .catch(error => {
        addMessage("Error inesperado al guardar. Intenta de nuevo.", "error");
        console.error("Error en la solicitud:", error);
    });
});

document.getElementById('cancel-button').addEventListener('click', function() {
    openCancelModal();
});

function openCancelModal() {
    document.getElementById('cancel-modal').classList.add('modal--show');
}

function closeCancelModal() {
    document.getElementById('cancel-modal').classList.remove('modal--show');
}

document.getElementById('accept-cancel-btn').addEventListener('click', function() {
    const url = this.getAttribute('data-href');
    if (url) {
        window.location.href = url;
    }
});

document.querySelectorAll('.table tbody tr').forEach(row => {
    row.addEventListener('click', function(e) {
        if (e.target.tagName.toLowerCase() === 'input') return;
        const input = row.querySelector('input[type="number"]');
        if (input) {
            input.focus();
        }
    });
});