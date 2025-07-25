function getCheckedSubdivisions() {
  const checkedValues = Array.from(
    document.querySelectorAll('input[name="subdivisions"]:checked')
  ).map((input) => input.value);
  console.log(checkedValues);
  return checkedValues;
}
// Получаем элементы
const create_ticket_btn = document.querySelector("#create-ticket-btn");
const form = document.querySelector("#create-ticket-form");
// const notificationContainer = document.querySelector("#notification-container");

create_ticket_btn.addEventListener("click", createTicketPost);

function createTicketPost(event) {
  event.preventDefault(); // отменяем нативную отправку формы

  // Собираем данные формы в объект
  const formData = new FormData(form);
  const jsonData = {};
  formData.forEach((value, key) => {
    jsonData[key] = value;
  });
  jsonData["subdivisions"] = getCheckedSubdivisions();
  const token = getCookie("auth_token");
  const context = document.getElementById("context");
  const apiBaseUrl = context.dataset.apiBaseUrl;
  console.log(`${apiBaseUrl}api/v1/tickets/create_ticket`);
  fetch(`${apiBaseUrl}api/v1/tickets/create_ticket`, {
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
      return response.json();
    })
    .then((data) => {
      showNotification("success", "Заявка успешно создана!");
    })
    .catch((error) => {
      console.error("Ошибка:", error);
      showNotification("error", `Не удалось создать заявку: ${error.message}`);
    });
}
