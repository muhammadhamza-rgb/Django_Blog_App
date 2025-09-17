"""Seed the database with random blog posts for existing users."""

import os
import random

import django
from faker import Faker

# setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.contrib.auth.models import User

from blog.models import Post

fake = Faker()

user_ids = [
    1,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
]

# Define 6 categories (adjust if using CharField)
category_names = [
    "Technology",
    "Health",
    "Travel",
    "Education",
    "Food",
    "Finance",
]

# Use category names directly since there's no Category model
categories = category_names


# def create_posts(num_posts=20):
#     for i in range(num_posts):
#         user_id = random.choice(user_ids)


def create_posts(num_posts=20):
    """
    Create random posts for existing users with random categories.
    """
    for _ in range(num_posts):
        user_id = random.choice(user_ids)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            print(f"User with id {user_id} does not exist. Skipping.")
            continue
        category = random.choice(categories)
        content = fake.text(max_nb_chars=800)  # ~100 words

        post = Post.objects.create(
            title=fake.sentence(nb_words=6),
            content=content,
            author=user,
            category=category,  # category is a CharField in Post
        )
        print(f"Created post: {post.title} by {user.username} in {category}")


create_posts(20)
