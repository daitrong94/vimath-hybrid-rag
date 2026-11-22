# Notebooks

Chỉ dùng để **khám phá**: xem nhanh chunk, thử tham số, vẽ hình nháp. Mọi logic tạo ra kết quả trong báo cáo phải nằm trong `src/` và `scripts/`, chạy bằng file cấu hình trong `configs/`.

- Đặt tên: `NN_mo-ta-ngan.ipynb`, ví dụ `01_probe-pdf.ipynb`.
- Output notebook có thể chứa văn bản SGK, nên hook `nbstripout` (pre-commit) tự xóa output khi commit. Chạy `uv run pre-commit install` một lần sau khi clone.
- Kernel: dùng môi trường của dự án (`uv run jupyter lab` sau khi tự cài Jupyter, ví dụ `uv add --dev jupyterlab`).
