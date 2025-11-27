import { useState, useEffect, useRef } from "react";
import { Send } from "lucide-react";

interface Message {
  sender: "user" | "bot";
  text: string;
}

interface Thread {
  id: string;
  title: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [threads, setThreads] = useState<Thread[]>([]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const [threadId, setThreadId] = useState<string>(
    localStorage.getItem("thread_id") || crypto.randomUUID()
  );
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const API_URL = import.meta.env.VITE_API_URL;

  // Save new threadId if newly created
  useEffect(() => {
    localStorage.setItem("thread_id", threadId);
  }, [threadId]);

  // Load chat history
  const loadHistory = async (id: string) => {
    try {
      const res = await fetch(
        `${API_URL}/chat/history/${id}?limit=50&offset=0`
      );
      if (!res.ok) throw new Error("Backend error");

      const data = await res.json();
      setMessages(data);
      setThreadId(id);
      localStorage.setItem("chat_messages", JSON.stringify(data));
      localStorage.setItem("thread_id", id);
    } catch (err) {
      console.warn("Using local fallback");
      const local = localStorage.getItem("chat_messages");
      setMessages(
        local
          ? JSON.parse(local)
          : [{ sender: "bot", text: "Hi! How can I help you today?" }]
      );
    }
  };

  // Load previous threads
  const loadThreads = async () => {
    try {
      const res = await fetch(`${API_URL}/chat/threads`);
      if (!res.ok) throw new Error("Backend error");
      const data = await res.json();
      setThreads(data);
    } catch (err) {
      console.warn("Could not load threads", err);
    }
  };

  useEffect(() => {
    loadThreads();
    loadHistory(threadId);
  }, []);

  // Auto scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, typing]);

  const botIndexRef = useRef<number>(-1);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    setInput("");
    setTyping(true);

    setMessages((prev) => {
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

      let botText = ""; // Temporary buffer

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        botText += chunk;

        setMessages((prev) => {
          const updated = [...prev];
          updated[botIndexRef.current] = {
            ...updated[botIndexRef.current],
            text: botText
          };
          return updated;
        });
      }
    } catch (err) {
      console.error(err);
    }

    setTyping(false);
    loadThreads(); // Refresh thread list after sending
  };

  function limitWords(text: any, limit = 5) {
    if (!text) return "";
    const words = text.split(" ");
    return words.length > limit
      ? words.slice(0, limit).join(" ") + "..."
      : text;
  }

  const clearChat = () => {
    localStorage.removeItem("chat_messages");
    localStorage.removeItem("thread_id");
    setMessages([{ sender: "bot", text: "New chat started!" }]);
    const newId = crypto.randomUUID();
    setThreadId(newId);
  };

  return (
    <div className="flex h-[90vh] bg-white">
      {/* Sidebar with threads */}
      <div className="w-64 border-r p-4 overflow-y-auto">
        <h3 className="font-bold mb-2">Previous Chats</h3>
        <button
          className="w-full mb-2 p-2 bg-amber-100 rounded"
          onClick={clearChat}
        >
          New Chat
        </button>
        {threads.map((thread) => (
          <div
            key={thread.id ?? crypto.randomUUID()}
            className={`p-2 mb-1 rounded cursor-pointer ${
              thread.id === threadId
                ? "bg-amber-300 font-bold"
                : "hover:bg-gray-200"
            }`}
            onClick={() => thread.id && loadHistory(thread.id)}
          >
            {limitWords(thread.title, 5) ?? thread.id?.slice(0, 6) ?? "Unknown"}
            ...
          </div>
        ))}
      </div>

      {/* Chat area */}
      <div className="flex-1 flex flex-col">
        {/* HEADER */}
        <div className="px-6 py-4 bg-amber-50 flex justify-between items-center gap-3">
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
        </div>

        {/* MESSAGES */}
        <div className="flex-1 p-6 overflow-y-auto space-y-4">
          {messages.map((msg, idx) => (
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
            <div className="text-sm text-gray-500 animate-pulse">
              Bot is typing...
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* INPUT */}
        <div className="border-t p-4">
          <div className="flex items-center gap-3">
            <input
              className="flex-1 px-4 py-2 border rounded-xl"
              placeholder="Type your message…"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
            />
            <button
              className="p-3 bg-amber-600 text-white rounded-xl"
              onClick={handleSend}
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
