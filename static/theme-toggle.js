
document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('theme-switch');
    const isDark = localStorage.getItem('theme') === 'dark';

    if (isDark) {
        document.body.classList.add('dark-mode');
        toggle.checked = true;
    }

    toggle.addEventListener('change', function () {
        if (this.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light');
        }
    });
});
