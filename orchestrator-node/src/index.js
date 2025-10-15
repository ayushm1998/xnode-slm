import express from "express";
import cors from "cors";
import morgan from "morgan";
import routes from "./routes/index.js";

const app = express();
app.use(cors({ origin: ["http://localhost:4200"] }));
app.use(express.json());
app.use(morgan("dev"));

app.use("/api", routes);

app.get("/healthz", (_req, res) => res.json({ ok: true }));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Orchestrator on :${PORT}`));
