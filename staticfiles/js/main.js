document.addEventListener("DOMContentLoaded", function() {
    const navOpen = document.getElementById("nav_mobile_icon");
    const navClose = document.getElementById("nav_close");
    const mainNav = document.getElementById("main-nav");


    navOpen.addEventListener("click", function() {
        mainNav.classList.add("active"); // ✅ Toggle active class
    });
    navClose.addEventListener("click", function() {
        mainNav.classList.remove("active"); // ✅ Toggle active class
    });
    
});
