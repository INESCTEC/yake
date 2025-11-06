# pylint: skip-file
import yake

text = """
    Artificial Intelligence and Machine Learning are transforming the technology industry.
    Deep Learning algorithms have revolutionized computer vision and natural language processing.
    Neural networks with multiple hidden layers can learn complex patterns from large datasets.
    Companies like Google, Microsoft, and Amazon are investing heavily in AI research.
    The future of AI includes autonomous vehicles, intelligent assistants, and advanced robotics.
    """

kw = yake.KeywordExtractor(lan='en', n=4, top=10)
result = kw.extract_keywords(text)

print('res = [')
for k, s in result:
    print(f'    ("{k}", {s}),')
print(']')
