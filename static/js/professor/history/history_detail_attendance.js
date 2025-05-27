document.addEventListener('DOMContentLoaded', function () {
    const editBtn = document.getElementById('edit-btn');
    const saveBtn = document.getElementById('save-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const form = document.getElementById('edit-attendance-form');
    const inputs = form.querySelectorAll('input[type="checkbox"]');
    const table = form.closest('.table-container').querySelector('.table');

    editBtn.addEventListener('click', function () {
        inputs.forEach(inp => inp.disabled = false);
        editBtn.style.display = 'none';
        saveBtn.style.display = '';
        cancelBtn.style.display = '';
        table.classList.add('editing');
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
        table.classList.remove('editing');
        inputs.forEach(inp => inp.disabled = true);
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
                    if (data.messages?.length) {
                        localStorage.setItem('successMessages', JSON.stringify(data.messages));
                    }
                    window.location.reload();
                }
                if (data.messages?.length && !data.success) {
                    data.messages.forEach(msg => addMessage(msg.text, msg.tag));
                }
            })
            .catch(() => {
                addMessage("Error inesperado al guardar. Intenta de nuevo.", "error");
            });
    });

    const stored = localStorage.getItem('successMessages');
    if (stored) {
        try {
            const msgs = JSON.parse(stored);
            msgs.forEach(msg => addMessage(msg.text, msg.tag));
        } catch { }
        localStorage.removeItem('successMessages');
    }

    document.querySelectorAll('.table tbody tr').forEach(row => {
        row.addEventListener('click', function (e) {
            if (e.target.closest('input[type="checkbox"]') || e.target.closest('label')) return;
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox && !checkbox.disabled) {
                checkbox.click();
            }
        });
    });
});