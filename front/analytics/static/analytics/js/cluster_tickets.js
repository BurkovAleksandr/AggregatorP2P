function clusterizationTickets() {
  const checked = document.querySelectorAll('input[type="checkbox"]:checked');
  const requiredFields = Array.from(checked).map((x) => x.value);
  const filters = JSON.parse(
    document.getElementById("filters-json").textContent
  );

  const jsonData = {
    required_fields: requiredFields,
    ...filters,
  };

  const token = getCookie("auth_token");
  const context = document.getElementById("context");
  const apiBaseUrl = context.dataset.apiBaseUrl;

  // 1. Отправляем запрос на кластеризацию
  fetch(`${apiBaseUrl}api/v1/tickets/clusterization_tickets`, {
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
        throw new Error(`Ошибка запуска задачи: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      const taskId = data.task_id;
      showNotification("info", "Кластеризация запущена. Ожидание...");
      // 2. Стартуем проверку статуса
      pollTaskStatus(taskId, apiBaseUrl, token);
    })
    .catch((error) => {
      console.error("Ошибка:", error);
      showNotification(
        "error",
        `Не удалось запустить задачу: ${error.message}`
      );
    });
}

function pollTaskStatus(taskId, apiBaseUrl, token, attempt = 0) {
  const maxAttempts = 30;
  const delay = 2000; // 2 секунды

  fetch(`${apiBaseUrl}api/v1/tickets/clusterization_result/${taskId}`, {
    method: "GET",
    credentials: "include",
    headers: {
      Authorization: `Token ${token}`,
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Ошибка при проверке статуса задачи");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      if (data.status === "done") {
        // 3. Скачиваем файл
        console.log(data);
        downloadReport(data.result);
      } else if (data.status === "failure") {
        showNotification("error", "Ошибка кластеризации.");
      } else {
        if (attempt < maxAttempts) {
          setTimeout(() => {
            pollTaskStatus(taskId, apiBaseUrl, token, attempt + 1);
          }, delay);
        } else {
          showNotification("error", "Время ожидания результата истекло.");
        }
      }
    })
    .catch((error) => {
      console.error("Ошибка при получении статуса:", error);
      showNotification("error", "Не удалось получить статус задачи.");
    });
}

function downloadReport(fileUrl) {
  const a = document.createElement("a");
  a.href = fileUrl;
  a.download = "tickets-clusterization.xlsx";
  document.body.appendChild(a);
  a.click();
  a.remove();
  showNotification("success", "Отчет сформирован и скачан");
}
