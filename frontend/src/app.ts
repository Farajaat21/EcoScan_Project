document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.querySelector('.hamburger');
  const navMainList = document.querySelector('.nav-main-list');

  if (!hamburger || !navMainList) return;

  hamburger.addEventListener('click', () => {
    navMainList.classList.toggle('active');
  });
});
