document.addEventListener("DOMContentLoaded", function() {
    const navOpen = document.getElementById("nav-mobile-icon");
    const navClose = document.getElementById("navClose");
    const mainNav = document.getElementById("mainNav");


    navOpen.addEventListener("click", function() {
        mainNav.classList.add("active"); // ✅ Toggle active class
    });
    navClose.addEventListener("click", function() {
        mainNav.classList.remove("active"); // ✅ Toggle active class
    });
    
});
