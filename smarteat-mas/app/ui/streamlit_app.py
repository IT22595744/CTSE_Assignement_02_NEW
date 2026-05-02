from __future__ import annotations

import json

import streamlit as st

from app.graph.state import build_initial_state
from app.graph.workflow import build_workflow
from app.logging.tracer import get_log_path, reset_trace_file

st.set_page_config(
    page_title="SmartEat MAS",
    page_icon="🍽️",
    layout="wide",
)

# ---------------------------
# Custom Styling
# ---------------------------
st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(180deg, #f8fbff 0%, #eef6ff 100%);
        }

        .hero-box {
            padding: 1.5rem 1.5rem 1rem 1.5rem;
            border-radius: 18px;
            background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
            color: white;
            margin-bottom: 1rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        }

        .hero-title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }

        .hero-subtitle {
            font-size: 1rem;
            opacity: 0.92;
        }

        .section-card {
            background: white;
            padding: 1rem 1rem 0.8rem 1rem;
            border-radius: 16px;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
            border: 1px solid #e5e7eb;
            margin-bottom: 1rem;
        }

        .metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 1rem;
            border-radius: 14px;
            border: 1px solid #dbeafe;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
            text-align: center;
        }

        .metric-title {
            font-size: 0.95rem;
            color: #475569;
            margin-bottom: 0.4rem;
        }

        .metric-value {
            font-size: 1.2rem;
            font-weight: 700;
            color: #0f172a;
        }

        .artifact-box {
            background: #f8fafc;
            border-left: 5px solid #2563eb;
            padding: 0.9rem 1rem;
            border-radius: 10px;
            margin-bottom: 0.7rem;
        }

        .footer-note {
            font-size: 0.9rem;
            color: #64748b;
            text-align: center;
            margin-top: 1rem;
        }

        .success-banner {
            background: #ecfdf5;
            border: 1px solid #bbf7d0;
            color: #166534;
            padding: 0.9rem 1rem;
            border-radius: 12px;
            font-weight: 600;
        }

        .failure-banner {
            background: #fef2f2;
            border: 1px solid #fecaca;
            color: #991b1b;
            padding: 0.9rem 1rem;
            border-radius: 12px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

workflow = build_workflow()

# ---------------------------
# Header
# ---------------------------
st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">🍽️ SmartEat Multi-Agent Food Ordering Assistant</div>
        <div class="hero-subtitle">
            Local CTSE Assignment 2 demo using LangGraph, Ollama, custom Python tools,
            shared state management, and execution tracing.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.title("⚙️ Demo Controls")
    st.markdown("Use the sample requests below to quickly test the workflow.")

    st.markdown("### ✅ Success Cases")

    if st.button("Success 1 — Halal Sri Lankan / Malabe"):
        st.session_state["user_id_value"] = "U001"
        st.session_state["query_value"] = "Find me a halal Sri Lankan meal under 2500 in Malabe"

    if st.button("Success 2 — Vegetarian Indian / Kottawa"):
        st.session_state["user_id_value"] = "U002"
        st.session_state["query_value"] = "Find me a vegetarian Indian meal under 1800 in Kottawa"

    if st.button("Success 3 — Chinese / Nugegoda"):
        st.session_state["user_id_value"] = "U003"
        st.session_state["query_value"] = "Find me a Chinese meal under 3000 in Nugegoda"

    if st.button("Success 4 — Arabian Halal / Malabe"):
        st.session_state["user_id_value"] = "U004"
        st.session_state["query_value"] = "Find me a halal Arabian meal under 3500 in Malabe"

    st.markdown("### ❌ Failure Cases")

    if st.button("Failure 1 — Too Low Budget"):
        st.session_state["user_id_value"] = "U001"
        st.session_state["query_value"] = "Find me a halal Sri Lankan meal under 500 in Malabe"

    if st.button("Failure 2 — No Matching Cuisine + Vegetarian"):
        st.session_state["user_id_value"] = "U001"
        st.session_state["query_value"] = "Find me an Arabian vegetarian halal meal under 500 in Kottawa"

    if st.button("Failure 3 — Closed Restaurant Scenario"):
        st.session_state["user_id_value"] = "U001"
        st.session_state["query_value"] = "Find me a halal Sri Lankan meal under 1200 in Malabe from Rice Bowl Express"

    if st.button("Failure 4 — Unknown User"):
        st.session_state["user_id_value"] = "U999"
        st.session_state["query_value"] = "Find me a halal Sri Lankan meal under 2500 in Malabe"

    st.markdown("---")
    st.markdown(
        """
        **System Features**
        - 4 specialized agents
        - LangGraph orchestration
        - Local Ollama model
        - SQLite data layer
        - JSONL trace logging
        - Pytest evaluation
        """
    )

# Initialize default session state
if "user_id_value" not in st.session_state:
    st.session_state["user_id_value"] = "U001"

if "query_value" not in st.session_state:
    st.session_state["query_value"] = "Find me a halal Sri Lankan meal under 2500 in Malabe"

# ---------------------------
# Input Section
# ---------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("📝 User Request")

col_input1, col_input2 = st.columns([1, 2])

with col_input1:
    user_id = st.text_input("User ID", value=st.session_state["user_id_value"])

with col_input2:
    query = st.text_area(
        "Food Request",
        value=st.session_state["query_value"],
        height=110,
        placeholder="Enter a natural language food ordering request...",
    )

run_button = st.button("🚀 Run SmartEat MAS", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Execution
# ---------------------------
if run_button:
    if not user_id.strip() or not query.strip():
        st.error("Please enter both user_id and query.")
    else:
        with st.spinner("Running SmartEat multi-agent workflow..."):
            reset_trace_file()

            initial_state = build_initial_state(
                user_id=user_id,
                user_query=query,
            )

            final_state = workflow.invoke(initial_state)

        # ---------------------------
        # Top Summary
        # ---------------------------
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📌 Final Response")

        if final_state["errors"]:
            st.markdown(
                f'<div class="failure-banner">{final_state["final_response"] or "Workflow failed."}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="success-banner">{final_state["final_response"] or "No response generated."}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------------------
        # Metrics
        # ---------------------------
        metric1, metric2, metric3, metric4 = st.columns(4)

        with metric1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Agents Executed</div>
                    <div class="metric-value">{len(final_state["execution_trace"])}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with metric2:
            restaurant_name = (
                final_state["selected_restaurant"]["name"]
                if final_state["selected_restaurant"]
                else "None"
            )
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Selected Restaurant</div>
                    <div class="metric-value">{restaurant_name}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with metric3:
            total_value = (
                final_state["order_draft"]["total"]
                if final_state["order_draft"]
                else "N/A"
            )
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Order Total</div>
                    <div class="metric-value">{total_value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with metric4:
            error_count = len(final_state["errors"])
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Errors</div>
                    <div class="metric-value">{error_count}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")

        # ---------------------------
        # Main Result Columns
        # ---------------------------
        left_col, right_col = st.columns(2)

        with left_col:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("🍴 Selected Restaurant")
            if final_state["selected_restaurant"]:
                st.json(final_state["selected_restaurant"])
            else:
                st.warning("No restaurant selected.")
            st.markdown("</div>", unsafe_allow_html=True)

        with right_col:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("🧾 Order Draft")
            if final_state["order_draft"]:
                st.json(final_state["order_draft"])
            else:
                st.warning("No order draft created.")
            st.markdown("</div>", unsafe_allow_html=True)

        # ---------------------------
        # Errors
        # ---------------------------
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("⚠️ Errors")
        if final_state["errors"]:
            for error in final_state["errors"]:
                st.error(error)
        else:
            st.info("No errors.")
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------------------
        # Artifacts
        # ---------------------------
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📁 Generated Artifacts")
        st.markdown(
            f"""
            <div class="artifact-box"><strong>Trace Log Path:</strong><br><code>{get_log_path()}</code></div>
            <div class="artifact-box"><strong>Summary File Path:</strong><br><code>{final_state["summary_file_path"]}</code></div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------------------
        # Execution Trace
        # ---------------------------
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🔍 Execution Trace")
        for index, entry in enumerate(final_state["execution_trace"], start=1):
            with st.expander(f"Step {index} — {entry['agent']} | {entry['step']}"):
                st.json(entry)
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------------------
        # Raw Final State
        # ---------------------------
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🧠 Raw Final State")
        st.code(json.dumps(final_state, indent=2, ensure_ascii=False), language="json")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Footer
# ---------------------------
st.markdown(
    """
    <div class="footer-note">
        SmartEat MAS • CTSE Assignment 2 • LangGraph + Ollama + SQLite + FastAPI + Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)