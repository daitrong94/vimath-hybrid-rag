# Dàn ý báo cáo và slide

> Yêu cầu định dạng của môn học: `TBD`. Dàn ý theo cấu trúc bài báo hội thảo (khoảng 6–8 trang, `TBD` theo hội thảo), có thể mở rộng thành báo cáo môn học.
> Mọi số liệu lấy từ `results/tables/` và ghi kèm `run_id`. Chỉ nêu đóng góp đã thực sự đạt được.

## Báo cáo

**Tên:** Xây dựng hệ thống Hybrid RAG kết hợp đồ thị kiến thức chương trình Toán THCS hỗ trợ giải thích và sinh gợi ý

**Tóm tắt** (150–200 từ): bài toán; phương pháp; dữ liệu (SGK Toán 6–9, golden set 160 câu); kết quả chính (`TBD`); ý nghĩa cho hệ thống Gia sư AI.

### 1. Giới thiệu

- Bối cảnh: Gia sư AI cho Toán THCS; LLM bịa công thức và dùng kiến thức vượt lớp
- Ý tưởng: truy hồi từ SGK kết hợp đồ thị kiến thức chương trình, lọc theo lớp, sinh có trích dẫn
- Câu hỏi nghiên cứu RQ1–RQ4 (RQ5 nếu làm)
- Đóng góp

### 2. Nghiên cứu liên quan

- RAG: Lewis et al. (2020)
- Truy hồi sparse và dense: BM25 (Robertson & Zaragoza, 2009); DPR (Karpukhin et al., 2020); BGE M3-Embedding (Chen et al., 2024); benchmark BEIR (Thakur et al., 2021)
- Hợp nhất và xếp hạng lại: RRF (Cormack et al., 2009); reranking bằng cross-encoder (Nogueira & Cho, 2019)
- RAG trên đồ thị: GraphRAG (Edge et al., 2024); HippoRAG (Gutiérrez et al., 2024); học quan hệ tiên quyết giữa khái niệm (Pan et al., 2017)
- Đánh giá RAG: RAGAS (Es et al., 2024); LLM-as-a-judge (Zheng et al., 2023)
- NLP tiếng Việt: PhoBERT (Nguyen & Nguyen, 2020); trích xuất tài liệu và công thức: MinerU (Wang et al., 2024)
- AI trong giáo dục toán bằng tiếng Việt, các bộ dữ liệu liên quan: `TBD` (cần khảo sát)

> Kiểm tra lại thông tin trích dẫn (tác giả, năm, nơi công bố) trước khi nộp.

### 3. Dữ liệu

- 3.1 Corpus SGK: nguồn, pipeline, thống kê số chunk theo lớp và loại (`TBD`), đánh giá chất lượng OCR trên mẫu (`TBD`)
- 3.2 Đồ thị kiến thức: lược đồ, quy trình xây dựng, thống kê (`TBD`)
- 3.3 Golden set: hướng dẫn gán nhãn, phân bố, độ nhất quán khi gán nhãn lại (`TBD`)
- 3.4 Bản quyền và đạo đức dữ liệu

### 4. Phương pháp

- 4.1 Tổng quan kiến trúc (Hình 1)
- 4.2 BM25 và token hóa tiếng Việt
- 4.3 Dense: bge-m3 + FAISS
- 4.4 Graph retriever: liên kết khái niệm, PPR, ánh xạ khái niệm → chunk
- 4.5 Hybrid: RRF, lọc theo lớp, reranker
- 4.6 Sinh câu trả lời và gợi ý có trích dẫn

### 5. Thực nghiệm

- 5.1 Thiết lập: phần cứng, mô hình, siêu tham số, chia dev/test
- 5.2 Kết quả truy hồi (Bảng 1, 2): RQ1, RQ2
- 5.3 Lọc theo lớp (Bảng 4): RQ3
- 5.4 Kết quả sinh (Bảng 3): RQ4
- 5.5 Ablation
- 5.6 Độ trễ và chi phí

### 6. Phân tích lỗi

Bảng nguyên nhân × phương pháp; ví dụ minh họa (EVALUATION.md, mục 9).

### 7. Thảo luận

Hạn chế: một bộ SGK, golden set nhỏ, một người gán nhãn, giới hạn của LLM-judge. Hướng tích hợp vào hệ thống Gia sư AI.

### 8. Kết luận và hướng phát triển

### Phụ lục

A. Prompt · B. Hướng dẫn gán nhãn · C. Lược đồ KG · D. Siêu tham số · E. Hướng dẫn tái lập

### Hình và bảng dự kiến

| Mã | Nội dung | Nguồn |
|---|---|---|
| Hình 1 | Sơ đồ pipeline | [ARCHITECTURE.md](ARCHITECTURE.md) (Mermaid) |
| Hình 2 | Đồ thị con quanh một khái niệm | `data/kg/graph.json` |
| Hình 3 | Recall@k theo k cho các phương pháp | `results/plots/` |
| Hình 4 | Ví dụ đầu ra demo (câu trả lời + nguồn) | ảnh chụp demo |
| Bảng 1–4 | Như [EVALUATION.md, mục 6](EVALUATION.md#6-bảng-kết-quả-mẫu) | `results/tables/` |

## Slide (khoảng 12–15 trang, `TBD` theo thời lượng trình bày)

1. Tiêu đề
2. Vấn đề: LLM bịa công thức, vượt lớp (ví dụ minh họa)
3. Mục tiêu và câu hỏi nghiên cứu
4. Dữ liệu: từ SGK đến chunk (pipeline offline)
5. Đồ thị kiến thức chương trình (hình đồ thị con)
6. Các bộ truy hồi: BM25 / Dense / Graph
7. Hybrid: RRF + rerank + lọc theo lớp
8. Golden set và độ đo
9. Kết quả chính (Bảng 1)
10. Theo loại câu hỏi và lọc theo lớp
11. Sinh câu trả lời: faithfulness, chi phí
12. Phân tích lỗi
13. Demo
14. Hạn chế và hướng phát triển
15. Kết luận
