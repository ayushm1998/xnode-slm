const MODEL_URL = process.env.MODEL_URL || "http://localhost:5000";

export async function predict(text) {
  const r = await fetch(`${MODEL_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, generate_options: { max_new_tokens: 40, temperature: 0.7 } }),
  });
  if (!r.ok) throw new Error(`Model service error: ${r.status}`);
  return r.json();
}
