#!/bin/bash

# -------------------------------------
# 🚀 XNode SLM - Full Stack Runner
# -------------------------------------

set -e  # Exit immediately on error
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}============================================"
echo -e "     🚀 Starting XNode Smart Language Model"
echo -e "============================================${NC}"

# --- FASTAPI BACKEND ---
echo -e "${GREEN}🔹 Activating Python virtual environment...${NC}"
cd model-python
if [ ! -d ".venv" ]; then
  echo -e "${CYAN}Creating virtual environment...${NC}"
  python3 -m venv .venv
fi
source .venv/bin/activate

echo -e "${GREEN}🔹 Installing backend dependencies...${NC}"
pip install -q fastapi uvicorn torch transformers datasets scikit-learn dash plotly pandas requests

echo -e "${GREEN}Starting FastAPI backend on port 5000...${NC}"
uvicorn src.server:app --port 5000 --reload > ../fastapi.log 2>&1 &
FASTAPI_PID=$!
sleep 5

cd ..

# --- NODE.JS SERVER ---
echo -e "${GREEN}Starting Node.js middleware on port 3000...${NC}"
cd orchestrator-node
npm install --silent
node server.js > ../node.log 2>&1 &
NODE_PID=$!
sleep 3

cd ..

# --- ANGULAR FRONTEND ---
echo -e "${GREEN}Starting Angular frontend on port 4200...${NC}"
cd ui-angular
npm install --silent
npm start > ../angular.log 2>&1 &
ANGULAR_PID=$!
sleep 6

cd ..

# --- DASH DASHBOARD ---
echo -e "${GREEN}Starting Dash visualization dashboard on port 8050...${NC}"
cd dashboard

# Ensure Python venv is active
source ../model-python/.venv/bin/activate

# Detect Dash version
DASH_VERSION=$(python3 -c "import dash; print(dash.__version__.split('.')[0])" 2>/dev/null || echo 0)
if [ "$DASH_VERSION" -ge 3 ]; then
  echo -e "${CYAN}Detected Dash v3+, using app.run()...${NC}"
  python3 -c "import re,sys; f=open('app.py').read(); f=re.sub(r'app\.run_server', 'app.run', f); open('app.py','w').write(f)"
fi

python3 app.py > ../dash.log 2>&1 &
DASH_PID=$!
sleep 4

cd ..

# --- OPEN ALL SERVICES ---
echo -e "${CYAN}🌐 Opening all services in browser...${NC}"
open http://127.0.0.1:5000
open http://localhost:3000
open http://localhost:4200
open http://localhost:8050

echo ""
echo -e "${GREEN}All services are running:${NC}"
echo "----------------------------------------"
echo "FastAPI Backend      → http://127.0.0.1:5000"
echo "Node.js Middleware   → http://localhost:3000"
echo "Angular Frontend     → http://localhost:4200"
echo "Dash Dashboard       → http://localhost:8050"
echo "----------------------------------------"
echo -e "${CYAN}Press [CTRL+C] to stop all processes.${NC}"

trap "echo -e '\nStopping all services...'; kill $FASTAPI_PID $NODE_PID $ANGULAR_PID $DASH_PID" SIGINT
wait
