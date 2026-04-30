from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.graph.state import build_initial_state
from app.graph.workflow import build_workflow
from app.logging.tracer import get_log_path, reset_trace_file

app = FastAPI(
    title="SmartEat MAS API",
    version="1.0.0",
    description="Local Multi-Agent SmartEat food ordering assistant",
)

workflow = build_workflow()


class OrderRequest(BaseModel):
    user_id: str = Field(..., min_length=1, description="User identifier")
    query: str = Field(..., min_length=1, description="Natural language food request")


class OrderResponse(BaseModel):
    final_response: str | None
    selected_restaurant: dict[str, Any] | None
    order_draft: dict[str, Any] | None
    errors: list[str]
    execution_trace: list[dict[str, Any]]
    trace_log_path: str
    summary_file_path: str | None

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "SmartEat MAS API is running"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/process-order-request", response_model=OrderResponse)
def process_order_request(request: OrderRequest) -> OrderResponse:
    reset_trace_file()

    initial_state = build_initial_state(
        user_id=request.user_id,
        user_query=request.query,
    )

    final_state = workflow.invoke(initial_state)

    return OrderResponse(
        final_response=final_state["final_response"],
        selected_restaurant=final_state["selected_restaurant"],
        order_draft=final_state["order_draft"],
        errors=final_state["errors"],
        execution_trace=final_state["execution_trace"],
        trace_log_path=get_log_path(),
        summary_file_path=final_state["summary_file_path"],
    )