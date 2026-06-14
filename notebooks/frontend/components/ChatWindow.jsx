import { useState } from "react";
import { apiPost } from "../api/client";

export default function ChatWindow() {
  const response = await apiPost(`/tutor/student_001/A`, { text: input });
  
  const botMsg = {
  sender: "agent",
  text: response.agent_reply
};

  async function sendMessage() {
    const userMsg = { sender: "user", text: input };
    setMessages([...messages, userMsg]);

    const response = await apiPost("/affective/classify", { text: input });

    const botMsg = {
      sender: "agent",
      text: `Estado detectado: ${response.affective_state}`
    };

    setMessages([...messages, userMsg, botMsg]);
    setInput("");
  }

  return (
    <div style={{ border: "1px solid #ccc", padding: 20 }}>
      <h3>Chat Educativo</h3>

      <div style={{ height: 200, overflowY: "scroll", marginBottom: 10 }}>
        {messages.map((m, i) => (
          <div key={i}>
            <strong>{m.sender}:</strong> {m.text}
          </div>
        ))}
      </div>

      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={{ width: "80%" }}
      />
      <button onClick={sendMessage}>Enviar</button>
    </div>
  );
}
