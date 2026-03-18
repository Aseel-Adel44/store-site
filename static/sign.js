const form = document.getElementById("signupForm");
const msg  = document.getElementById("msg");

function show(text, ok=false){
  msg.style.display = "block";
  msg.textContent = text;

  if (ok) {
    msg.style.color = "#16a34a";
    msg.style.background = "rgba(22,163,74,.08)";
    msg.style.border = "1px solid rgba(22,163,74,.20)";
  } else {
    msg.style.color = "#ef4444";
    msg.style.background = "rgba(239,68,68,.08)";
    msg.style.border = "1px solid rgba(239,68,68,.20)";
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const firstName = document.getElementById("firstName").value.trim();
  const lastName = document.getElementById("lastName").value.trim();
  const phoneNumber = document.getElementById("phoneNumber").value.trim();
  const password = document.getElementById("password").value;
  const password2 = document.getElementById("password2").value;

  if (password !== password2) {
    show("The two passwords do not match.");
    return;
  }

  try {
    const res = await fetch("/api/signup", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ username, email, firstName, lastName, phoneNumber, password ,password2 })
    });

    const data = await res.json().catch(()=> ({}));

    if (data.ok) {
      show("✅ Account created successfully", true);   
     setTimeout(() => window.location.href = "/", 1200);
    } else {
      show(data.message || "❌ Account creation failed");  
    }
  } catch (err) {
    console.error(err);
    show("❌ Server connection problem");
  }
}); 