function addPhotoUpload(ticketId) {
  const container = document.querySelector("#comment-container");

  // Не добавлять форму повторно
  if (document.querySelector("#photo-upload-form")) return;

  const form = document.createElement("div");
  form.id = "photo-upload-form";
  form.classList.add("photo-upload-form");

  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";
  input.multiple = true;
  input.classList.add("photo-input");

  const uploadBtn = document.createElement("button");
  uploadBtn.textContent = "Загрузить фото";
  uploadBtn.classList.add("photo-upload-btn");

  uploadBtn.addEventListener("click", () => {
    const files = input.files;
    if (!files.length) {
      showNotification("error", "Файлы не выбраны");
      return;
    }
    uploadPhotos(ticketId, files);
    form.remove();
  });

  form.appendChild(input);
  form.appendChild(uploadBtn);
  container.appendChild(form);
}

function uploadPhotos(ticketId, files) {
  const formData = new FormData();
  formData.append("report_id", ticketId);

  for (let i = 0; i < files.length; i++) {
    formData.append("attachments", files[i]);
  }

  const token = getCookie("auth_token");
  const context = document.getElementById("context");
  const apiBaseUrl = context.dataset.apiBaseUrl;

  fetch(`${apiBaseUrl}api/v1/report/add_report_attachment`, {
    method: "POST",
    credentials: "include",
    headers: {
      Authorization: `Token ${token}`,
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: formData,
  })
    .then((response) => {
      console.log("Reponse: ", response);
      if (response.ok) {
        showNotification("success", "Фотографии загружены");
      } else {
        showNotification("error", `Ошибка загрузки: ${error.message}`);
      }
    })
    .catch((error) => {
      console.error("Ошибка:", error);
      showNotification("error", `Ошибка загрузки: ${error.message}`);
    });
}
