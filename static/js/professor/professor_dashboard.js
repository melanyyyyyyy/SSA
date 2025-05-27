const filas = document.querySelectorAll('.table tbody tr');
const modal = document.querySelector('.modal');

filas.forEach(fila => {
    fila.addEventListener('click', () => {
        const href = fila.getAttribute('data-href');
        if (href) {
            window.location.href = href;
        }
    });
});

function showModal(action) {
    let modalAccept = modal.querySelector('.modal-accept');
    let modalCancel = modal.querySelector('.modal-cancel');

    const newAccept = modalAccept.cloneNode(true);
    modalAccept.parentNode.replaceChild(newAccept, modalAccept);

    const newCancel = modalCancel.cloneNode(true);
    modalCancel.parentNode.replaceChild(newCancel, modalCancel);

    modalAccept = modal.querySelector('.modal-accept');
    modalCancel = modal.querySelector('.modal-cancel');

    modalAccept.addEventListener('click', () => {
        if (typeof action === "function") action();
        modal.classList.remove('modal--show');
    });
    modalCancel.addEventListener('click', () => {
        modal.classList.remove('modal--show');
    });

    modal.classList.add('modal--show');
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.comment-delete-button').forEach(button => {
        button.addEventListener('click', function () {
            const form = this.closest('.comment-delete-form');
            const formAction = form.getAttribute("action");
            const csrfToken = form.querySelector("input[name=csrfmiddlewaretokendeletecomment]").value;

            showModal(() => {
                fetch(formAction, {
                    method: "POST",
                    headers: { "X-CSRFToken": csrfToken },
                    credentials: "include",
                })
                .then(response => response.json())
                .then(data => {
                    if (data.messages?.length) {
                        data.messages.forEach(msg => addMessage(msg.text, msg.tag));
                    }
                    if (data.success) {
                        const comment = form.closest('.comment');
                        comment.classList.add("fade-out");
                        setTimeout(() => {
                            comment.remove();
                            if (visibleCount > 3) visibleCount = 3;
                            updateCommentsDisplay();
                            const container = document.querySelector('.comments-container');
                            if (container.querySelectorAll('.comment').length === 0) {
                                const noComments = document.createElement('h3');
                                noComments.className = 'title element-not-found';
                                noComments.innerText = 'No hay comentarios disponibles.';
                                container.appendChild(noComments);
                            }
                        }, 500);
                    }
                })
                .catch(error => {
                    addMessage("Error inesperado al eliminar. Intenta de nuevo.", "error");
                    console.error("Error en la solicitud:", error);
                });
            });
        });
    });
});

let visibleCount = 3;

function updateCommentsDisplay() {
    const comments = document.querySelectorAll('#comments-container .comment');
    const verMasBtn = document.getElementById('ver-mas-btn');
    if (visibleCount > comments.length) {
        visibleCount = comments.length;
    }
    comments.forEach((comment, idx) => {
        comment.style.display = idx < visibleCount ? '' : 'none';
    });
    if (visibleCount < comments.length) {
        verMasBtn.style.display = '';
    } else {
        verMasBtn.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const comments = document.querySelectorAll('#comments-container .comment');
    const verMasBtn = document.getElementById('ver-mas-btn');
    updateCommentsDisplay();
    if (verMasBtn) {
        verMasBtn.addEventListener('click', function () {
            visibleCount += 3;
            updateCommentsDisplay();
        });
    }
});