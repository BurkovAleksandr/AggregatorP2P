function expandFiltersContainer() {
  const filters = document.getElementById("filtersContainer");
  filters.classList.toggle("hidden");
}

// Формируем ссылку при наведении/клике
document.addEventListener("DOMContentLoaded", function () {
  const applyLink = document.getElementById("applyFiltersLink");

  applyLink.addEventListener("click", function (event) {
    const dateFrom = document.getElementById("filterDateFrom").value;
    const dateTo = document.getElementById("filterDateTo").value;
    const subdivisionSelect = document.getElementById("filterSubdivision");
    const status = document.getElementById("filterStatus").value;
    const page_size = document.getElementById("pageSize").value;

    const selectedSubdivisions = Array.from(
      subdivisionSelect.selectedOptions
    ).map((option) => option.value);

    const params = new URLSearchParams();
    if (dateFrom) params.append("created_after", dateFrom);
    if (dateTo) params.append("created_before", dateTo);
    if (status) params.append("status", status);
    if (page_size) params.append("page_size", page_size);
    selectedSubdivisions.forEach((value) => {
      params.append("subdivisions", value);
    });

    const baseUrl = "reports";
    applyLink.href = `${baseUrl}?${params.toString()}`;
  });
});
