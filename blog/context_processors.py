from .models import Post


def categories_context(request):
    categories = (
        Post.objects.values_list("category", flat=True)
        .exclude(category__isnull=True)  # remove NULL
        .exclude(category__exact="")  # remove empty string
        .distinct()
    )
    return {"categories": categories}
