"use client";

import { useState, useRef, useEffect } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    const userMessage: Message = { role: "user", content: trimmed };
    const nextMessages = [...messages, userMessage];

    setMessages(nextMessages);
    setInput("");
    setError("");
    setLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: trimmed,
          history: nextMessages.map((m) => [m.role, m.content]),
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail ?? "Something went wrong");
      }

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.reply },
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message");
      // roll back the optimistic user message on failure
      setMessages(messages);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex rounded-md flex-col  w-[70%] mx-auto p-10 bg-gradient-main-2 shadow-2xl h-[80%]">
      <div className="flex-1 overflow-y-auto space-y-3 p">
        {messages.length === 0 && (
          <p className="text-center text-sm text-gray-400 mt-3">
            Ask about your accounts, transactions, or goals to get started.
          </p>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[75%] rounded-2xl px-4 py-2 text-sm whitespace-pre-wrap ${
                msg.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 text-gray-900"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-500 rounded-2xl px-4 py-2 text-sm">
              Thinking...
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {error && (
        <p className="px-4 pb-1 text-sm text-red-600" role="alert">
          {error}
        </p>
      )}

      <form onSubmit={handleSend} className="flex gap-2 p-4 border-t">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="e.g. Create a savings account with 5000"
          className="flex-1 rounded-xl border border-gray-200 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          Send
        </button>
      </form>
    </div>
  );
}
