# Đồ thị kiến thức chương trình (KG)

Chỉ chứa **cấu trúc**: tên khái niệm, tên bài/chương, quan hệ giữa chúng. Không chứa văn bản SGK.

| File | Nội dung |
|---|---|
| `schema.yaml` | Lược đồ nút/cạnh, nguồn chuẩn duy nhất (mã nguồn đọc trực tiếp file này) |
| `example_graph.json` | Đồ thị tổng hợp nhỏ minh họa định dạng (số bài, tên bài chỉ để minh họa) |
| `curated/` | *(chưa tạo)* `lessons.csv`, `concepts.csv`, `edges.csv`, hiệu đính thủ công |
| `candidates/` | *(chưa tạo)* ứng viên do LLM gợi ý (chỉ tên + `chunk_id` làm bằng chứng) |
| `graph.json` | *(chưa tạo)* đồ thị đầy đủ do `scripts/build_kg.py` xây dựng |

- Kiểm tra một đồ thị theo lược đồ: `uv run python scripts/build_kg.py --validate data/kg/example_graph.json`
- Mô tả lược đồ và quy trình xây dựng: [docs/DATA.md §6](../../docs/DATA.md#6-lược-đồ-đồ-thị-kiến-thức-kg).
