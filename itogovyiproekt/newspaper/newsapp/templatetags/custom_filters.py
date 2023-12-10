from django import template

register = template.Library()

bad_words = ['редиска', 'дурак', 'идиот']


@register.filter()
def censor(sentence):
    text = sentence.split()
    for i, word in enumerate(text):
        if word in bad_words:
            text[i] = word[0] + '***'
    return ' '.join(text)
