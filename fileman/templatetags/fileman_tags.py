from django import template
import random

register = template.Library()

#this templae filter will be used to render random gif images
@register.filter(name="random_image")
def random_im(text):
	images = ['https://media.tenor.com/images/8ad7e27c04f68d43526032f33100f0c1/tenor.gif','https://media.tenor.com/images/ad7078ec337dd55db7daf897be9374a7/tenor.gif','https://media.tenor.com/images/5a0f3d7fccaef7074ede52f373f53a8c/tenor.gif','https://media.tenor.com/images/08eac08b72efb26ca161fa1e2d8e652d/tenor.gif','https://media.tenor.com/images/dc1b24f72693a857af9553715fd73323/tenor.gif','https://media.tenor.com/images/b6d83d66859b0cf095ef81120ef98e1f/tenor.gif','https://media.tenor.com/images/c13ca5df3adc4f2bd28a97ca9f3af010/tenor.gif','https://media.tenor.com/images/4ded3e63cdeb091e55a9e91b1ceb2340/tenor.gif','https://media.tenor.com/images/c50a63221c9e5d63f3b06aba42b86539/tenor.gif','https://media.tenor.com/images/6a178d5ccbebbd44786ef5a6d59825b9/tenor.gif']
	return random.choice(images)


