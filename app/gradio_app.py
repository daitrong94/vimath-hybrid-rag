"""Single-turn Gradio demo: question + grade + method -> answer + sources.

Run (needs the ``demo``, ``ml`` and ``llm`` extras):
    uv run python app/gradio_app.py

Keep the demo local (no ``share=True``, no public deployment): it shows textbook passages,
which are copyrighted.
"""

from vimath_rag.api import answer

GRADE_CHOICES = ["Tất cả", "6", "7", "8", "9"]
METHOD_CHOICES = ["hybrid_rerank", "hybrid", "dense", "bm25", "graph", "none"]
MODE_CHOICES = [("Giải thích", "answer"), ("Gợi ý", "hint")]


def run_query(question: str, grade: str, method: str, mode: str) -> tuple[str, str]:
    """Call :func:`vimath_rag.api.answer` and format the answer and its sources as Markdown."""
    if not question.strip():
        return "Hãy nhập câu hỏi.", ""
    student_grade = None if grade == "Tất cả" else int(grade)
    try:
        result = answer(question, grade=student_grade, method=method, mode=mode)
    except NotImplementedError as exc:
        return f"Chưa triển khai: {exc}", ""
    sources = "\n".join(f"- [{i}] {s.citation}" for i, s in enumerate(result.sources, start=1))
    return result.answer, sources


def build_demo():  # -> gradio.Blocks (gradio is imported lazily)
    """Build the Blocks UI. TODO(M5): check the layout against the installed Gradio 6 API."""
    import gradio as gr

    with gr.Blocks(title="ViMath Hybrid RAG") as demo:
        gr.Markdown("# ViMath Hybrid RAG\nHỏi đáp Toán THCS dựa trên SGK *Kết nối tri thức*.")
        question = gr.Textbox(
            label="Câu hỏi", lines=3, placeholder="Ví dụ: Định lí Pythagore phát biểu thế nào?"
        )
        with gr.Row():
            grade = gr.Dropdown(GRADE_CHOICES, value="Tất cả", label="Lớp")
            method = gr.Dropdown(
                METHOD_CHOICES, value="hybrid_rerank", label="Phương pháp truy hồi"
            )
            mode = gr.Radio(MODE_CHOICES, value="answer", label="Chế độ")
        submit = gr.Button("Hỏi", variant="primary")
        answer_box = gr.Markdown()
        gr.Markdown("### Nguồn")
        sources_box = gr.Markdown()
        submit.click(
            run_query, inputs=[question, grade, method, mode], outputs=[answer_box, sources_box]
        )
    return demo


if __name__ == "__main__":
    build_demo().launch()  # local only; never share=True (copyrighted content)
