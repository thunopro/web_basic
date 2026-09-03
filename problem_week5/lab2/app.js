const API_URL = "https://jsonplaceholder.typicode.com/users";
const btnLoad = document.querySelector("#btnLoad");
const btnErase = document.querySelector("#btnErase");
const statusMessage = document.querySelector("#statusMessage");
const tbody = document.querySelector("#user-table tbody");

function eraseUsers() {
    tbody.innerHTML = "";
    setStatus("Danh sách đã được xóa.", "status-info");
}

function setStatus(text, className) {
    statusMessage.textContent = text;
    statusMessage.className = `status ${className}`;
}

async function loadUsers() {
    setStatus("Đang tải dữ liệu...", "status-loading");
    btnLoad.disabled = true;

    tbody.innerHTML = "";

    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const users = await response.json();

        users.forEach((user) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${user.id}</td>
                <td><strong>${user.name}</strong></td>
                <td>${user.email}</td>
                <td>${user.address ? user.address.city : "N/A"}</td>
                <td>${user.company ? user.company.name : "N/A"}</td>
            `;

            tbody.appendChild(row);
        });

        setStatus(`Đã tải thành công ${users.length} người dùng!`, "status-success");
    } catch (error) {
        console.error("Lỗi khi tải người dùng:", error);
        setStatus(`Thất bại: ${error.message}`, "status-error");
    } finally {
        btnLoad.disabled = false;
    }
}

btnLoad.addEventListener("click", loadUsers);
btnErase.addEventListener("click", eraseUsers);

loadUsers();
