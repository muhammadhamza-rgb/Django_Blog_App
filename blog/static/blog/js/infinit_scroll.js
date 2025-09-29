$(document).ready(function () {
  let page = 2; // first page already loaded
  let loading = false;
  let hasMore = true;

  const $scrollContainer = $(".flex-grow-1.overflow-auto");

  function loadMore() {
    if (loading || !hasMore) return;

    const scrollTop = $scrollContainer.scrollTop();
    const containerHeight = $scrollContainer.innerHeight();
    const scrollHeight = $scrollContainer[0].scrollHeight;

    // Only trigger when at the bottom
    if (scrollTop + containerHeight >= scrollHeight) {
      loading = true;
      $("#loading").show();

      $.ajax({
        url: "?page=" + page, // backend should return only 6 posts per page
        type: "get",
        dataType: "html",
        headers: { "X-Requested-With": "XMLHttpRequest" },
        success: function (data) {
          if (data.trim() === "") {
            hasMore = false; // stop if no posts
          } else {
            $("#post-container").append(data);
            page += 1;

            // 🔑 Force a tiny scroll up so we’re no longer at bottom
            // prevents auto-triggering again immediately
            $scrollContainer.scrollTop(scrollTop - 1);
          }
        },
        error: function () {
          console.error("Error loading posts");
        },
        complete: function () {
          loading = false;
          $("#loading").hide();
        },
      });
    }
  }

  $scrollContainer.on("scroll", function () {
    if (!loading) {
      loadMore();
    }
  });
});
