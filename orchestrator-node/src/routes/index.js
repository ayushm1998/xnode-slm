import { Router } from "express";
import { predict } from "../services/modelClient.js";
import { chooseAgent, initDb, logPrediction, metricsSummary } from "../services/routing.js";

const router = Router();
initDb();

router.post("/predict", async (req, res) => {
  const { text } = req.body;
  const t0 = Date.now();

  try {
    const modelOut = await predict(text);
    const agent = chooseAgent(modelOut.intent, modelOut.confidence);
    const totalMs = Date.now() - t0;

    await logPrediction({
      text,
      intent: modelOut.intent,
      confidence: modelOut.confidence,
      agentId: agent.id,
      modelMs: modelOut.model_latency_ms ?? 0,
      routingMs: totalMs - (modelOut.model_latency_ms ?? 0),
      totalMs,
    });

    return res.json({
      intent: modelOut.intent,
      confidence: modelOut.confidence,
      agent,
      response: modelOut.response,
      timings: { model_ms: modelOut.model_latency_ms ?? 0, total_ms: totalMs },
    });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ error: "prediction_failed" });
  }
});

router.get("/metrics/summary", async (_req, res) => {
  const m = await metricsSummary();
  res.json(m);
});

router.get("/agents", (_req, res) => {
  res.json([
    { id: "order-bot", intents: ["order_status"], status: "healthy" },
    { id: "complaint-bot", intents: ["complaint"], status: "healthy" },
    { id: "concierge", intents: ["*"], status: "healthy" },
  ]);
});

export default router;
