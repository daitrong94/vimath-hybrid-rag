# Dữ liệu

> Mô tả nguồn dữ liệu, chính sách bản quyền, quy trình xử lý, lược đồ chunk, golden set và đồ thị kiến thức.
> Các thống kê (số trang, số chunk, …) chỉ được ghi sau khi chạy pipeline; hiện tại là `TBD`.

## 1. Nguồn dữ liệu

### 1.1 Sách giáo khoa (corpus chính)

Bộ *Kết nối tri thức với cuộc sống* (NXB Giáo dục Việt Nam), Toán 6–9, mỗi lớp 2 tập, được chọn vì là bộ SGK thống nhất trên toàn quốc. Nguồn: Hành trang số (taphuan.nxbgd.vn). Người thực hiện tự tải và đặt file vào `data/raw/` **đúng tên** dưới đây (khai báo trong `configs/corpus.yaml: books`).

| `book_id` | Sách | File trong `data/raw/` | Trạng thái | `printed_page_offset` |
|---|---|---|---|---|
| `g6v1` | Toán 6 – Tập 1 | `toan6_tap1.pdf` | đã tải 24/11: toàn ảnh (không có lớp chữ), 126 trang, 1094×1536 px | 1 |
| `g6v2` | Toán 6 – Tập 2 | `toan6_tap2.pdf` | chưa tải | `TBD` |
| `g7v1` | Toán 7 – Tập 1 | `toan7_tap1.pdf` | chưa tải | `TBD` |
| `g7v2` | Toán 7 – Tập 2 | `toan7_tap2.pdf` | chưa tải | `TBD` |
| `g8v1` | Toán 8 – Tập 1 | `toan8_tap1.pdf` | chưa tải | `TBD` |
| `g8v2` | Toán 8 – Tập 2 | `toan8_tap2.pdf` | chưa tải | `TBD` |
| `g9v1` | Toán 9 – Tập 1 | `toan9_tap1.pdf` | chưa tải | `TBD` |
| `g9v2` | Toán 9 – Tập 2 | `toan9_tap2.pdf` | chưa tải | `TBD` |

- Pipeline xử lý được cả PDF có lớp văn bản lẫn PDF ảnh (mục 3).
- `printed_page_offset` = số trang PDF − số trang in trong sách, dùng để trích dẫn đúng số trang. Xác định khi có PDF.

**Kết quả kiểm tra `g6v1` (24/11/2026):**

- File được ghép từ ảnh chụp từng trang (metadata: `pdf-lib`); mỗi trang là một ảnh 1094×1536 px nén không mất dữ liệu (ước tính khoảng 146 DPI với khổ sách rộng 19 cm), **không có lớp văn bản** nên phải OCR toàn bộ. Ảnh nét, dấu tiếng Việt rõ.
- Trang 1 là bìa, trang 2 là trang lót, trang 126 là bìa sau; số trang in liền mạch ở các trang lấy mẫu (PDF 3 → trang 2, …, PDF 124 → trang 123), nên `printed_page_offset = 1`.
- Mọi trang có watermark mờ "KẾT NỐI TRI THỨC / VỚI CUỘC SỐNG" ở giữa, cần lọc sau OCR (`normalize.strip_patterns`).
- Số bài nằm trong huy hiệu tròn "BÀI 8", không phải dòng tiêu đề; một số nhãn chỉ là biểu tượng (dấu "?" cho câu hỏi) nên OCR sẽ mất nhãn.
- Mỗi bài mở đầu bằng khung **"KHÁI NIỆM, THUẬT NGỮ"** liệt kê khái niệm của bài (ví dụ Bài 8: Chia hết, Ước, Bội), dùng để khởi tạo đồ thị kiến thức (mục 6.4).

### 1.2 Chương trình GDPT 2018 môn Toán (khởi tạo đồ thị kiến thức)

- Ban hành kèm Thông tư 32/2018/TT-BGDĐT. Phần nội dung và "yêu cầu cần đạt" của từng lớp cho biết khái niệm nào thuộc lớp nào, dùng để khởi tạo nút khái niệm và thuộc tính `grade_introduced`.
- Văn bản quy phạm pháp luật không thuộc đối tượng bảo hộ quyền tác giả (Luật Sở hữu trí tuệ, Điều 15), nên danh sách khái niệm rút ra từ đó có thể commit. *(Ghi chú để tham khảo, không phải tư vấn pháp lý.)*
- Trạng thái: `TBD` (chưa tải).

### 1.3 Câu hỏi đánh giá

- **Golden set tự xây dựng** (160 câu), xem mục 5.
- **DHMATH (Hugging Face, tùy chọn):** lọc các bài phần THCS để bổ sung câu hỏi dạng vận dụng. `TBD`: mã dataset chính xác, giấy phép, cách lọc. Chỉ dùng nếu giấy phép cho phép; ghi `source: "dhmath"`.

## 2. Chính sách bản quyền

Nội dung SGK thuộc bản quyền của nhà xuất bản và tác giả. Repo này **không phân phối** nội dung SGK dưới bất kỳ hình thức nào.

| Được commit ✅ | Không được commit ❌ |
|---|---|
| Mã nguồn, cấu hình, test | PDF SGK (`data/raw/`) |
| Câu hỏi golden set (tự viết) + `chunk_id` | Markdown/OCR và chunk (`data/processed/`) |
| Cấu trúc đồ thị kiến thức: tên khái niệm, tên bài, quan hệ | Chỉ mục BM25/FAISS (sinh từ văn bản SGK) |
| Ví dụ tổng hợp (synthetic) | Kết quả từng câu có văn bản truy hồi/câu trả lời (`results/runs/`) |
| Bảng và biểu đồ số liệu tổng hợp | Output notebook chứa văn bản SGK |

**Cơ chế bảo vệ** (nhiều lớp):

1. `.gitignore` loại `data/raw/`, `data/processed/`, `results/runs/` và mọi file `*.pdf` (trừ trong `docs/`).
2. Hook pre-commit `forbid-textbook-data` và `forbid-pdf` chặn các file này, kể cả khi bị `git add -f`.
3. Hook `nbstripout` xóa output notebook trước khi commit.
4. CI kiểm tra lại không có file nào trong các thư mục trên được git theo dõi.

**Quy tắc bổ sung:**

- Câu hỏi golden set phải **tự viết bằng lời của mình**, không chép nguyên văn câu chữ hay bài tập trong SGK.
- Ứng viên KG do LLM gợi ý chỉ lưu tên khái niệm và `chunk_id` làm bằng chứng, không lưu trích dẫn văn bản.
- Demo Gradio chỉ chạy cục bộ (không `share=True`, không triển khai công khai) vì hiển thị đoạn trích SGK.
- Khi gửi đoạn trích SGK làm ngữ cảnh cho API LLM: điều khoản của một số gói miễn phí (ví dụ free tier của Gemini API) cho phép nhà cung cấp dùng dữ liệu gửi lên để cải thiện sản phẩm. Đọc điều khoản hiện hành trước khi chạy và hạn chế lượng văn bản gửi lên ở free tier.
- Báo cáo và slide chỉ trích ngắn (một định nghĩa, một công thức) để minh họa, có ghi nguồn.

## 3. Quy trình xử lý

```
data/raw/{file}.pdf
  └─ probe ─────► data/processed/probe/{book_id}.json
  └─ convert ───► data/processed/md/{book_id}.md (+ {book_id}.manifest.json)
       └─ normalize + chunk ─► data/processed/chunks/chunks.jsonl (+ chunks.meta.json)
```

### 3.1 Probe (laptop)

`uv run python scripts/build_corpus.py --stage probe` ghi thống kê cho từng trang:

| Trường | Ý nghĩa |
|---|---|
| `page` | Số trang PDF (bắt đầu từ 1) |
| `n_chars` | Số ký tự trong lớp văn bản |
| `valid_syllable_ratio` | Tỉ lệ token là âm tiết tiếng Việt hợp lệ (phát hiện lỗi font TCVN3/VNI) |
| `image_area_ratio` | Tỉ lệ diện tích trang bị ảnh che phủ |
| `verdict` | `text` / `garbled` / `scanned` |

Ngưỡng ban đầu trong `configs/corpus.yaml: probe` chỉ là phỏng đoán, cần hiệu chỉnh trên PDF thật.

### 3.2 Convert (Colab T4)

- Ngay cả với PDF có lớp văn bản, công thức thường bị vỡ (ký tự rời, font ký hiệu), nên mặc định OCR mọi trang bằng Marker hoặc MinerU; lớp văn bản (nếu tốt) dùng để đối chiếu dấu tiếng Việt. `g6v1` không có lớp văn bản nên bắt buộc OCR.
- **Công cụ trên Colab T4** (theo README marker-pdf 2.2.0 và mineru 4.2.3, đọc ngày 24/11/2026):
  - Marker: chế độ GPU (`balanced`, `vllm`) chạy VLM qua vLLM trong Docker, Colab không hỗ trợ, nên dùng `--mode fast` (OCR bằng ONNX) kèm `--force_ocr`. Có thể thử `balanced` sau nếu tự dựng server suy luận (`SURYA_INFERENCE_URL`).
  - MinerU: lệnh độc lập `mineru-kit parse <pdf> -o <md> --tier basic|standard`. Colab miễn phí (khoảng 12 GB RAM) hợp với `basic`; `standard` khuyến nghị ≥ 16 GB RAM. Tắt telemetry bằng `MINERU_TELEMETRY_DISABLED=1`.
  - **Không dùng** `marker --use_llm` hay `mineru --remote`: cả hai gửi trang SGK tới dịch vụ bên thứ ba.
- **Thử nghiệm OCR (tuần 1):** `scripts/ocr_spike.py` + `notebooks/colab_ocr_spike.ipynb`, 11 trang mẫu của `g6v1` (danh sách trong `configs/corpus.yaml: ocr_spike`), ở ảnh gốc và ảnh phóng 2×. Tiêu chí chấm tay (0–2) trong `scores.csv`: (1) đúng dấu tiếng Việt, (2) đúng LaTeX, (3) giữ cấu trúc Chương/Bài/mục, (4) bảng; kèm thời gian mỗi trang và các chỉ số tự động trong `summary.json` (tỉ lệ chữ có dấu, số công thức, số lần còn watermark). Khi có Toán 8 hoặc 9 cần thử thêm vài trang nhiều công thức. Kết quả chọn `ocr.backend`: `TBD`.
- Đầu ra: `data/processed/md/{book_id}.md` có mốc `<!-- page: N -->`, kèm `{book_id}.manifest.json` (công cụ, phiên bản, lệnh chạy, thời gian).
- Giấy phép (theo PyPI và README, kiểm tra 22–24/11/2026): mã nguồn `marker-pdf` 2.x là Apache-2.0, trọng số mô hình dùng giấy phép AI Pubs Open Rail-M sửa đổi (miễn phí cho nghiên cứu và mục đích cá nhân); `mineru` 4.x dùng giấy phép riêng (MinerU Open Source License). Không dùng PyMuPDF trong package (AGPL-3.0); dùng pypdfium2.

### 3.3 Normalize

- Unicode NFC; bỏ ký tự vô hình (zero-width space, soft hyphen).
- Thống nhất kiểu đặt dấu thanh (ví dụ `hoà` / `hòa`) trong **khóa tìm kiếm**; văn bản hiển thị giữ nguyên.
- Biến thể i/y (`lí`/`lý`, `kĩ`/`kỹ`): chỉ gộp trong khóa tìm kiếm (ablation A2).
- LaTeX: `\dfrac`, `\tfrac` → `\frac`; bỏ `\left`/`\right`; chuẩn hóa khoảng trắng.
- Giữ dấu phẩy thập phân (`3,5`), không đổi sang dấu chấm.
- Bỏ header, footer, số trang lặp lại (mẫu regex trong config, xác định khi có PDF).

### 3.4 Chunk

- Phân cấp: Chương → đơn vị (Bài, hoặc đơn vị không phải bài: Luyện tập chung, Bài tập cuối chương, Hoạt động thực hành trải nghiệm) → mục → khối.
- Mỗi khối có kiểu là một chunk: định nghĩa, định lí/tính chất, công thức, ví dụ (kèm lời giải), bài tập. Phần giải thích dài được tách theo đoạn (`max_chars`); khối quá ngắn (`min_chars`) được gộp vào khối trước trong cùng đơn vị.
- Không tách giữa công thức hiển thị (`$$...$$`), không tách ví dụ khỏi lời giải.
- Dấu hiệu nhận dạng (cần xác nhận trên PDF thật): tiêu đề "CHƯƠNG …", "Bài …"; khung "Định nghĩa", "Định lí", "Tính chất"; "Ví dụ …", "Luyện tập …", "Vận dụng", "HĐ…", "Bài tập"; số bài tập dạng `2.15`.
- Đầu ra: `data/processed/chunks/chunks.jsonl` và `chunks.meta.json` (`corpus_version`, hash cấu hình, thống kê; thống kê chỉ ghi khi đã chạy).

## 4. Lược đồ chunk

Nguồn chuẩn: lớp `Chunk` trong [`src/vimath_rag/schemas.py`](../src/vimath_rag/schemas.py).

| Trường | Kiểu | Mô tả |
|---|---|---|
| `chunk_id` | str | `g{grade}-{unit}-{type}-{nn}`, xem mục 4.1 |
| `grade` | int (6–9) | Lớp |
| `volume` | int (1–2) | Tập |
| `unit_id` | str | Đơn vị bài học, ví dụ `g8-b12`; trùng id nút bài học trong KG |
| `chapter`, `chapter_title` | int?, str? | Số chương (chữ số Ả Rập) và tên chương |
| `lesson`, `lesson_title` | int?, str? | Số bài và tên bài (`null` với đơn vị không phải bài) |
| `section` | str? | Tiêu đề mục trong bài |
| `type` | enum | `definition` · `theorem` · `formula` · `example` · `exercise` · `explanation` · `other` |
| `label` | str? | Nhãn hiển thị, ví dụ "Ví dụ 2", "Bài 2.15" |
| `text` | str | Markdown + LaTeX (`$...$`). **Có bản quyền, không commit** |
| `page_start`, `page_end` | int | Trang PDF (bắt đầu từ 1) |
| `concepts` | list[str] | Id khái niệm KG liên kết với chunk |
| `extraction` | `text_layer` \| `ocr` | Cách lấy văn bản (phục vụ phân tích lỗi) |
| `source_file` | str | Ví dụ `toan8_tap1.pdf` |
| `corpus_version` | str | Phiên bản corpus, tăng khi quy tắc chunk thay đổi |

Hai loại `explanation` (văn bản giải thích, hoạt động HĐ, nhận xét) và `other` được thêm vào năm loại của đề bài để khối nào cũng có loại.

Ví dụ (giá trị minh họa, văn bản tổng hợp, không trích SGK):

```json
{
  "chunk_id": "g6-b10-definition-01",
  "grade": 6, "volume": 1, "unit_id": "g6-b10",
  "chapter": 2, "chapter_title": "(minh họa)",
  "lesson": 10, "lesson_title": "(minh họa)",
  "section": "(minh họa)",
  "type": "definition", "label": null,
  "text": "(văn bản tổng hợp) Số nguyên tố là số tự nhiên lớn hơn 1 chỉ có hai ước là 1 và chính nó.",
  "page_start": 38, "page_end": 38,
  "concepts": ["so-nguyen-to"],
  "extraction": "ocr", "source_file": "toan6_tap1.pdf", "corpus_version": "v1"
}
```

### 4.1 Quy ước `unit_id` và `chunk_id`

`unit_id = g{grade}-{unit}`, trong đó `unit` là (bảng mã sẽ chốt sau khi xem cấu trúc PDF thật):

| Mã `unit` | Đơn vị | Ví dụ |
|---|---|---|
| `b{nn}` | Bài số nn (2 chữ số) | `g8-b05` |
| `c{nn}-ltc{m}` | Luyện tập chung thứ m của chương nn | `g6-c02-ltc1` |
| `c{nn}-btcc` | Bài tập cuối chương nn | `g7-c03-btcc` |
| `c{nn}-intro` | Phần mở đầu chương (nếu có nội dung) | `g9-c01-intro` |
| `tn{m}` | Hoạt động thực hành trải nghiệm thứ m | `g6-tn1` |

`chunk_id = {unit_id}-{type}-{nn}`, với `nn` là thứ tự (2–3 chữ số) **trong cùng đơn vị và cùng loại**, theo thứ tự đọc. Ví dụ: `g8-b12-theorem-01`, `g6-c02-ltc1-exercise-03`.

- **Ổn định:** vì đếm theo (đơn vị, loại), thêm hoặc bớt một đoạn giải thích không làm đổi id của định lí hay ví dụ.
- **Khi đổi quy tắc chunk:** tăng `corpus_version`; `run_eval.py` kiểm tra mọi id trong golden set còn tồn tại và báo các id bị mất để cập nhật nhãn.
- Số chương và số bài được giả định đánh liên tục qua hai tập của một lớp (cần xác nhận), nên `volume` không nằm trong id.

## 5. Golden set

### 5.1 Định dạng

- File chính: `data/golden_set/golden_v1.jsonl` (chưa tạo). Ví dụ: `data/golden_set/examples.jsonl` (3 câu tổng hợp). JSON Schema: `data/golden_set/schema.json`, sinh từ lớp `GoldItem` bằng `scripts/export_schemas.py`.

| Trường | Bắt buộc | Mô tả |
|---|---|---|
| `qid` | ✅ | `q0001`, `q0002`, … (ví dụ tổng hợp: `ex-001`, …) |
| `question` | ✅ | Câu hỏi bằng lời của học sinh |
| `grade` | ✅ | Lớp của học sinh hỏi; mọi chunk gold phải có lớp ≤ `grade` |
| `qtype` | ✅ | `definition` · `formula` · `prerequisite` · `applied` |
| `gold_chunk_ids` | ✅ | Chunk trả lời trực tiếp (relevance = 2) |
| `supporting_chunk_ids` | | Chunk có ích nhưng chưa đủ để trả lời (relevance = 1) |
| `gold_concept_ids` | ✅ với `prerequisite` | Id khái niệm trong KG |
| `reference_answer` | | Đáp án ngắn tự viết |
| `source` | ✅ | `self` · `dhmath` · `synthetic` |
| `split` | ✅ | `dev` · `test` |
| `notes` | | Ghi chú |

Ví dụ:

```json
{"qid": "ex-003", "question": "Trước khi học rút gọn phân số, em cần ôn lại những kiến thức nào?",
 "grade": 6, "qtype": "prerequisite",
 "gold_chunk_ids": ["g6-b11-definition-02"], "supporting_chunk_ids": ["g6-b10-example-03"],
 "gold_concept_ids": ["ucln"], "reference_answer": null,
 "source": "synthetic", "split": "dev", "notes": "Ví dụ tổng hợp: id chunk chỉ để minh họa."}
```

### 5.2 Quy mô và phân bố

- **160 câu = 4 lớp × 4 loại × 10 câu.**
- Chia mỗi ô (lớp × loại) thành 2 câu `dev` + 8 câu `test`, tức **32 dev / 128 test**. Chỉ tinh chỉnh (prompt, trọng số RRF, ngưỡng, …) trên `dev`; báo cáo kết quả trên `test`.
- Biến thể "không dấu" của tập test được sinh tự động (bỏ dấu) cho ablation A8, không cần gán nhãn thêm.

### 5.3 Định nghĩa loại câu hỏi

| Loại | Mô tả | Ví dụ (tự viết) | Gold thường là |
|---|---|---|---|
| `definition` | Hỏi khái niệm, định nghĩa | "Số nguyên tố là gì?" | chunk `definition` |
| `formula` | Hỏi công thức, định lí, tính chất, quy tắc | "Công thức tính diện tích hình thang là gì?" | `formula` / `theorem` (+ `example` hỗ trợ) |
| `prerequisite` | Hỏi kiến thức cần có trước | "Muốn học phương trình bậc hai em cần ôn lại gì?" | định nghĩa/định lí của khái niệm tiên quyết trực tiếp (thường ở bài hoặc lớp trước) + `gold_concept_ids` |
| `applied` | Hỏi cách làm, giải thích "vì sao", vận dụng vào tình huống | "Làm sao biết một tam giác có vuông không khi biết độ dài ba cạnh?" | `theorem` + `example` minh họa |

### 5.4 Hướng dẫn gán nhãn

1. **Chọn ô cần lấp** (lớp × loại) để giữ cân bằng, rồi chọn một bài trong lớp đó.
2. **Viết câu hỏi bằng lời của học sinh.** Không chép câu chữ SGK: vừa vì bản quyền, vừa để tránh thiên lệch từ vựng có lợi cho BM25. Đa dạng cách hỏi: văn nói, viết tắt (ƯCLN), ký hiệu viết bằng chữ ("x bình phương") hoặc kiểu gõ máy ("x^2"). Viết có dấu; biến thể không dấu được sinh tự động.
3. **Tìm chunk gold bằng nhiều cách** (tìm BM25, tìm dense, duyệt theo bài) để không thiên vị một phương pháp. Ghi `gold_chunk_ids` (đủ để trả lời) và `supporting_chunk_ids` (có ích).
4. **Đặt `grade`** là lớp của học sinh hỏi. Với câu `prerequisite`, chunk gold có thể thuộc lớp thấp hơn.
5. **Câu `prerequisite`:** ghi `gold_concept_ids` theo KG. Chunk gold là định nghĩa/định lí của các khái niệm tiên quyết **trực tiếp** (1 bước), không liệt kê cả chuỗi; khái niệm xa hơn đưa vào `supporting_chunk_ids` nếu thật sự có ích.
6. **`reference_answer`** (khuyến khích với `definition` và `formula`): 1–2 câu tự viết.
7. **LLM chỉ được dùng để gợi ý cách diễn đạt câu hỏi.** Mọi nhãn do người gán nhãn kiểm tra; ghi vào `notes` nếu câu hỏi do LLM gợi ý.
8. **Kiểm tra chất lượng:** (a) câu hỏi trả lời được bằng SGK; (b) mọi id tồn tại trong corpus hiện tại (script kiểm tra); (c) không có câu trùng lặp; (d) sau một tuần, gán nhãn lại 10% số câu để đo độ nhất quán của chính người gán nhãn (`TBD`).
9. **Đóng băng `golden_v1`** (mốc M3) trước khi chạy benchmark chính. Sửa sau thời điểm đó thì tạo `golden_v2` và ghi lý do.

## 6. Lược đồ đồ thị kiến thức (KG)

Nguồn chuẩn: [`data/kg/schema.yaml`](../data/kg/schema.yaml) (mã nguồn đọc trực tiếp file này). Ví dụ nhỏ: [`data/kg/example_graph.json`](../data/kg/example_graph.json). Kiểm tra: `uv run python scripts/build_kg.py --validate <file>`.

### 6.1 Nút

| Loại | Id | Thuộc tính bắt buộc | Thuộc tính tùy chọn | Ví dụ |
|---|---|---|---|---|
| `concept` | slug ASCII không dấu, ví dụ `so-nguyen-to` | `name`, `kind`, `grade_introduced` | `aliases`, `description`, `curriculum_ref` | Số nguyên tố (`kind: concept`, lớp 6) |
| `lesson` | trùng `unit_id`, ví dụ `g6-b10` | `grade`, `title` | `number`, `volume`, `chapter` | Toán 6, Bài 10 |
| `chapter` | `g{grade}-c{nn}`, ví dụ `g6-c02` | `grade`, `number`, `title` | | Toán 6, Chương II |

- `kind` ∈ `topic`, `concept`, `theorem`, `formula`, `property`, `method`.
- `grade_introduced` có thể nhỏ hơn 6 với khái niệm tiên quyết từ tiểu học (khái niệm đó không có bài trong corpus).

### 6.2 Cạnh

| Loại | Từ → Đến | Ý nghĩa | Ràng buộc | Ví dụ |
|---|---|---|---|---|
| `prerequisite_of` | concept → concept | Cần biết A trước khi học B | Không có chu trình; `grade_introduced(A) ≤ grade_introduced(B)` | `uoc-va-boi → so-nguyen-to` |
| `related_to` | concept — concept | Liên quan (đối xứng) | Chỉ lưu một chiều | `so-nguyen-to — hop-so` |
| `part_of` | concept → concept; lesson → chapter | Thuộc về | Không có chu trình | `g6-b10 → g6-c02` |
| `appears_in_lesson` | concept → lesson | Khái niệm xuất hiện trong bài | `role` ∈ `introduced`, `used` | `so-nguyen-to → g6-b10` (`introduced`) |

### 6.3 Định dạng file

- Hiệu đính tay (commit): `data/kg/curated/lessons.csv`, `concepts.csv`, `edges.csv` (`TBD`).
- Ứng viên do LLM gợi ý: `data/kg/candidates/*.csv` (`status: candidate`), chỉ chứa id, tên và `chunk_id` làm bằng chứng.
- Đồ thị đã xây dựng: `data/kg/graph.json`, JSON node-link (`graph`, `nodes`, `edges`), cùng định dạng với `example_graph.json`.

### 6.4 Quy trình xây dựng

1. Nút `chapter` và `lesson` từ mục lục SGK (tên bài là thông tin ngắn mang tính sự kiện).
2. Nút `concept` và `grade_introduced` từ Chương trình GDPT 2018 (nội dung, yêu cầu cần đạt), đối chiếu với khung "KHÁI NIỆM, THUẬT NGỮ" ở đầu mỗi bài: khái niệm trong khung → cạnh `appears_in_lesson` (`role = introduced`) tới bài đó.
3. LLM gợi ý khái niệm và quan hệ ứng viên theo từng bài (`kg.extract`) → CSV.
4. Người hiệu đính chấp nhận, sửa hoặc xóa từng dòng → `curated/`.
5. `scripts/build_kg.py` xây dựng đồ thị và kiểm tra bằng `kg.schema.validate_graph`: kiểu nút/cạnh hợp lệ, `prerequisite_of` và `part_of` không có chu trình, tính đơn điệu theo lớp.
6. Ưu tiên độ phủ cho các khái niệm xuất hiện trong golden set. Quy mô đồ thị: `TBD` sau bước 2.
