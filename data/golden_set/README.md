# Golden set

Câu hỏi đánh giá kèm mã chunk đúng. **Chỉ chứa câu hỏi tự viết và id, không chứa văn bản SGK.**

| File | Nội dung |
|---|---|
| `examples.jsonl` | 3 câu tổng hợp minh họa định dạng (id chunk chỉ để minh họa, chưa đối chiếu corpus) |
| `schema.json` | JSON Schema sinh tự động từ `GoldItem` trong `src/vimath_rag/schemas.py` |
| `golden_v1.jsonl` | *(chưa tạo)* 160 câu: 4 lớp × 4 loại × 10 câu; 32 `dev` / 128 `test` |

- Sau khi sửa `GoldItem`, sinh lại schema: `uv run python scripts/export_schemas.py` (có test kiểm tra hai bên khớp nhau).
- Hướng dẫn gán nhãn và định nghĩa loại câu hỏi: [docs/DATA.md §5](../../docs/DATA.md#5-golden-set).
- Kiểm tra định dạng: `uv run python scripts/run_eval.py --golden data/golden_set/examples.jsonl --split all`.
