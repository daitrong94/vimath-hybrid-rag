# Lộ trình (Roadmap)

**Hạn cuối:** ≈ Chủ nhật 03/01/2027 (cần xác nhận) · **Yêu cầu nộp bài:** `TBD` · **Thời gian:** 6 tuần, từ 23/11/2026.

Nguyên tắc: đạt **kết quả tối thiểu chạy được end-to-end (MVR)** càng sớm càng tốt, sau đó mới mở rộng. Mã chưa làm được đánh dấu `TODO(Mx)` theo mốc bên dưới.

## Mốc kiểm tra

| Mốc | Ngày | Tiêu chí hoàn thành |
|---|---|---|
| M0 – Khung dự án | 22/11/2026 | Skeleton, tài liệu, cấu hình, test smoke chạy được |
| M1 – Corpus v1 | 29/11/2026 | 8 PDF đã probe; đã chọn backend OCR; có `chunks.jsonl` cho ít nhất 1 lớp (mục tiêu: cả 4 lớp); độ đo truy hồi có test |
| **M2 – MVR** ⭐ | **06/12/2026** | `run_eval.py --methods bm25 dense` chạy end-to-end trên golden set hiện có (≥ 80 câu) và xuất bảng từ dữ liệu thật |
| M3 – Graph + golden v1 | 13/12/2026 | KG đã hiệu đính và qua kiểm tra; Graph retriever chạy được; golden set 160 câu đã đóng băng |
| M4 – Benchmark truy hồi | 20/12/2026 | Hybrid, Hybrid + Rerank; Bảng 1, 2, 4 trên test; LLM client, prompt, `answer()` hoạt động |
| M5 – Sinh + demo | 27/12/2026 | Đánh giá sinh (Bảng 3), demo Gradio, phân tích lỗi |
| M6 – Nộp bài | 03/01/2027 | Báo cáo, slide, README có kết quả, kiểm tra tái lập từ bản clone sạch |

## Kế hoạch theo tuần

### Tuần 1 (23/11 – 29/11): Dữ liệu → M1

- [ ] Tải 8 PDF vào `data/raw/`, đặt tên theo [DATA.md, mục 1.1](DATA.md#11-sách-giáo-khoa-corpus-chính)
- [ ] Triển khai `ingest/probe.py` + test; chạy probe, ghi nhận loại PDF
- [ ] Thử OCR trên Colab: Marker vs. MinerU, khoảng 10 trang mẫu mỗi lớp → chọn backend, điền `command` trong `configs/corpus.yaml`
- [ ] Triển khai `convert.py` (mốc trang, manifest), `normalize.py`, `chunker.py` v0 + test
- [ ] Chạy convert + chunk, ưu tiên một lớp trước (ví dụ lớp 8) rồi mở rộng
- [ ] Triển khai độ đo truy hồi + test (Hit@k, Recall@k, MRR, nDCG, Unit-Hit, Out-of-grade)
- [ ] Viết công cụ hỗ trợ gán nhãn (tìm chunk theo từ khóa/bài); bắt đầu golden set (mục tiêu 40 câu)

### Tuần 2 (30/11 – 06/12): MVR ⭐ → M2

- [ ] BM25 (bm25s + token hóa tiếng Việt): build/save/load/retrieve + test
- [ ] Dense (bge-m3 + FAISS): encode corpus (laptop hoặc Colab), retrieve + test
- [ ] `run_eval.py` phần truy hồi: kiểm tra id gold, chạy các phương pháp, ghi `results/runs/` và `results/tables/`
- [ ] Golden set đạt ≥ 80 câu, cân bằng lớp × loại
- [ ] **Mốc M2:** bảng BM25 vs. Dense đầu tiên từ dữ liệu thật

### Tuần 3 (07/12 – 13/12): Đồ thị kiến thức + Graph retriever → M3

- [ ] Nút bài/chương từ mục lục SGK; nút khái niệm từ Chương trình GDPT 2018
- [ ] `kg/extract.py` (LLM, Gemini free tier) → ứng viên → hiệu đính → `build_kg.py`
- [ ] Liên kết khái niệm ↔ chunk
- [ ] Graph retriever (liên kết khái niệm + PPR/BFS) + test
- [ ] Hoàn thành golden set 160 câu; kiểm tra chất lượng; **đóng băng `golden_v1`**

### Tuần 4 (14/12 – 20/12): Hybrid, Rerank, Sinh → M4

- [ ] RRF + lọc theo lớp + reranker (bge-reranker-v2-m3) + test; tinh chỉnh trên dev
- [ ] `generation/llm.py` (Gemini, OpenAI/Anthropic, Ollama) + cache + `CostTracker`
- [ ] Prompt trả lời/gợi ý/closed-book; `api.answer()`
- [ ] Chạy benchmark truy hồi đầy đủ trên test; ablation A1–A3, A7, A8 nếu kịp
- [ ] Chọn mô hình `final` và `judge`; ước tính chi phí từ số token đo được

### Tuần 5 (21/12 – 27/12): Đánh giá sinh, demo, phân tích lỗi → M5

- [ ] Hiệu chỉnh LLM-judge (30 câu dev chấm tay)
- [ ] Chạy đánh giá sinh trên test trong giới hạn ngân sách (Bảng 3)
- [ ] Demo Gradio; chụp ảnh/quay video demo cho báo cáo
- [ ] Phân tích lỗi theo [EVALUATION.md, mục 9](EVALUATION.md#9-phân-tích-lỗi)
- [ ] *(Tùy chọn, chỉ khi M2–M4 đúng hạn)* fine-tune embedding trên Colab

### Tuần 6 (28/12 – 03/01): Viết báo cáo → M6

- [ ] Báo cáo theo [REPORT_OUTLINE.md](REPORT_OUTLINE.md); slide
- [ ] Cập nhật README (kết quả + `run_id`), dọn mã, kiểm tra tái lập từ bản clone sạch
- [ ] Thời gian dự phòng (nghỉ Tết Dương lịch 01/01)

## Quy tắc ưu tiên khi trễ tiến độ

1. Giữ bằng được M2 (MVR): nếu OCR chậm, chạy MVR trên 1–2 lớp trước.
2. Nếu đến 13/12 KG chưa xong: thu hẹp KG về các khái niệm có trong golden set.
3. Đánh giá sinh có thể thu gọn về closed-book vs. Hybrid + Rerank.
4. Mục tùy chọn (fine-tune embedding, phân loại lớp/chủ đề) chỉ làm khi đã đạt M4.

## Việc còn mở (cần thông tin)

- [ ] Xác nhận hạn nộp và yêu cầu nộp bài của môn học
- [ ] Mã dataset DHMATH trên Hugging Face + giấy phép
- [ ] Mô hình `final` (GPT hay Claude) và `judge`
- [ ] Tên hội thảo mục tiêu và định dạng bài báo
