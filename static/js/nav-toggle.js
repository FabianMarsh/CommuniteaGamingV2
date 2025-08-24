export function initNavToggle() {
  const navOpen = document.getElementById("navMobileIcon");
  const navClose = document.getElementById("navClose");
  const mainNav = document.getElementById("mainNav");

  if (!navOpen || !navClose || !mainNav) return;

  navOpen.addEventListener("click", () => {
    mainNav.classList.add("active");
  });

  navClose.addEventListener("click", () => {
    mainNav.classList.remove("active");
  });
}
