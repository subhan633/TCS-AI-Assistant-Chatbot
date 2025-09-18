const API_BASE = "http://127.0.0.1:8000";  // backend URL
const SESSION_ID = localStorage.getItem("session_id") || `sess_${Date.now()}`;

// Save session ID to localStorage
localStorage.setItem("session_id", SESSION_ID);

async function sendMessage() {
  let input = document.getElementById("userInput");
  let message = input.value.trim();
  if (message === "") return;

  // Show user message
  addMessage("user", message);
  input.value = "";

  // Call backend
  try {
    let response = await fetch(`${API_BASE}/chat/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: SESSION_ID,
        query: message,
        history: []
      })
    });

    if (!response.ok) {
      let errorText = await response.text();
      console.error("Backend Error:", errorText);
      addMessage("bot", "⚠️ Backend error: " + errorText);
      return;
    }

    let data = await response.json();
    console.log("Backend Response:", data); // 🔍 Full logging

    // Show only the bot's answer (no sources)
    addMessage("bot", data.answer);

  } catch (err) {
    addMessage("bot", "⚠️ Error contacting backend.");
    console.error("Fetch Error:", err);
  }
}

function addMessage(role, text) {
  let messages = document.getElementById("messages");
  let div = document.createElement("div");
  div.className = `message ${role}`;
  div.innerText = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}
