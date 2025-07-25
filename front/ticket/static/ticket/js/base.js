const notificationContainer = document.querySelector("#notification-container");
function showNotification(type, message) {
  const notif = document.createElement("div");
  notif.classList.add("notification", type);
  notif.textContent = message;

  notificationContainer.appendChild(notif);
  requestAnimationFrame(() => {
    notif.classList.add("show");
  });

  setTimeout(() => {
    notif.classList.remove("show");
    notif.classList.add("hide");
    notif.addEventListener(
      "transitionend",
      () => {
        notif.remove();
        // if (type != "error") {
        //   // window.location.href = "/tickets/";
        // }
      },
      {
        once: true,
      }
    );
  }, 3000);
}

function getCookie(name) {
  const cookieStr = `; ${document.cookie}`;
  const parts = cookieStr.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";")[0];
}
