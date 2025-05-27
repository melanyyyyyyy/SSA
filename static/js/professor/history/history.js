function showModal(action) {
    const modal = document.querySelector('.modal');
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

function addEmptyRow(tableSelector, colspan, message) {
    const tbody = document.querySelector(tableSelector + ' tbody');
    if (tbody) {
        const dataRows = Array.from(tbody.querySelectorAll('tr')).filter(tr => 
            !tr.textContent.trim().startsWith('No hay registros')
        );
        if (dataRows.length === 0) {
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            td.colSpan = colspan;
            td.textContent = message;
            tr.appendChild(td);
            tbody.appendChild(tr);
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.attendance-delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const date = btn.getAttribute('data-date');
            const subject_id = btn.getAttribute('data-subject');
            showModal(() => {
                fetch('/professor/dashboard/history/delete_attendance/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('input[name=csrfmiddlewaretoken]').value,
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: `subject_id=${subject_id}&date=${date}`,
                    credentials: "include"
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        btn.closest('tr').remove();
                        addEmptyRow('.table:nth-of-type(2)', 3, 'No hay registros de asistencia.');
                    }
                    if (data.messages) {
                        data.messages.forEach(msg => addMessage(msg.text, msg.tag));
                    }
                });
            });
        });
    });
    
    document.querySelectorAll('.grade-delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const date = btn.getAttribute('data-date');
            const name = btn.getAttribute('data-name');
            const subject_id = btn.getAttribute('data-subject');
            showModal(() => {
                fetch('/professor/dashboard/history/delete_grade/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('input[name=csrfmiddlewaretoken]').value,
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: `subject_id=${subject_id}&date=${date}&name=${encodeURIComponent(name)}`,
                    credentials: "include"
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        btn.closest('tr').remove();
                        addEmptyRow('.table:nth-of-type(1)', 4, 'No hay registros de evaluaciones.');
                    }
                    if (data.messages) {
                        data.messages.forEach(msg => addMessage(msg.text, msg.tag));
                    }
                });
            });
        });
    });
});


document.querySelectorAll('.attendance-row, .grade-row').forEach(fila => {
    fila.addEventListener('click', function(e) {

        if (e.target.closest('button')) return;
        const href = fila.getAttribute('data-href');
        if (href) {
            window.location.href = href;
        }
    });
});

document.querySelectorAll('.attendance-row .action-btn:not(.attendance-delete-btn), .grade-row .action-btn:not(.grade-delete-btn)').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.stopPropagation(); 
        const fila = btn.closest('tr');
        const href = fila.getAttribute('data-href');
        if (href) {
            window.location.href = href;
        }
    });
});