// console.log("scroll file activated");
// $(document).ready(function () {
//   let page = 2; // page 1 already loaded
//   let loading = false;

//   $(window).scroll(function () {
//     if (loading) return;

//     if (
//       $(window).scrollTop() + $(window).height() >=
//       $(document).height() - 200
//     ) {
//       loading = true;
//       $("#loading").show();

//       $.ajax({
//         url: "?page=" + page,
//         type: "get",
//         dataType: "html",
//         headers: { "X-Requested-With": "XMLHttpRequest" },
//         success: function (data) {
//           if (data.trim() === "") {
//             $(window).off("scroll"); // no more pages
//             $("#loading").hide();
//           } else {
//             $("#post-container").append(data);
//             page += 1;
//             loading = false;
//             $("#loading").hide();
//           }
//         },
//         error: function () {
//           console.error("Error loading posts");
//           loading = false;
//           $("#loading").hide();
//         },
//       });
//     }
//   });
// });

$(document).ready(function () {
  let page = 2; // first page already loaded
  let loading = false;

  // Attach scroll event to your scrollable div
  const $scrollContainer = $(".flex-grow-1.overflow-auto");

  $scrollContainer.on("scroll", function () {
    if (loading) return;

    const scrollTop = $scrollContainer.scrollTop();
    const containerHeight = $scrollContainer.innerHeight();
    const scrollHeight = $scrollContainer[0].scrollHeight;

    // Trigger when user scrolls near bottom
    if (scrollTop + containerHeight >= scrollHeight - 200) {
      loading = true;
      $("#loading").show();

      $.ajax({
        url: "?page=" + page,
        type: "get",
        dataType: "html",
        headers: { "X-Requested-With": "XMLHttpRequest" },
        success: function (data) {
          if (data.trim() === "") {
            // No more posts
            $("#loading").hide();
            loading = false;
          } else {
            $("#post-container").append(data);
            page += 1;
            loading = false;
            $("#loading").hide();
          }
        },
        error: function () {
          console.error("Error loading posts");
          loading = false;
          $("#loading").hide();
        },
      });
    }
  });
});
