from transformers import pipeline

generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')


def generate_phrase():
    context = "text"
    output = generator(context, max_length=50, do_sample=True, temperature=0.9)
    with open('dl.txt', 'w') as f:
        f.write(str(output))
