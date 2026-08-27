/* =========================================================
   CV cá nhân — app.js          Tuần 4: JavaScript & DOM

   Tuần 3 bạn đã trang trí xong trang này bằng CSS.
   Tuần 4 làm nó SỐNG DẬY: lọc kỹ năng, vẽ lại danh sách từ dữ
   liệu, kiểm tra form liên hệ. Không sửa index.html, không sửa
   style.css — chỉ viết vào 4 phần dưới đây.

   Mở Console (F12 -> tab Console) và để mở suốt buổi.
   Kiểm tra file đã được nối: bỏ chú thích dòng dưới, lưu lại,
   Console phải in ra dòng chữ đó.
   ========================================================= */

// console.log("app.js đã chạy");


/* ===== DỮ LIỆU DÙNG CHUNG CHO CẢ 4 LAB — đã cho sẵn ===== */

const skills = [
  { ten: "Python",     mucDo: "Khá",    nam: 2, ghiChu: "pandas, numpy, matplotlib" },
  { ten: "SQL",        mucDo: "Khá",    nam: 2, ghiChu: "truy vấn nhiều bảng, window function" },
  { ten: "HTML & CSS", mucDo: "Cơ bản", nam: 1, ghiChu: "dựng trang tĩnh, responsive" },
  { ten: "Tiếng Anh",  mucDo: "B2",     nam: 5, ghiChu: "đọc tài liệu kỹ thuật" },
];


/* =========================================================
   LAB 1 — CÚ PHÁP JS               (chỉ làm việc với Console)
   ---------------------------------------------------------
   1. locTheoNam(list, toiThieu)   -> mảng các kỹ năng có nam >= toiThieu
                                      (viết bằng vòng for, rồi viết lại bằng filter)
   2. tongSoNam(list)              -> tổng trường nam của cả mảng
   3. lauNhat(list)                -> object có nam lớn nhất
   4. In từng kỹ năng bằng forEach + template literal, dạng:
         `Python: 2 năm (Khá)`

   CONSOLE PHẢI IN RA:
      3 kỹ năng từ 2 năm: Python, SQL, Tiếng Anh
      Tổng số năm: 10
      Lâu nhất: Tiếng Anh (5 năm)
      Python: 2 năm (Khá)
      SQL: 2 năm (Khá)
      HTML & CSS: 1 năm (Cơ bản)
      Tiếng Anh: 5 năm (B2)
   ========================================================= */

// 1. Hàm lọc kỹ năng theo số năm tối thiểu
// Cách 1: Dùng vòng lặp for truyền thống
function locTheoNamBangFor(list, toiThieu) {
  let ketQua = [];
  for (let i = 0; i < list.length; i++) {
    if (list[i].nam >= toiThieu) {
      ketQua.push(list[i]);
    }
  }
  return ketQua;
}

// Cách 2: Dùng phương thức .filter() ngắn gọn
function locTheoNam(list, toiThieu) {
  return list.filter(item => item.nam >= toiThieu);
}

// 2. Hàm tính tổng số năm kinh nghiệm của cả danh sách
function tongSoNam(list) {
  let tong = 0;
  for (let i = 0; i < list.length; i++) {
    tong += list[i].nam;
  }
  return tong;
}

// 3. Hàm tìm kỹ năng có số năm kinh nghiệm lớn nhất (lâu nhất)
function lauNhat(list) {
  if (list.length === 0) return null;
  let maxItem = list[0];
  for (let i = 1; i < list.length; i++) {
    if (list[i].nam > maxItem.nam) {
      maxItem = list[i];
    }
  }
  return maxItem;
}

// 4. In kết quả ra Console đúng theo định dạng yêu cầu

// In danh sách các kỹ năng từ 2 năm trở lên
const dsLoc = locTheoNam(skills, 2);
const tenCacKyNang = dsLoc.map(s => s.ten).join(", ");
console.log(`${dsLoc.length} kỹ năng từ 2 năm: ${tenCacKyNang}`);

// In tổng số năm kinh nghiệm
console.log(`Tổng số năm: ${tongSoNam(skills)}`);

// In kỹ năng có kinh nghiệm lâu nhất
const knLauNhat = lauNhat(skills);
console.log(`Lâu nhất: ${knLauNhat.ten} (${knLauNhat.nam} năm)`);

// Duyệt qua từng kỹ năng bằng forEach và in ra màn hình bằng template literal
skills.forEach(s => {
  console.log(`${s.ten}: ${s.nam} năm (${s.mucDo})`);
});




/* =========================================================
   LAB 2 — CHỌN VÀ SỬA PHẦN TỬ         (chưa tạo phần tử mới)
   ---------------------------------------------------------
   1. document.querySelectorAll(".skill") -> in ra số thẻ (phải là 4)
   2. Đọc số năm của từng thẻ bằng  the.dataset.years
      Lưu ý: giá trị đọc ra là CHUỖI -> Number(...) mới so sánh được
   3. lamMoThePhu(toiThieu)  -> duyệt các thẻ bằng forEach:
         nam <  toiThieu  ->  the.classList.add("dimmed")
         nam >= toiThieu  ->  the.classList.remove("dimmed")
   4. Gọi lamMoThePhu(2)

   PHẢI THẤY: thẻ "HTML & CSS" (1 năm) mờ đi, ba thẻ còn lại bình thường.
   Lớp .dimmed đã có sẵn trong style.css — JS chỉ gắn tên lớp vào.
   ========================================================= */

// 1. Chọn tất cả các thẻ .skill và in ra số lượng
const cacTheSkill = document.querySelectorAll(".skill");
console.log(`Số thẻ kỹ năng ban đầu: ${cacTheSkill.length}`);

// 2 & 3. Hàm làm mờ thẻ có số năm kinh nghiệm nhỏ hơn toiThieu
function lamMoThePhu(toiThieu) {
  const cards = document.querySelectorAll(".skill");
  cards.forEach(the => {
    // the.dataset.years lấy giá trị thuộc tính data-years (chuỗi)
    const nam = Number(the.dataset.years);
    if (nam < toiThieu) {
      the.classList.add("dimmed");
    } else {
      the.classList.remove("dimmed");
    }
  });
}

// 4. Gọi hàm làm mờ thẻ dưới 2 năm kinh nghiệm
lamMoThePhu(2);




/* =========================================================
   LAB 3 — TẠO VÀ XÓA PHẦN TỬ
   ---------------------------------------------------------
   1. veKyNang(list) — vẽ lại toàn bộ khu .skills từ dữ liệu:
         a. const khung = document.querySelector(".skills");
         b. khung.innerHTML = "";                  // xóa sạch thẻ cũ
         c. list.forEach(...) với mỗi phần tử:
               const the = document.createElement("div");
               the.classList.add("skill");
               the.dataset.years = s.nam;
               the.innerHTML = `<h3>...</h3><p class="level">...</p>
                                <p class="note">... — ... năm</p>`;
               khung.appendChild(the);
   2. Gọi veKyNang(skills) rồi gọi lại lamMoThePhu(2)
   3. Thử veKyNang(locTheoNam(skills, 2)) -> chỉ còn 3 thẻ

   PHẢI THẤY: giao diện y hệt trước, nhưng bây giờ 4 thẻ do JS
   sinh ra. Xóa một phần tử của mảng skills rồi tải lại trang:
   thẻ tương ứng biến mất mà không cần sửa HTML.
   ========================================================= */

// 1. Hàm vẽ lại danh sách kỹ năng từ mảng dữ liệu (Array of Objects)
function veKyNang(list) {
  const khung = document.querySelector(".skills");
  if (!khung) return;

  // Xóa sạch các thẻ HTML tĩnh cũ
  khung.innerHTML = "";

  // Tạo và chèn từng thẻ mới từ dữ liệu
  list.forEach(s => {
    const the = document.createElement("div");
    the.classList.add("skill");
    the.dataset.years = s.nam; // gán thuộc tính data-years
    the.innerHTML = `
      <h3>${s.ten}</h3>
      <p class="level">${s.mucDo}</p>
      <p class="note">${s.ghiChu} — ${s.nam} năm</p>
    `;
    khung.appendChild(the);
  });
}

// 2. Vẽ lại toàn bộ 4 thẻ từ biến skills và làm mờ thẻ dưới 2 năm
veKyNang(skills);
lamMoThePhu(2);




/* =========================================================
   LAB 4 — SỰ KIỆN VÀ KIỂM TRA FORM
   ---------------------------------------------------------
   1. Hai nút lọc:
         #btn-all -> veKyNang(skills)
         #btn-exp -> veKyNang(locTheoNam(skills, 2))
      (dùng addEventListener("click", ...), nhớ gọi lamMoThePhu nếu cần)
   2. #contact-form, sự kiện "submit":
         event.preventDefault();          // chặn tải lại trang
         xoaLoiCu();                      // gỡ hết .error và .error-msg cũ
         Kiểm tra 3 ô (dùng .value.trim()):
            #ten      rỗng                       -> "Vui lòng nhập họ tên."
            #email    không chứa "@" hoặc rỗng   -> "Email không hợp lệ."
            #loi-nhan ngắn hơn 10 ký tự          -> "Lời nhắn cần ít nhất 10 ký tự."
   3. Với mỗi ô sai:  o.classList.add("error")  và chèn ngay dưới nó một
      <p class="error-msg"> tạo bằng createElement.
   4. Không có lỗi -> hiện <p class="ok-msg">Đã gửi! Cảm ơn bạn.</p>

   PHẢI THẤY: bấm Gửi khi form rỗng -> 3 dòng đỏ, viền ô đỏ, trang
   KHÔNG tải lại. Bấm tiếp lần nữa -> vẫn đúng 3 dòng, không nhân đôi.
   Điền đủ và đúng -> lỗi biến mất, hiện dòng xanh.

   XONG SỚM:
   5. Sự kiện "input": gõ lại vào ô nào thì gỡ .error của ô đó.
   6. #theme-btn: document.body.classList.toggle("dark")
   ========================================================= */

// 1. Gắn sự kiện click cho 2 nút lọc kỹ năng
const btnAll = document.querySelector("#btn-all");
const btnExp = document.querySelector("#btn-exp");

if (btnAll) {
  btnAll.addEventListener("click", () => {
    veKyNang(skills);
    lamMoThePhu(2); // Giữ hiệu ứng làm mờ thẻ phụ
  });
}

if (btnExp) {
  btnExp.addEventListener("click", () => {
    const dsLoc = locTheoNam(skills, 2);
    veKyNang(dsLoc); // Chỉ vẽ các kỹ năng từ 2 năm trở lên (3 thẻ)
  });
}

// 2, 3, 4. Kiểm tra form liên hệ khi submit
const form = document.querySelector("#contact-form");

// Hàm gỡ bỏ tất cả thông báo lỗi và viền đỏ cũ
function xoaLoiCu() {
  if (!form) return;
  const cacOError = form.querySelectorAll(".error");
  cacOError.forEach(o => o.classList.remove("error"));

  const cacThongBao = form.querySelectorAll(".error-msg, .ok-msg");
  cacThongBao.forEach(tb => tb.remove());
}

if (form) {
  form.addEventListener("submit", function (event) {
    event.preventDefault(); // Chặn hành vi tải lại trang mặc định của form
    xoaLoiCu();             // Xóa lỗi cũ trước khi kiểm tra mới

    const oTen = document.querySelector("#ten");
    const oEmail = document.querySelector("#email");
    const oLoiNhan = document.querySelector("#loi-nhan");

    let coLoi = false;

    // Kiểm tra ô Tên: không được để rỗng
    if (!oTen.value.trim()) {
      coLoi = true;
      oTen.classList.add("error");
      const err = document.createElement("p");
      err.classList.add("error-msg");
      err.textContent = "Vui lòng nhập họ tên.";
      oTen.after(err);
    }

    // Kiểm tra ô Email: không được rỗng và phải chứa ký tự '@'
    const emailVal = oEmail.value.trim();
    if (!emailVal || !emailVal.includes("@")) {
      coLoi = true;
      oEmail.classList.add("error");
      const err = document.createElement("p");
      err.classList.add("error-msg");
      err.textContent = "Email không hợp lệ.";
      oEmail.after(err);
    }

    // Kiểm tra ô Lời nhắn: ít nhất 10 ký tự
    if (oLoiNhan.value.trim().length < 10) {
      coLoi = true;
      oLoiNhan.classList.add("error");
      const err = document.createElement("p");
      err.classList.add("error-msg");
      err.textContent = "Lời nhắn cần ít nhất 10 ký tự.";
      oLoiNhan.after(err);
    }

    // Nếu không có lỗi nào -> Hiển thị thông báo thành công
    if (!coLoi) {
      const ok = document.createElement("p");
      ok.classList.add("ok-msg");
      ok.textContent = "Đã gửi! Cảm ơn bạn.";
      form.appendChild(ok);
      form.reset(); // Xóa sạch nội dung đã nhập sau khi gửi thành công
    }
  });

  // 5. Phần xong sớm: Sự kiện "input" gõ đến đâu gỡ lỗi đến đó
  const cacInput = form.querySelectorAll("input, textarea");
  cacInput.forEach(input => {
    input.addEventListener("input", function () {
      this.classList.remove("error");
      if (this.nextElementSibling && this.nextElementSibling.classList.contains("error-msg")) {
        this.nextElementSibling.remove();
      }
    });
  });
}

// 6. Phần xong sớm: Nút đổi giao diện sáng / tối (Dark Mode)
const themeBtn = document.querySelector("#theme-btn");
if (themeBtn) {
  themeBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark");
  });
}
