import sys
sys.path.insert(0, '.')

from ilmulti.translator.pretrained import from_pretrained
from argparse import ArgumentParser
from pprint import pprint

model = from_pretrained('mm-all-iter0')

def test(sample, language):
    result = model(sample, tgt_lang=language)
    pprint(result)
    
samples = [
    "Hello World!",
    "For older Python versions (< 2.7), you can use this receipe to get the Counter class.",
    "This solution is really elegant, but currently, the other one worked for me.",
    "UP के राज्यपाल राम नाइक ने CM की सिफारिश मानी, ओमप्रकाश राजभर को राज्य मंत्रिमंडल से किया बर्खास्त",
    "JEE Advanced Admit Card 2019: कुछ ही देर में जारी होगा एडमिट कार्ड, jeeadv.ac.in से यूं कर पाएंगे डाउनलोड",
]

for sample in samples:
    for lang in ["hi", "ml", "ta", "te", "ur", "bn", "en"]:
        test(sample, lang)
