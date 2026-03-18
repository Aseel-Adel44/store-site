
  // الحصول على التاريخ الحالي
  const today = new Date();

  // تحويل التاريخ إلى شكل قابل للقراءة (مثال: 14 مارس 2026)
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  const formattedDate = today.toLocaleDateString('en-JO', options);

  // عرض التاريخ في العنصر
  document.getElementById('entry-date').textContent = formattedDate;

  //تعديل المعلومات 


function toggleEdit() {
    const form = document.getElementById("edit-form");
    form.style.display = (form.style.display === "none") ? "block" : "none";
}

function saveChanges() {
    const firstName = document.getElementById("first_name_input").value;
    const phone = document.getElementById("phone_input").value;

    fetch("/edit_profile_ajax", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({first_name: firstName, phone: phone})
    })
    .then(res => res.json())
    .then(data => {
        if(data.ok){
            // تحديث النصوص مباشرة في الصفحة
            document.getElementById("first_name_display").innerText = firstName;
            document.getElementById("phone_display").innerText = phone;
            toggleEdit();
            alert("Changes saved successfully!");
        } else {
            alert("Error: " + data.message);
        }
    });
}


