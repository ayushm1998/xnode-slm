import dash
from dash import html, dcc
import pandas as pd
import requests
import plotly.graph_objects as go

app = dash.Dash(__name__)

def fetch_metrics():
    try:
        r = requests.get("http://127.0.0.1:5000/metrics", timeout=2)
        return r.json()
    except Exception:
        return {
            "accuracy_by_intent": {},
            "agent_latency_ms": {},
            "workflow_efficiency": 0,
            "total_predictions": 0
        }

app.layout = html.Div([
    html.H1("Agent Routing & Communication Dashboard", style={"textAlign": "center"}),

    html.Div(id="metrics-container"),

    dcc.Interval(
        id="refresh-interval",
        interval=5000,  # every 5s
        n_intervals=0
    )
])

@app.callback(
    dash.Output("metrics-container", "children"),
    dash.Input("refresh-interval", "n_intervals")
)
def update_dashboard(n):
    data = fetch_metrics()
    if not data["accuracy_by_intent"]:
        return html.Div("⚠️ No metrics yet. Try sending a few intents via the UI.")

    # Convert data for charts
    acc_df = pd.DataFrame(list(data["accuracy_by_intent"].items()), columns=["Intent", "Accuracy"])
    latency_df = pd.DataFrame(list(data["agent_latency_ms"].items()), columns=["Agent", "Latency (ms)"])

    # Accuracy bar chart
    accuracy_fig = go.Figure([
        go.Bar(x=acc_df["Intent"], y=acc_df["Accuracy"], marker_color="teal")
    ])
    accuracy_fig.update_layout(title="Intent Classification Accuracy", yaxis_title="Confidence")

    # Latency chart
    latency_fig = go.Figure([
        go.Bar(x=latency_df["Agent"], y=latency_df["Latency (ms)"], marker_color="orange")
    ])
    latency_fig.update_layout(title="Average Agent Response Time", yaxis_title="ms")

    # Efficiency gauge
    eff_value = data["workflow_efficiency"] * 100
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=eff_value,
        title={'text': "Workflow Efficiency (%)"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "green"}}
    ))

    return html.Div([
        html.Div([
            html.H3(f"Total Predictions: {data['total_predictions']}"),
        ], style={"marginBottom": "2rem"}),

        html.Div([
            dcc.Graph(figure=accuracy_fig),
            dcc.Graph(figure=latency_fig),
            dcc.Graph(figure=gauge),
        ])
    ])

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
