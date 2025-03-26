"use client";

import { useState } from "react";
import Image from "next/image";

export default function Home() {
  const [text, setText] = useState("");
  const [imgUrl, setImgUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!text.trim()) return;
    console.log(process.env.NEXT_PUBLIC_GENERATE_API_ENDPOINT);

    setLoading(true);
    try {
      const res = await fetch(process.env.NEXT_PUBLIC_GENERATE_API_ENDPOINT!, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: text }),
      });

      const data = await res.json();
      setImgUrl(data.presigned_url);
    } catch (err) {
      console.error("送信失敗やで💦", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 flex flex-col items-center gap-8">
      <h1 className="text-2xl font-bold">テキストから画像生成しよか！</h1>
      <div className="flex flex-col sm:flex-row gap-4 w-full max-w-xl">
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="なんか入力してや〜"
          className="flex-1 border border-gray-300 rounded px-4 py-2"
        />
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "送信中..." : "送信！"}
        </button>
      </div>

      {imgUrl && (
        <div className="mt-8">
          <Image
            src={imgUrl}
            alt="生成された画像やで"
            width={400}
            height={400}
            className="rounded shadow"
          />
        </div>
      )}
    </div>
  );
}
