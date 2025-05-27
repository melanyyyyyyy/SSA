document.addEventListener('DOMContentLoaded', function () {
    const editAttendanceBtn = document.getElementById('edit-attendance-btn');
    const saveAttendanceBtn = document.getElementById('save-attendance-btn');
    const cancelAttendanceBtn = document.getElementById('cancel-attendance-btn');
    const attendanceForm = document.getElementById('edit-attendance-form');
    const attendanceInputs = attendanceForm.querySelectorAll('input[type="checkbox"]');
    const attendanceTable = attendanceForm.querySelector('.table');

    editAttendanceBtn.addEventListener('click', function () {
        attendanceInputs.forEach(inp => inp.disabled = false);
        editAttendanceBtn.style.display = 'none';
        saveAttendanceBtn.style.display = '';
        cancelAttendanceBtn.style.display = '';
        attendanceTable.classList.add('editing');
    });

    cancelAttendanceBtn.addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('cancel-attendance-modal').classList.add('modal--show');
        attendanceTable.classList.remove('editing');
    });

    const cancelAttendanceModal = document.getElementById('cancel-attendance-modal');
    if (cancelAttendanceModal) {
        const acceptBtn = cancelAttendanceModal.querySelector('.modal-accept');
        const cancelModalBtn = cancelAttendanceModal.querySelector('.modal-cancel');
        acceptBtn.addEventListener('click', function () {
            window.location.reload();
        });
        cancelModalBtn.addEventListener('click', function () {
            cancelAttendanceModal.classList.remove('modal--show');
        });
    }

    attendanceForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(attendanceForm);
        fetch(attendanceForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': attendanceForm.querySelector('input[name=csrfmiddlewaretoken]').value
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

    const editGradeBtn = document.getElementById('edit-grade-btn');
    const saveGradeBtn = document.getElementById('save-grade-btn');
    const cancelGradeBtn = document.getElementById('cancel-grade-btn');
    const gradeForm = document.getElementById('edit-grade-form');
    const gradeInputs = gradeForm.querySelectorAll('input[type="number"]');
    const gradeTable = gradeForm.querySelector('.table');

    editGradeBtn.addEventListener('click', function () {
        gradeInputs.forEach(inp => inp.disabled = false);
        editGradeBtn.style.display = 'none';
        saveGradeBtn.style.display = '';
        cancelGradeBtn.style.display = '';
        gradeTable.classList.add('editing');
    });

    cancelGradeBtn.addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('cancel-grade-modal').classList.add('modal--show');
        gradeTable.classList.remove('editing');
    });

    const cancelGradeModal = document.getElementById('cancel-grade-modal');
    if (cancelGradeModal) {
        const acceptBtn = cancelGradeModal.querySelector('.modal-accept');
        const cancelModalBtn = cancelGradeModal.querySelector('.modal-cancel');
        acceptBtn.addEventListener('click', function () {
            window.location.reload();
        });
        cancelModalBtn.addEventListener('click', function () {
            cancelGradeModal.classList.remove('modal--show');
        });
    }

    gradeForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(gradeForm);
        fetch(gradeForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': gradeForm.querySelector('input[name=csrfmiddlewaretoken]').value
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

    gradeTable.querySelectorAll('tbody tr').forEach(row => {
        row.addEventListener('click', function (e) {
            if (e.target.tagName.toLowerCase() === 'input') return;
            if (gradeTable.classList.contains('editing')) {
                const input = row.querySelector('input[type="number"]');
                if (input && !input.disabled) {
                    input.focus();
                }
            }
        });
    });

    attendanceTable.querySelectorAll('tbody tr').forEach(row => {
        row.addEventListener('click', function (e) {
            if (!attendanceTable.classList.contains('editing')) return;
            if (e.target.closest('input[type="checkbox"]')) return;
            if (e.target.closest('label')) return;
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox && !checkbox.disabled) {
                checkbox.click();
            }
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
});