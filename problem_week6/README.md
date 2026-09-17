# Mini House-Price Prediction API

## How to run the project
1. Tạo và kích hoạt môi trường ảo (nếu chưa có):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install fastapi "uvicorn[standard]"
   ```
   *(Lưu ý: Nếu gặp lỗi thiếu thư viện venv trên Ubuntu, bạn cần chạy `sudo apt install python3.12-venv` trước)*
   
2. Mở terminal và truy cập vào thư mục `backend`:
   ```bash
   cd backend
   ```
3. Chạy server FastAPI bằng `uvicorn`:
   ```bash
   uvicorn main:app --reload
   ```
4. Mở trình duyệt và truy cập vào địa chỉ sau để xem giao diện:
   ```
   http://127.0.0.1:8000/static/house_form.html
   ```

## Testing via /docs (Task 3)
API có thể được test trực tiếp qua Swagger UI bằng cách truy cập:
`http://127.0.0.1:8000/docs`
Tại đây, bạn mở endpoint `GET /predict`, chọn **Try it out**, nhập các thông số (ví dụ: `area=80`, `bedrooms=3`, `location=hanoi`), sau đó bấm **Execute**. Server sẽ trả về HTTP Status 200 kèm theo JSON response chính xác chứa thông tin phòng và giá nhà dự đoán.

## Task 3: Explanation
1. **Calling `/predict` without `location` works. Why?**
   Bởi vì tham số `location` trong hàm đã được gán một giá trị mặc định là `"other"` (`location: str = "other"`). Do đó, nó trở thành tham số tùy chọn (optional parameter) và nếu không được truyền trên URL, FastAPI sẽ tự động dùng giá trị mặc định này.

2. **Calling `/predict` without `area` returns a 422 error. Why?**
   Bởi vì tham số `area` được khai báo nhưng không có giá trị mặc định, nên nó là một tham số bắt buộc (required parameter). FastAPI sẽ tự động thực hiện việc kiểm tra đầu vào (validation). Nếu bị thiếu, nó sẽ trả về lỗi 422 (Unprocessable Entity).

## Task 5: Explanation
1. **Why does a relative URL (e.g., `/predict`) work now in `fetch()`?**
   Bởi vì chúng ta đã dùng `StaticFiles` để host trang frontend HTML trên cùng một server với API (cùng chạy trên `http://127.0.0.1:8000`). Trình duyệt sẽ tự động ghép đường dẫn tương đối `/predict` vào phía sau origin hiện tại của trang web để tạo thành URL hoàn chỉnh. Việc này cũng giúp chúng ta tránh được lỗi bảo mật CORS.

## Task 6: Bonus Explanation
**Difference between sending data via query parameters and JSON body:**
Gửi dữ liệu qua Query Parameters thì dữ liệu được đính kèm trực tiếp trên URL (vd: `?area=50&bedrooms=2`), phù hợp cho phương thức GET và dữ liệu ngắn, dễ đọc. Trong khi đó, gửi qua JSON Body (thường dùng trong POST) thì dữ liệu được giấu trong phần body của HTTP request (không hiển thị trên URL), có cấu trúc rõ ràng (JSON) và phù hợp để truyền dữ liệu lớn hoặc phức tạp.
