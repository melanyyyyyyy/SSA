document.addEventListener('DOMContentLoaded', function () {
    const editBtn = document.getElementById('edit-btn');
    const saveBtn = document.getElementById('save-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const form = document.getElementById('edit-grade-form');
    const inputs = form.querySelectorAll('input[type="number"]');
    const messagesDiv = document.getElementById('messages');

    editBtn.addEventListener('click', function () {
        inputs.forEach(inp => inp.disabled = false);
        editBtn.style.display = 'none';
        saveBtn.style.display = '';
        cancelBtn.style.display = '';
        form.closest('.table-container').querySelector('.table').classList.add('editing');
    });

    function openCancelModal() {
        document.getElementById('cancel-modal').classList.add('modal--show');
    }

    function closeCancelModal() {
        document.getElementById('cancel-modal').classList.remove('modal--show');
    }

    cancelBtn.addEventListener('click', function (e) {
        e.preventDefault();
        openCancelModal();
        form.closest('.table-container').querySelector('.table').classList.remove('editing');
    });

    const modal = document.getElementById('cancel-modal');
    if (modal) {
        const acceptBtn = modal.querySelector('.modal-accept');
        const cancelModalBtn = modal.querySelector('.modal-cancel');

        acceptBtn.addEventListener('click', function () {
            window.location.reload();
        });
        cancelModalBtn.addEventListener('click', function () {
            closeCancelModal();
        });
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': form.querySelector('input[name=csrfmiddlewaretoken]').value
            },
            credentials: "include"
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                }
                if (data.messages?.length) {
                    data.messages.forEach(msg => addMessage(msg.text, msg.tag));
                }
            })
            .catch(() => {
                addMessage("Error inesperado al eliminar. Intenta de nuevo.", "error");
            });
    });

    document.querySelectorAll('.table tbody tr').forEach(row => {
        row.addEventListener('click', function (e) {
            if (e.target.tagName.toLowerCase() === 'input') return;
            const input = row.querySelector('input[type="number"]');
            if (input) {
                input.focus();
            }
        });
    });
});