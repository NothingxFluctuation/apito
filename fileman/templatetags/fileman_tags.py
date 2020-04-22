from django import template
import random

register = template.Library()


@register.filter(name="random_image")
def random_im(text):
    images = ['https://media.tenor.com/images/246201afa588d1b25d773b3611e1df28/tenor.gif','https://media.tenor.com/images/2b52390ecac95322516dd74c11ff57ff/tenor.gif','https://media.tenor.com/images/b3c3571d7fd00e3fca22dce6e21d590b/tenor.gif','https://media.tenor.com/images/bff89595f10f1b07608dbe71ca67e75e/tenor.gif','https://media.tenor.com/images/b7aa76b4a9fb5ef1d3cf5ef2bf1f2e6e/tenor.gif','https://media.tenor.com/images/48914d4d1626cd4b8c38ae9613f6af3e/tenor.gif','https://media.tenor.com/images/88719414bb5559454a796537a7bfd7ae/tenor.gif','https://media.tenor.com/images/d548083fa12da06c632e0fed697bb91d/tenor.gif','https://media.tenor.com/images/a5747f7b1d84287ca4a62e8a428d51ae/tenor.gif','https://media.tenor.com/images/e77ee8bfeb9b2de9104b7a38b160ec18/tenor.gif']
    return random.choice(images)

