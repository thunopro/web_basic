const btnFetchPredictions = document.querySelector("#btnFetchPredictions");
const statusInfo = document.querySelector("#statusInfo");
const cardsContainer = document.querySelector("#cardsContainer");

function setStatus(text, className) {
    statusInfo.textContent = text;
    statusInfo.className = className;
}

function formatCurrencyVND(amount) {
    return new Intl.NumberFormat("vi-VN", {
        style: "currency",
        currency: "VND"
    }).format(amount);
}

async function loadPredictions() {
    setStatus("Đang tải dữ liệu dự đoán từ AI model...", "status-loading");
    btnFetchPredictions.disabled = true;
    cardsContainer.innerHTML = "";

    try {
        const response = await fetch("data.json");
        
        if (!response.ok) {
            throw new Error(`Không thể nạp dữ liệu! Status: ${response.status}`);
        }

        const predictions = await response.json();

        predictions.forEach((item) => {
            const card = document.createElement("div");
            card.className = "prediction-card";

            card.innerHTML = `
                <h3>${item.address}</h3>
                <div class="price-badge">${formatCurrencyVND(item.predicted_price_vnd)}</div>
                <div class="details">
                    <p>🛏️ <strong>Số phòng ngủ:</strong> ${item.bedrooms}</p>
                    <p>📐 <strong>Diện tích:</strong> ${item.area_sqm} m²</p>
                    <p>🎯 <strong>Độ tin cậy:</strong> ${(item.confidence * 100).toFixed(0)}%</p>
                </div>
            `;

            cardsContainer.appendChild(card);
        });

        setStatus(`Đã tải thành công ${predictions.length} mẫu dự đoán.`, "status-success");
    } catch (error) {
        console.error("Lỗi khi tải dự đoán:", error);
        setStatus(`Lỗi: ${error.message}`, "status-error");
    } finally {
        btnFetchPredictions.disabled = false;
    }
}

btnFetchPredictions.addEventListener("click", loadPredictions);

loadPredictions();
