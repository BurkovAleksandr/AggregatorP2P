function acceptTicket(ticketId) {
  const token = getCookie("auth_token");
  const jsonData = {
    status: "Received",
    ticket_id: ticketId,
  };
  const context = document.getElementById("context");
  const apiBaseUrl = context.dataset.apiBaseUrl;
  fetch(`${apiBaseUrl}api/v1/tickets/change_status`, {
    method: "PATCH",
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
      showNotification("success", "Заявка принята");
    })
    .catch((error) => {
      console.error("Ошибка:", error);
      showNotification("error", `Не удалось принять заявку: ${error.message}`);
    });
}
