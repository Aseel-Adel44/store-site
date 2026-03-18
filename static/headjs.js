// ====== تحميل السلة من LocalStorage عند بداية الصفحة ======
let username = document.body.dataset.user;
let cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
let total = JSON.parse(localStorage.getItem('total_' + username)) || 0;

// تحديث السلة بعد تحميل الصفحة
document.addEventListener("DOMContentLoaded", function(){
    updateCartUI();
});
// ====== إضافة جهاز للسلة ======
function addToCart(productName, price = 0){
    cart.push({name: productName, price: price});
    total += price;

    saveCart();   // حفظ السلة في localStorage
    updateCartUI();

    // عرض Popup
    const popup = document.getElementById('cart-popup');
    popup.innerText = `${productName} added to cart!`;
    popup.style.display = 'block';
    setTimeout(() => { popup.style.display = 'none'; }, 2000);
}

// ====== حفظ السلة في LocalStorage ======
function saveCart(){
     localStorage.setItem('cart_' + username, JSON.stringify(cart));

    localStorage.setItem('total_' + username, JSON.stringify(total));}


// ====== تحديث واجهة السلة ======
function updateCartUI(){
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';

    cart.forEach((item, index) => {
        const li = document.createElement('li');
        li.innerHTML = `${item.name} - ${item.price} JOD
            <button class="remove-item" onclick="removeFromCart(${index})">Delete</button>`;
        cartItems.appendChild(li);
    });

    document.getElementById('cart-total').innerText = `Total: ${total} JOD`;
    document.getElementById("cart-count").innerText = cart.length;
}

// ====== حذف عنصر من السلة ======
function removeFromCart(index){
    total -= cart[index].price;
    cart.splice(index,1);
    saveCart();      // تحديث LocalStorage
    updateCartUI();
}

// ====== تأكيد الطلب ======
function confirmOrder(){
    if(cart.length === 0){
        alert("The shopping basket is empty!");
        return;
    }

    // يمكنك مسح السلة بعد التأكيد
    cart = [];
    total = 0;
    saveCart();
    updateCartUI();

    const popup = document.getElementById('cart-popup');
    popup.innerText = "The order has been successfully confirmed!";
    popup.style.display = 'block';
    setTimeout(() => { popup.style.display = 'none'; }, 10000);
}

// ====== فتح وغلق السلة ======
function toggleCart(){
    const cartElement = document.querySelector(".cart-container");
    cartElement.classList.toggle("active");
}

//اضافه صوره 

let products = {

head1:[
"/static/images/head1.webp",
"/static/images/head.webp"
],

head2:[
"/static/images/jbl.webp",
"/static/images/jbl1.webp",
"/static/images/jbl2.webp"
],

head3:[
"/static/images/airbuds.png",
"/static/images/airbuds1.png"
]

};

let index = {
head1:0,
head2:0,
head3:0
};

function nextImage(product){

index[product]++;

if(index[product] >= products[product].length){
index[product] = 0;
}

document.getElementById(product + "-img").src = products[product][index[product]];

}

function prevImage(product){

index[product]--;

if(index[product] < 0){
index[product] = products[product].length - 1;
}

document.getElementById(product + "-img").src = products[product][index[product]];

}