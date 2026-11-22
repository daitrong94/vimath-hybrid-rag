# Tổng quan đề tài (Project Brief)

> Mô tả bài toán, động lực, câu hỏi nghiên cứu, đóng góp dự kiến và phạm vi của đề tài.
> Mọi kết quả và số liệu chỉ được điền sau khi chạy thực nghiệm; hiện tại ghi `TBD`.

## 1. Thông tin chung

| Mục | Nội dung |
|---|---|
| Môn học | Xử lý ngôn ngữ tự nhiên (NLP), Trường ĐH Khoa học Tự nhiên – ĐHQGHN (HUS) |
| Hình thức | Đề tài cá nhân |
| Chương trình nghiên cứu | Gia sư AI (AI Tutor) cho môn Toán THCS (lớp 6–9); mỗi sinh viên phụ trách một chủ đề con |
| Chủ đề con | **#8 – Truy hồi thông tin (Information Retrieval) & RAG** |
| Tên đề tài | *Xây dựng hệ thống Hybrid RAG kết hợp đồ thị kiến thức chương trình Toán THCS hỗ trợ giải thích và sinh gợi ý* |
| Tên tiếng Anh | *Hybrid RAG with a curriculum knowledge graph over Vietnamese grade 6–9 math textbooks, to support explanations and hint generation* |
| Hạn hoàn thành | ≈ 03/01/2027 (cần xác nhận), xem [ROADMAP.md](ROADMAP.md) |
| Yêu cầu nộp bài của môn học | `TBD` (chưa công bố) |
| Nơi công bố dự kiến | Hội thảo/hội nghị trong nước về CNTT & Giáo dục (`TBD` tên cụ thể) |
| Giấy phép mã nguồn | MIT |

## 2. Bài toán

**Đầu vào:** một câu hỏi tiếng Việt về Toán của học sinh THCS, kèm (tùy chọn) lớp của học sinh `g ∈ {6, 7, 8, 9}` và chế độ: `answer` (giải thích) hoặc `hint` (gợi ý).

**Đầu ra:**

1. Danh sách top-k đoạn trích (chunk) liên quan nhất từ SGK Toán 6–9 (định nghĩa, định lí, công thức, ví dụ, …), kèm metadata: lớp, chương, bài, trang, loại nội dung.
2. Câu trả lời hoặc gợi ý do LLM sinh ra **chỉ dựa trên** các đoạn trích đó, có trích dẫn dạng "SGK Toán 8, Bài X".

**Ràng buộc:**

- *Trung thực với nguồn (grounded):* không bịa công thức, không thêm kiến thức không có trong ngữ cảnh.
- *Phù hợp lớp:* không dùng kiến thức vượt quá chương trình của lớp `g` (lọc metadata `grade ≤ g`).
- *Dùng lại được:* cung cấp API Python `answer(...)` / `retrieve(...)` cho các module khác của hệ thống Gia sư AI.

## 3. Động lực

- **LLM dễ "ảo giác" với toán phổ thông:** nhớ sai công thức, dùng định lí ngoài chương trình, hoặc trình bày khác cách của SGK. Với học sinh THCS, một công thức sai hay một phương pháp "vượt lớp" đều ảnh hưởng xấu tới việc học.
- **Ngôn ngữ và ký hiệu riêng của SGK Việt Nam:** dấu phẩy thập phân (3,5), thuật ngữ theo chương trình mới (ví dụ "định lí Pythagore"), biến thể chính tả (lí/lý), hai kiểu đặt dấu thanh (hoà/hòa). Truy hồi từ vựng (BM25) nhạy với các biến thể này; truy hồi ngữ nghĩa (dense) và đồ thị khái niệm có thể bù lại.
- **Văn bản toán trộn ngôn ngữ tự nhiên và công thức (LaTeX):** chất lượng OCR và cách tách đoạn ảnh hưởng trực tiếp tới truy hồi.
- **Câu hỏi về quan hệ giữa các kiến thức** ("cần biết gì trước khi học X?") khó trả lời bằng so khớp văn bản; đồ thị kiến thức chương trình với quan hệ tiên quyết là nguồn thông tin tự nhiên cho loại câu hỏi này.
- **Cần đánh giá có hệ thống:** đề tài xây dựng một golden set có nhãn đến mức đoạn trích để so sánh các phương pháp truy hồi trên SGK Toán tiếng Việt. Khảo sát các bộ dữ liệu và công trình liên quan: `TBD`.

## 4. Câu hỏi nghiên cứu

| Mã | Câu hỏi |
|---|---|
| RQ1 | Trên SGK Toán 6–9 tiếng Việt, truy hồi **sparse** (BM25), **dense** (bge-m3) và **graph** (đồ thị kiến thức chương trình) so với nhau thế nào, tổng thể và theo từng loại câu hỏi (định nghĩa, công thức, tiên quyết, vận dụng)? |
| RQ2 | Kết hợp **hybrid** (Reciprocal Rank Fusion) và **reranker** cross-encoder cải thiện bao nhiêu so với phương pháp đơn tốt nhất, và tốn thêm bao nhiêu độ trễ? |
| RQ3 | **Lọc theo lớp** (`grade ≤ g`) loại bỏ được bao nhiêu kết quả "vượt lớp", và có làm giảm độ phủ (recall) không? |
| RQ4 | Truy hồi tốt hơn có giúp câu trả lời/gợi ý **trung thực hơn** (faithfulness) và **đúng trọng tâm hơn** (answer relevance) so với LLM không truy hồi (closed-book) không? Chi phí token là bao nhiêu? |
| RQ5 *(tùy chọn)* | Fine-tune mô hình embedding trên các cặp (câu hỏi, đoạn trích) có cải thiện truy hồi dense không? |

Thí nghiệm và độ đo cho từng câu hỏi: [EVALUATION.md](EVALUATION.md).

## 5. Đóng góp dự kiến

> Đây là đóng góp *dự kiến*; chỉ khẳng định trong báo cáo sau khi đã có kết quả.

1. **Pipeline dữ liệu tái lập được**: từ PDF SGK Toán 6–9 (bộ *Kết nối tri thức với cuộc sống*) đến các đoạn trích Markdown + LaTeX có metadata chương trình (lớp, chương, bài, trang, loại nội dung), xử lý được cả PDF có lớp văn bản lẫn PDF scan.
2. **Đồ thị kiến thức chương trình Toán THCS**: khái niệm, bài học, quan hệ tiên quyết / liên quan / thuộc về. Công bố cấu trúc đồ thị (không chứa văn bản SGK).
3. **Golden set 160 câu hỏi** có nhãn đến mức đoạn trích, cân bằng 4 lớp × 4 loại câu hỏi, kèm hướng dẫn gán nhãn. Công bố câu hỏi và mã đoạn trích.
4. **So sánh có hệ thống** Sparse / Dense / Graph / Hybrid (+ Rerank) về chất lượng truy hồi, chất lượng sinh, độ trễ và chi phí, kèm phân tích lỗi.
5. **Module dùng lại được**: API Python `answer(...)` / `retrieve(...)` và demo Gradio cho hệ thống Gia sư AI.

## 6. Phạm vi

### Trong phạm vi

1. Pipeline corpus: PDF → Markdown có LaTeX (công cụ OCR như Marker / MinerU) → chunk theo bài/mục kèm metadata (`grade`, `chapter`, `lesson`, `page`, `type`).
2. Bộ truy hồi: BM25; dense (bge-m3 + FAISS); graph (NetworkX, Neo4j tùy chọn); hybrid (RRF + reranker tùy chọn + lọc theo lớp).
3. Sinh câu trả lời / gợi ý có trích dẫn SGK; backend LLM hoán đổi được (API hoặc chạy cục bộ qua Ollama).
4. Đánh giá: golden set 160 câu; Recall@k, MRR, nDCG@k; faithfulness, answer relevance; độ trễ và chi phí token. Kết quả chính: một bảng so sánh BM25 / Dense / Graph / Hybrid / Hybrid + Rerank.
5. API Python `answer(question, grade=None, method="hybrid", mode="answer")`.
6. Demo Gradio một lượt: câu hỏi + lớp + phương pháp → câu trả lời + nguồn.

### Tùy chọn (nếu còn thời gian)

- Fine-tune mô hình embedding trên cặp (câu hỏi, đoạn trích), thêm dòng "Fine-tuned Dense" vào bảng kết quả.
- Bộ phân loại nhỏ dự đoán lớp/chủ đề của câu hỏi để lọc.

### Ngoài phạm vi

- Sản phẩm chatbot hoàn chỉnh: hội thoại nhiều lượt, đăng nhập, giao diện streaming, lưu lịch sử.
- Fine-tune LLM.
- Các bộ SGK khác (Cánh Diều, Chân trời sáng tạo); có thể mở rộng sau.

## 7. Giả định và ràng buộc

| Loại | Nội dung |
|---|---|
| Dữ liệu | 8 tập SGK Toán 6–9 bộ *Kết nối tri thức với cuộc sống* (Tập 1 + Tập 2 mỗi lớp), được chọn vì là bộ SGK thống nhất trên toàn quốc. Nguồn: Hành trang số (taphuan.nxbgd.vn); người thực hiện tự tải về `data/raw/`. Loại PDF (có lớp văn bản hay scan) chưa biết. |
| Bản quyền | Nội dung SGK có bản quyền: không commit PDF, kết quả OCR, văn bản chunk. Xem [DATA.md, mục 2](DATA.md#2-chính-sách-bản-quyền). |
| Tính toán | Laptop chỉ dùng CPU (GPU MX250 không đủ cho các mô hình); Google Colab T4 cho OCR và các tác vụ cần GPU. |
| Ngân sách API | Tổng cộng ≤ 10 USD. Gemini Flash (free tier) khi phát triển; GPT hoặc Claude cho lần chạy cuối (`TBD`). |
| Thời gian | 6 tuần (23/11/2026 – 03/01/2027), làm một mình. |
| Tái lập | Mọi bước chạy được bằng script + file cấu hình; notebook chỉ để khám phá. |

## 8. Rủi ro và phương án giảm thiểu

| Rủi ro | Ảnh hưởng | Giảm thiểu |
|---|---|---|
| PDF là bản scan, hoặc lớp văn bản lỗi font (TCVN3/VNI) | OCR chậm, sai dấu tiếng Việt | Bước `probe` phát hiện sớm (tuần 1); thử OCR trên trang mẫu trước khi chạy toàn bộ |
| OCR sai công thức (LaTeX) | Truy hồi và câu trả lời sai | So sánh Marker và MinerU trên trang mẫu; kiểm tra thủ công các bài có trong golden set |
| Xây dựng đồ thị kiến thức tốn công | Trễ phần Graph-RAG | Khởi tạo từ Chương trình GDPT 2018 + mục lục SGK; LLM gợi ý ứng viên, người hiệu đính; ưu tiên khái niệm có trong golden set |
| Gán nhãn golden set tốn thời gian | Thiếu dữ liệu đánh giá | Bắt đầu từ tuần 1, đạt ≥ 80 câu trước mốc MVR; có công cụ tìm kiếm hỗ trợ gán nhãn |
| Vượt ngân sách API | Không chạy được đánh giá cuối | Cache phản hồi LLM, dùng free tier khi phát triển, giới hạn chi phí cứng trong code, đánh giá sinh trên một tập con phương pháp |
| Thiên lệch khi gán nhãn (chỉ tìm gold bằng một phương pháp) | Kết quả ưu ái phương pháp đó | Tìm gold bằng nhiều cách (BM25 + dense + duyệt theo bài); viết câu hỏi bằng lời của học sinh |

## 9. Thuật ngữ

| Thuật ngữ | Giải thích |
|---|---|
| RAG | Retrieval-Augmented Generation: sinh văn bản có bổ sung ngữ cảnh truy hồi |
| Chunk (đoạn trích) | Đơn vị nội dung được truy hồi: một định nghĩa, định lí, công thức, ví dụ, bài tập hoặc đoạn giải thích |
| Golden set | Tập câu hỏi có nhãn đoạn trích đúng, dùng để đánh giá |
| BM25 | Mô hình truy hồi từ vựng (sparse) cổ điển |
| Dense retrieval | Truy hồi bằng vector embedding (ở đây: bge-m3) |
| Graph retrieval | Truy hồi dựa trên đồ thị kiến thức (khái niệm, quan hệ tiên quyết) |
| RRF | Reciprocal Rank Fusion: kết hợp nhiều danh sách xếp hạng |
| Reranker | Mô hình cross-encoder xếp hạng lại các ứng viên |
| Faithfulness | Mức độ câu trả lời được ngữ cảnh truy hồi hỗ trợ |
| MVR | Minimum Viable Result: kết quả tối thiểu chạy end-to-end (BM25 + Dense + đánh giá) |
