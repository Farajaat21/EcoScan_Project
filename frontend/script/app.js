document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMainList = document.querySelector('.nav-main-list');

    hamburger.addEventListener('click', function() {
        navMainList.classList.toggle('active');
    });
});