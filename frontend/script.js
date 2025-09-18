const API_BASE = "http://127.0.0.1:8000";   // change if backend hosted elsewhere
const SESSION_ID = localStorage.getItem("session_id") || `sess_${Date.now()}`;
localStorage.setItem("session_id", SESSION_ID);

const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const messagesEl = document.getElementById("messages");
const chatbox = document.getElementById("chatbox");

let isSending = false; // prevent double sends

// Attach events
sendBtn.addEventListener("click", () => sendMessage());
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Create a message node (role: 'user' or 'bot')
function createMessageNode(role, textOrNode) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role}`;

  const avatar = document.createElement("img");
  avatar.className = "avatar";
  avatar.src = role === "user" ? "user.png" : "bot.png";
  avatar.alt = role;

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  // If textOrNode is a DOM node (typing indicator), append, else set text
  if (textOrNode instanceof Node) {
    bubble.appendChild(textOrNode);
  } else {
    bubble.innerText = textOrNode;
  }

  wrapper.appendChild(avatar);
  wrapper.appendChild(bubble);
  return wrapper;
}

// Scroll helper
function scrollToBottom() {
  // small timeout ensures DOM updated before scroll
  setTimeout(() => {
    chatbox.scrollTop = chatbox.scrollHeight;
  }, 20);
}

// Show typing indicator (returns the wrapper so we can remove later)
function showTypingIndicator() {
  const dots = document.createElement("div");
  dots.className = "typing-dots";
  for (let i = 0; i < 3; i++) {
    const d = document.createElement("div");
    d.className = "dot";
    dots.appendChild(d);
  }

  const typingBubble = document.createElement("div");
  typingBubble.className = "typing-bubble";
  typingBubble.appendChild(dots);

  const node = createMessageNode("bot", typingBubble);
  node.id = "typing-indicator";
  messagesEl.appendChild(node);
  scrollToBottom();
  return node;
}

function removeTypingIndicator() {
  const node = document.getElementById("typing-indicator");
  if (node) node.remove();
  scrollToBottom();
}

// Display a user message (immediate)
function displayUserMessage(text) {
  const node = createMessageNode("user", text);
  messagesEl.appendChild(node);
  scrollToBottom();
}

// Stream the bot message (typewriter) and preserve spaces
function streamBotMessage(fullText, speed = 20) {
  // Create bubble with empty text
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerText = ""; // will be filled

  const wrapper = document.createElement("div");
  wrapper.className = "message bot";

  const avatar = document.createElement("img");
  avatar.className = "avatar";
  avatar.src = "bot.png";

  wrapper.appendChild(avatar);
  wrapper.appendChild(bubble);
  messagesEl.appendChild(wrapper);
  scrollToBottom();

  let i = 0;
  // type by character but keep spaces (slice preserves spaces)
  const t = setInterval(() => {
    i++;
    bubble.innerText = fullText.slice(0, i);
    scrollToBottom();
    if (i >= fullText.length) {
      clearInterval(t);
      isSending = false;
      enableInput();
    }
  }, speed);
}

// Disable input (while request in-flight)
function disableInput() {
  userInput.disabled = true;
  sendBtn.disabled = true;
  sendBtn.style.cursor = "not-allowed";
}

// Enable input
function enableInput() {
  userInput.disabled = false;
  sendBtn.disabled = false;
  userInput.focus();
}

// Main send function
async function sendMessage() {
  if (isSending) return;          // guard against double-send
  const text = userInput.value.trim();
  if (!text) return;

  // show user message
  displayUserMessage(text);
  userInput.value = "";

  // prepare
  isSending = true;
  disableInput();

  // show typing indicator immediately
  showTypingIndicator();

  try {
    const res = await fetch(`${API_BASE}/chat/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: SESSION_ID,
        query: text,
        history: []
      }),
    });

    // remove typing before handling result (keeps UI responsive)
    removeTypingIndicator();

    if (!res.ok) {
      const errText = await res.text();
      // show error as bot message
      streamBotMessage("⚠️ Backend error: " + errText, 10);
      return;
    }

    const data = await res.json();

    // small delay to simulate typing realism (optional)
    await new Promise(r => setTimeout(r, 250));

    // stream the answer
    streamBotMessage(data.answer || "Sorry, I couldn't find an answer.", 18);

  } catch (err) {
    removeTypingIndicator();
    console.error("Fetch Error:", err);
    streamBotMessage("⚠️ Error contacting backend.", 12);
  }
}
