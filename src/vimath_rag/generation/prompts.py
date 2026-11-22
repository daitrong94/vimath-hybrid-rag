"""Vietnamese prompt templates for grounded answers, hints and the closed-book baseline.

Draft v0: iterate on the dev split only and bump ``PROMPT_VERSION`` on every change (it is
recorded with each evaluation run).
"""

from collections.abc import Sequence
from typing import Literal

from vimath_rag.generation.llm import Message
from vimath_rag.schemas import Chunk

PROMPT_VERSION = "v0"

PromptMode = Literal["answer", "hint", "closed_book"]

SYSTEM_ANSWER = """\
Bạn là gia sư Toán THCS ở Việt Nam, đang giúp một học sinh {grade_label}.
Hãy trả lời câu hỏi CHỈ dựa trên các trích đoạn sách giáo khoa (SGK) được cung cấp.

Quy tắc:
1. Chỉ dùng kiến thức có trong các trích đoạn; không dùng kiến thức ngoài chương trình {grade_label}.
2. Giữ thuật ngữ và ký hiệu như trong SGK (ví dụ dấu phẩy thập phân: 3,5).
3. Viết công thức bằng LaTeX trong cặp dấu $...$.
4. Sau mỗi ý lấy từ một trích đoạn, ghi số thứ tự trích đoạn trong ngoặc vuông, ví dụ [1].
5. Nếu các trích đoạn không đủ để trả lời, hãy nói rõ "Các trích đoạn SGK được cung cấp chưa đủ để trả lời câu hỏi này." và không tự suy diễn thêm.
6. Trả lời ngắn gọn, rõ ràng, phù hợp với học sinh.
"""

SYSTEM_HINT = """\
Bạn là gia sư Toán THCS ở Việt Nam, đang giúp một học sinh {grade_label} tự giải bài.
Hãy đưa ra GỢI Ý, KHÔNG đưa ra đáp số hay lời giải hoàn chỉnh. Chỉ dựa trên các trích đoạn SGK được cung cấp.

Quy tắc:
1. Đưa tối đa 3 gợi ý, đi từ khái quát đến cụ thể.
2. Mỗi gợi ý nêu kiến thức cần dùng (định nghĩa, định lí, công thức) và ghi nguồn [n].
3. Không dùng kiến thức ngoài chương trình {grade_label}.
4. Nếu các trích đoạn không đủ để gợi ý, hãy nói rõ điều đó.
"""

SYSTEM_CLOSED_BOOK = """\
Bạn là gia sư Toán THCS ở Việt Nam, đang giúp một học sinh {grade_label}.
Hãy trả lời câu hỏi ngắn gọn, đúng chương trình {grade_label}. Viết công thức bằng LaTeX trong cặp dấu $...$.
"""

USER_WITH_CONTEXT = """\
Các trích đoạn SGK:
{context}

Câu hỏi: {question}
"""

USER_CLOSED_BOOK = "Câu hỏi: {question}\n"

CONTEXT_ITEM = "[{n}] ({citation})\n{text}"


def grade_label(grade: int | None) -> str:
    """``8`` -> "lớp 8"; ``None`` -> "THCS (lớp 6–9)"."""
    return f"lớp {grade}" if grade is not None else "THCS (lớp 6–9)"


def format_citation(chunk: Chunk, printed_page_offset: int | None = None) -> str:
    """Citation such as "SGK Toán 8, Tập 1, Bài 12: <lesson title>, tr. 45".

    The printed page is ``page_start - printed_page_offset``; omit the page when the offset is
    unknown. Non-lesson units use their label (e.g. "Luyện tập chung"). TODO(M4).
    """
    raise NotImplementedError("TODO(M4): format_citation")


def build_messages(
    question: str,
    chunks: Sequence[Chunk],
    *,
    grade: int | None,
    mode: PromptMode,
) -> list[Message]:
    """Fill the templates: numbered context items ``[1]..[k]`` + the question. TODO(M4)."""
    raise NotImplementedError("TODO(M4): build_messages")
