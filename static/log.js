
const form = document.getElementById("loginForm");
const msg  = document.getElementById("msg");
const btn  = document.getElementById("btnLogin");

function show(text, ok=false){
  msg.style.display = text ? "block" : "none";
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

  btn.disabled = true;// تعطيل الزر
  show("Logging in...", true); 

  const username = document.getElementById("username").value.trim();// ازالة الفراغات
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ username, password })
    });

    const data = await res.json().catch(()=> ({}));

    if (data.ok) {
      show("✅ Successful entry", true);
      window.location.href = "/page2";
    } else {
      show(data.message || "❌ Login failed");
    }

  } catch (err) {
    console.error(err);
    show("❌ Server or API connection problem");
  } finally {
    btn.disabled = false;
  }
});