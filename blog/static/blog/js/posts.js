console.log("posts.js loaded");

function getEditUrl(userId) {
  const editUrl = document.getElementById("urls").dataset.updateurl;
  console.log(editUrl); // "/users/12345/update/"
  return editUrl.replace("12345", userId);
}
function getDeleteUrl(userId) {
  const deleteUrl = document.getElementById("urls").dataset.deleteurl;
  console.log(deleteUrl); // "/users/12345/update/"
  return deleteUrl.replace("12345", userId);
}
// Initialize DataTable on document ready
$(document).ready(function () {
  new DataTable("#usersTable", {
    paging: false,
    scrollCollapse: true,
    scrollY: "50vh",
    ajax: {
      url: "/users/post/json/", // 👈 your endpoint for fetching data
      dataSrc: "data", // 👈 tells DataTables where to find the array
    },
    columns: [
      { data: "id" },
      { data: "username" },
      { data: "total_posts" },
      { data: "email" },
      { data: null }, // For action buttons
    ],
    columnDefs: [
      {
        target: 4,
        data: null,
        render: function (data, type, row) {
          return `
                    <div class="dropdown">
                        <button class="btn btn-sm btn-outline-primary dropdown-toggle" 
                                type="button" 
                                data-bs-toggle="dropdown" 
                                aria-expanded="false">
                    <i class="bi bi-three-dots"></i>
                    </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item edit-btn" data-id="${row.id}">Edit</a></li>
                            <li><a class="dropdown-item delete-btn" data-id="${row.id}">Delete</a></li>
                        </ul>
                    </div>`;
        },
      },
    ],
    responsive: true,
  });

  // Open modal and load form via AJAX
  $(document).on("click", ".edit-btn", function (e) {
    e.preventDefault();
    let userId = $(this).data("id");

    const editUrl = getEditUrl(userId);

    console.log(editUrl);
    $.ajax({
      url: `${editUrl}`, // Django view returning the form partial
      type: "GET",
      success: function (response) {
        console.log("Form loaded successfully");

        $(".edit-btn").blur(); // remove focus
        // Inject the form HTML into the modal body
        $("#editProfileModal .modal-body").html(response);
        $("#editProfileForm").attr("action", `/users/profile/${userId}/`);

        // Show the modal
        var modalEl = document.getElementById("editProfileModal");
        if (modalEl) {
          var modal = new bootstrap.Modal(modalEl);
          modal.show();
        } else {
          console.error("Modal element not found!");
        }
        $("#usersTable").DataTable().ajax.reload(null, false);
      },
      error: function () {
        alert("Error loading form");
        console.log("Error loading form");
      },
    });
  });

  $(document).on("click", ".delete-btn", function (e) {
    e.preventDefault();
    let userId = $(this).data("id");

    const deleteUrl = getDeleteUrl(userId);
    console.log(deleteUrl);
    $.ajax({
      url: `${deleteUrl}`,
      type: "get",
      success: function (response) {
        console.log("user deleted successfully" + response.redirect_url);
        window.location.href = response.redirect_url;
      },
      error: function (response) {
        window.location.href = response.redirect_url;
      },
    });
  });

  // Submit form via AJAX
  $(document).on("submit", "#editProfileForm", function (e) {
    e.preventDefault();
    let form = $(this);
    let formData = new FormData(this); // works for file uploads

    $.ajax({
      url: form.attr("action"),
      type: form.attr("method"),
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        $("#editProfileModal").modal("hide");
        // alert("Profile updated successfully!");
        $("#usersTable").DataTable().ajax.reload(null, false);
        // Optionally, refresh parts of the page
      },
      error: function (xhr) {
        // Show errors in modal
        $("#editProfileModalBody").html(xhr.responseText);
      },
    });
  });
});
