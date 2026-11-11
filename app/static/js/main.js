/**
 * DeadlineOS — Main JavaScript
 * Author (Frontend): Yuvraj
 */

// ── Auto-dismiss flash alerts after 4 seconds ────────────────
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 4000);
  });
});

// ── Highlight overdue deadlines ──────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  const now = new Date();
  document.querySelectorAll('[data-due]').forEach(function (el) {
    const due = new Date(el.dataset.due);
    if (due < now) {
      el.classList.add('text-danger', 'fw-bold');
    }
  });
});
