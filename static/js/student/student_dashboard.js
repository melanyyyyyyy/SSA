document.addEventListener('DOMContentLoaded', function () {
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

    const comments = document.querySelectorAll('.comments-container .comment');
    const verMasBtn = document.getElementById('ver-mas-btn');
    let visibleCount = 3;

    function updateCommentsDisplay() {
        comments.forEach((comment, idx) => {
            comment.style.display = idx < visibleCount ? '' : 'none';
        });
        if (verMasBtn) {
            verMasBtn.style.display = visibleCount < comments.length ? '' : 'none';
        }
    }

    updateCommentsDisplay();

    if (verMasBtn) {
        verMasBtn.addEventListener('click', function () {
            visibleCount += 3;
            updateCommentsDisplay();
        });
    }
});