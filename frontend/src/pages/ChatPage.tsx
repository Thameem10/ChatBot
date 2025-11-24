import { useState, useEffect, useRef } from "react";
import { Send } from "lucide-react";

export default function ChatPage() {
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem("chat_messages");
    return saved
      ? JSON.parse(saved)
      : [{ sender: "bot", text: "Hi! How can I help you today?" }];
  });

  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const API_URL = import.meta.env.VITE_API_URL;

  // Auto scroll bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, typing]);

  // Save messages whenever updated
  useEffect(() => {
    localStorage.setItem("chat_messages", JSON.stringify(messages));
  }, [messages]);

  const threadId = localStorage.getItem("thread_id") || crypto.randomUUID();

  useEffect(() => {
    localStorage.setItem("thread_id", threadId);
  }, []);
  const botIndexRef = useRef<number>(-1);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev: any) => [...prev, userMessage]);

    setInput("");
    setTyping(true);

    setMessages((prev: any) => {
      botIndexRef.current = prev.length;
      return [...prev, { sender: "bot", text: "" }];
    });

    try {
      const res = await fetch(`${API_URL}/chat/send`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input, thread_id: threadId })
      });

      const reader = res.body!.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);

        setMessages((prev: any) => {
          const updated = [...prev];
          updated[botIndexRef.current].text += chunk;
          return updated;
        });
      }
    } catch (err) {
      console.error(err);
    }

    setTyping(false);
  };

  const clearChat = () => {
    localStorage.removeItem("chat_messages");
    localStorage.removeItem("thread_id");
    setMessages([{ sender: "bot", text: "New chat started!" }]);
  };

  return (
    <div className="flex flex-col h-[90vh] bg-white ">
      {/* Header */}
      <div className="px-6 py-4  bg-amber-50 flex justify-between items-center gap-3">
        <div className="flex gap-3">
          <div className="w-10 h-10 bg-amber-200 rounded-full flex items-center justify-center font-bold">
            🤖
          </div>
          <div>
            <h2 className="text-lg font-semibold text-amber-900">
              AI Assistant
            </h2>
            <p className="text-sm text-gray-600">Ask anything...</p>
          </div>
        </div>
        <div>
          <button
            className="border border-solid border-black text-amber-900 text-lg font-semibold p-2 rounded-xl"
            onClick={clearChat}
          >
            clear chat
          </button>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 p-6 overflow-y-auto space-y-4">
        {messages.map((msg: any, idx: any) => (
          <div
            key={idx}
            className={`flex ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-md px-4 py-2 rounded-xl text-sm shadow-sm ${
                msg.sender === "user"
                  ? "bg-amber-600 text-white rounded-br-none"
                  : "bg-gray-100 text-gray-800 rounded-bl-none"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {typing && (
          <div className="flex items-center gap-2 text-gray-500 text-sm">
            <span className="animate-pulse">Bot is typing...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t p-4 bg-white">
        <div className="flex items-center gap-3">
          <input
            type="text"
            className="flex-1 px-4 py-2 border rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-400"
            placeholder="Type your message…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />

          <button
            onClick={handleSend}
            className="p-3 bg-amber-600 hover:bg-amber-700 transition rounded-xl text-white shadow"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
