from django import template
import random

register = template.Library()


@register.filter(name="random_image")
def random_im(text):
    images = ['https://media.tenor.com/images/246201afa588d1b25d773b3611e1df28/tenor.gif','https://media.tenor.com/images/2b52390ecac95322516dd74c11ff57ff/tenor.gif','https://i.gifer.com/3QeQ.gif']
    return random.choice(images)