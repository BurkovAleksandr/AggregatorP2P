function generateReport() {
  const checked = document.querySelectorAll('input[type="checkbox"]:checked');
  const requiredFields = Array.from(checked).map((x) => x.value);
  const filters = JSON.parse(
    document.getElementById("filters-json").textContent
  );
  // const filters = JSON.parse(document.getElementById("filters-json").textContent);
  jsonData = {
    required_fields: requiredFields,
    ...filters,
  };
  console.log(jsonData);
  const token = getCookie("auth_token");
  const context = document.getElementById("context");
  const apiBaseUrl = context.dataset.apiBaseUrl;
  fetch(`${apiBaseUrl}api/v1/tickets/generate_report`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(jsonData),
  })
    .then((response) => {
      if (!response.ok) {
        return response
          .json()
          .then((errData) => {
            const msg = errData.detail || JSON.stringify(errData);
            throw new Error(msg);
          })
          .catch(() => {
            throw new Error("Ошибка HTTP: " + response.status);
          });
      }
      return response.blob();
    })
    .then((blob) => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "tickets-report.xlsx"; // имя файла
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      showNotification("success", "Отчет сформирован и скачан");
    })
    .catch((error) => {
      console.error("Ошибка:", error);
      showNotification(
        "error",
        `Не удалось сформировать отчет: ${error.message}`
      );
    });
}
