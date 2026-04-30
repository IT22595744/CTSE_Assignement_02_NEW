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

st.title("🍽️ SmartEat Multi-Agent Food Ordering Assistant")
st.write("Local CTSE Assignment 2 demo using LangGraph + Ollama + FastAPI-style workflow.")

workflow = build_workflow()

with st.sidebar:
    st.header("Quick Test Requests")
    st.markdown(
        """
**Success case**
- Find me a halal Sri Lankan meal under 2500 in Malabe

**Failure case**
- Find me an Arabian vegetarian halal meal under 500 in Kottawa
        """
    )

user_id = st.text_input("User ID", value="U001")
query = st.text_area(
    "Food Request",
    value="Find me a halal Sri Lankan meal under 2500 in Malabe",
    height=120,
)

run_button = st.button("Run SmartEat MAS")

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

        st.subheader("Final Response")
        st.success(final_state["final_response"] or "No response generated.")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Selected Restaurant")
            if final_state["selected_restaurant"]:
                st.json(final_state["selected_restaurant"])
            else:
                st.warning("No restaurant selected.")

        with col2:
            st.subheader("Order Draft")
            if final_state["order_draft"]:
                st.json(final_state["order_draft"])
            else:
                st.warning("No order draft created.")

        st.subheader("Errors")
        if final_state["errors"]:
            st.error("\n".join(final_state["errors"]))
        else:
            st.info("No errors.")

        st.subheader("Execution Trace")
        for index, entry in enumerate(final_state["execution_trace"], start=1):
            with st.expander(f"Step {index} - {entry['agent']} / {entry['step']}"):
                st.json(entry)

        st.subheader("Artifacts")
        st.write(f"**Trace Log Path:** `{get_log_path()}`")
        st.write(f"**Summary File Path:** `{final_state['summary_file_path']}`")

        st.subheader("Raw Final State")
        st.code(json.dumps(final_state, indent=2, ensure_ascii=False), language="json")