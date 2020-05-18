from django import template
import random

register = template.Library()


@register.filter(name="random_image")
def random_im(text):
    images = ['https://media.tenor.com/images/8ad7e27c04f68d43526032f33100f0c1/tenor.gif','https://media.tenor.com/images/ad7078ec337dd55db7daf897be9374a7/tenor.gif','https://media.tenor.com/images/5a0f3d7fccaef7074ede52f373f53a8c/tenor.gif','https://media.tenor.com/images/7e4e64f8fc396bf2420cc7afd2f26574/tenor.gif','https://media.tenor.com/images/1db08eb5865f1f857ec490a57e48c362/tenor.gif','https://media.tenor.com/images/6050fd1e362cdab73f6e7d73b4fb0cf6/tenor.gif','https://media.tenor.com/images/c22f4bc14d0bb9cbfe98b7b7c8ff3f10/tenor.gif','https://media.tenor.com/images/6b447bebe84fe53cf8ceae90578f4870/tenor.gif','https://media.tenor.com/images/6c2400daaf6da50021a943331f2891f1/tenor.gif','https://media.tenor.com/images/9a71139f4991d06dcc150d033c63d3ab/tenor.gif']
    return random.choice(images)

