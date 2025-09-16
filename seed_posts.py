import os
import random

import django

# setup Django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "project.settings"
)  # change project to your project name
django.setup()

from django.contrib.auth.models import User
from faker import Faker

from blog.models import Post

fake = Faker()

# user IDs you want to assign posts to
user_ids = [22]


def create_posts(num_posts=20):
    for i in range(num_posts):
        user_id = random.choice(user_ids)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            print(f"User with id {user_id} does not exist. Skipping.")
            continue

        post = Post.objects.create(
            title=fake.sentence(nb_words=6),  # random title with ~6 words
            content=fake.text(max_nb_chars=200),  # ~30 words
            author=user,
        )
        print(f"Created post: {post.title} by {user.username}")


if __name__ == "__main__":
    create_posts(20)
