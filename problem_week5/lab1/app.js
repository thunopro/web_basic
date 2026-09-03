function fakeFetchData(delay = 1500) {
    return new Promise((resolve, reject) => {
        const isSuccess = true;

        setTimeout(() => {
            if (isSuccess) {
                const sampleData = {
                    id: 101,
                    task: "House Price Prediction",
                    price: 450000,
                    status: "Completed"
                };
                resolve(sampleData);
            } else {
                reject(new Error("Lỗi kết nối mạng: Không thể tải dữ liệu."));
            }
        }, delay);
    });
}

function runWithThen() {
    console.log("[.then] Bắt đầu gọi fakeFetchData()...");
    const outputDiv = document.querySelector("#output");
    outputDiv.textContent = "[.then] Đang tải dữ liệu...";

    fakeFetchData(1500)
        .then((data) => {
            console.log("[.then] Nhận dữ liệu thành công:", data);
            outputDiv.textContent = `[.then] Dữ liệu: ${JSON.stringify(data, null, 2)}`;
        })
        .catch((error) => {
            console.error("[.then] Gặp lỗi:", error);
            outputDiv.textContent = `[.then] Lỗi: ${error.message}`;
        });
}

async function runWithAsyncAwait() {
    console.log("[async/await] Bắt đầu gọi fakeFetchData()...");
    const outputDiv = document.querySelector("#output");
    outputDiv.textContent = "[async/await] Đang tải dữ liệu...";

    try {
        const data = await fakeFetchData(1500);
        console.log("[async/await] Nhận dữ liệu thành công:", data);
        outputDiv.textContent = `[async/await] Dữ liệu: ${JSON.stringify(data, null, 2)}`;
    } catch (error) {
        console.error("[async/await] Gặp lỗi:", error);
        outputDiv.textContent = `[async/await] Lỗi: ${error.message}`;
    }
}

document.querySelector("#btnThen").addEventListener("click", runWithThen);
document.querySelector("#btnAsync").addEventListener("click", runWithAsyncAwait);

console.log("=== Lab 1: Promise Basics loaded ===");
runWithThen();
setTimeout(() => {
    runWithAsyncAwait();
}, 2000);
