function addComment(ticketId) {
  const commentContainer = document.querySelector("#comment-container");

  // Не создавать вторую форму
  if (document.querySelector("#comment-form")) return;

  const commentForm = document.createElement("div");
  commentForm.id = "comment-form";
  commentForm.classList.add("comment-form");

  const input = document.createElement("textarea");
  input.placeholder = "Введите комментарий";
  input.classList.add("comment-input");

  const sendButton = document.createElement("button");
  sendButton.textContent = "Отправить";
  sendButton.classList.add("comment-submit-btn");

  sendButton.addEventListener("click", () => {
    const value = input.value.trim();
    if (value) {
      console.log("Комментарий:", value);
      sendComment(value, ticketId); // ✅ передаём аргументы правильно
    }
    commentForm.remove(); // Удалить форму
  });

  commentForm.appendChild(input);
  commentForm.appendChild(sendButton);
  commentContainer.appendChild(commentForm);
}

function sendComment(text, ticketId) {
  const token = getCookie("auth_token");
  const jsonData = {
    comment_text: text,
    ticket_id: ticketId,
  };
  const context = document.getElementById("context");
  const apiBaseUrl = context.dataset.apiBaseUrl;
  console.log(jsonData);
  fetch(`${apiBaseUrl}api/v1/tickets/set_comment`, {
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
      showNotification("success", "Комментарий отправлен");
    })
    .catch((error) => {
      console.error("Ошибка:", error);
      showNotification(
        "error",
        `Не удалось создать комментарий: ${error.message}`
      );
    });
}
