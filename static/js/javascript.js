
const menuIcon = document.querySelector(".menu-icon")
const navBar = document.querySelector(".navbar")

menuIcon.addEventListener("click", function(){
    navBar.classList.toggle("active")
})