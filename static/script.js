const input = document.getElementById("message");
const chatBox = document.getElementById("chat-box");

function addMessage(msg, sender) {
    const div = document.createElement("div");
    div.className = "message " + sender;
    div.textContent = msg;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const msg = input.value.trim();
    if (!msg) return;

    addMessage("You: " + msg, "user");
    input.value = "";

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        });

        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();
        addMessage("StudyBot: " + data.response, "bot");
    } catch (error) {
        addMessage("StudyBot: Sorry, I couldn't process your request.", "bot");
        console.error("Fetch error:", error);
    }
}

// Press Enter to send
input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});
