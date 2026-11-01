# Week 07 — Extended Lab (Lab 4): FastAPI Routing & Request/Response

## How to run
1. Tạo và kích hoạt môi trường ảo (nếu chưa có):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install fastapi "uvicorn[standard]"
   ```
2. Chạy server từ thư mục `backend`:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
3. Giao diện: `http://127.0.0.1:8000/` (tự chuyển tới `/static/index.html`)
   Swagger UI: `http://127.0.0.1:8000/docs`

## Endpoints
| Method | Path | Mô tả |
|---|---|---|
| GET | `/items` | Danh sách (filter `min_price`, `max_price`, `q`; sort `sort_by`, `order`; phân trang `skip`, `limit`) — trả về envelope |
| GET | `/items/{id}` | Chi tiết, 404 nếu không có |
| POST | `/items` | Tạo mới (201), 409 nếu trùng tên |
| PUT | `/items/{id}` | Thay thế toàn bộ, 409 nếu đổi sang tên đã tồn tại |
| PATCH | `/items/{id}` | Cập nhật một phần, 409 nếu đổi sang tên đã tồn tại |
| DELETE | `/items/{id}` | Xoá (204) |
| POST | `/predict/house-price` | Dự đoán giá nhà (công thức giả lập) |

## Part A — PATCH vs PUT
`model_dump(exclude_unset=True)` chỉ trả về những field client thực sự gửi lên, nên PATCH chỉ sửa đúng các field đó, còn lại giữ nguyên. Nếu client gửi `null` cho một field thì field đó bị bỏ qua, vì `name`/`price` không được để trống.

**Vì sao PATCH với `ItemUpdate` khác PUT với `ItemCreate` dù cùng JSON body?**
PUT nghĩa là "đây là trạng thái đầy đủ mới của resource": field nào client bỏ qua thì về lý phải reset về mặc định (vì vậy `ItemCreate` bắt buộc đủ field). PATCH nghĩa là "chỉ sửa những gì tôi gửi": field bỏ qua giữ nguyên giá trị cũ.

## Part B — Filter, search, sort
Thứ tự xử lý trong `list_items`: **lọc → sắp xếp → đếm `total` → cắt `skip/limit`**. Nếu cắt trang trước rồi mới lọc, một trang có thể bị lọc thành rỗng dù vẫn còn item khớp ở các trang sau, khiến phân trang sai.
`sort_by` và `order` được ràng buộc bằng `Query(pattern=...)`; giá trị sai sẽ trả về 422. `q` có độ dài dưới 2 ký tự cũng trả về 422.

## Part C — 409 Conflict
Tên được so sánh không phân biệt hoa/thường. Khi PUT/PATCH, việc kiểm tra bỏ qua chính item đang sửa, nên đổi `Apple` → `apple` vẫn hợp lệ. Dùng 409 vì request hợp lệ về cú pháp (không phải 422) nhưng xung đột với trạng thái hiện tại của server.

## Part D — Envelope
`GET /items` trả về `{items, total, skip, limit}`, trong đó `total` là số item **sau khi lọc, trước khi cắt trang**, đủ để client hiển thị "Trang 3 / 12".

## Part E — Toy prediction
`HousePriceRequest` dùng `Field(gt=0)` / `Field(ge=0)` để ràng buộc body, nên `area_sqm <= 0` tự động trả về 422 mà không cần `if` trong hàm. Sau này chỉ cần thay công thức bằng `model.predict(...)`.

Ví dụ: `{"area_sqm": 80, "bedrooms": 3, "distance_to_center_km": 5}` → `{"predicted_price": 1235000000.0, "currency": "VND"}`
