document.addEventListener('DOMContentLoaded', function () {
    const attendance_button = document.getElementById('attendance_button');
    if (attendance_button) {
        attendance_button.addEventListener('click', function () {
            const href = attendance_button.getAttribute('data-href');
            if (href) {
                window.location.href = href;
            }
        });
    }

    const grade_button = document.getElementById('grade_button');
    if (grade_button) {
        grade_button.addEventListener('click', function () {
            const href = grade_button.getAttribute('data-href');
            if (href) {
                window.location.href = href;
            }
        });
    }

    const history_button = document.getElementById('history_button');
    if (history_button) {
        history_button.addEventListener('click', function () {
            const href = history_button.getAttribute('data-href');
            if (href) {
                window.location.href = href;
            }
        });
    }

    document.querySelectorAll('.view-details-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.stopPropagation();
            const href = btn.getAttribute('data-href');
            if (href) {
                window.location.href = href;
            }
        });
    });

    document.querySelectorAll('.table tbody tr').forEach(row => {
        row.addEventListener('click', function (e) {
            const btn = row.querySelector('.view-details-btn');
            if (btn && !e.target.closest('button')) {
                const href = btn.getAttribute('data-href');
                if (href) {
                    window.location.href = href;
                }
            }
        });
    });
});