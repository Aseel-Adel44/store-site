let list=document.querySelectorAll('.list');

function activeLink(){
    list.forEach((item)=>
        item.classList.remove('active'));
    this.classList.add('active');

}
 list.forEach((item)=>
    item.addEventListener('click',activeLink));

/*buttom language*/
 function toggleLanguageMenu(e){
    e.preventDefault();
    let menu = document.getElementById("languageDropdown");

    if(menu.style.display === "block"){
        menu.style.display = "none";
    }else{
        menu.style.display = "block";
    }
}

function setLanguage(lang){
    if(lang === "ar"){
        alert("تم اختيار اللغة العربية");
    }else{
        alert("English selected");
    }
     languageDropdown.style.display = "none"; // إغلاق القائمة بعد اختيار اللغة

}