Aligning Docs
=============

The following are snapshots of new pages with potential Translation Memories.
There are many such documents available on the web.  We'll use the following
from Press Information Bureau of India.

* [English](https://pib.gov.in/PressReleseDetail.aspx?PRID=1700504)
* [Hindi](https://pib.gov.in/PressReleasePage.aspx?PRID=1700571)
* [Tamil](https://pib.gov.in/PressReleasePage.aspx?PRID=1700583)

We will use this library to align the sentences from one of these to the other,
through the API to demonstrate the application, walking through the internals
of what is happening. For the purpose of this walkthrough, we will assume the
text blobs from these articles before processing are already available to us.

We will need to obtain sentences first to align these. For this, we use the
Punkt Segmenters provided in this library.


## Setting up a commandline

```py
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--src', type=str, required=True)
parser.add_argument('--src-lang', type=str, required=True)
parser.add_argument('--tgt', type=str, required=True)
parser.add_argument('--tgt-lang', type=str, required=True)
args = parser.parse_args()
```

### Reading a blob from file

```py
def read_blob(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

src = read_blob(args.src)
tgt = read_blob(args.tgt)
```

### build function, to be used extensively

```py
from ilmulti.registry import build
```

## Gale-Church Algorithm

#### Building a splitter 

```py
splitter = build('splitter', 'punkt/pib')

src_sentences = splitter(src, lang=args.src_lang)
tgt_sentences = splitter(tgt, lang=args.tgt_lang)
```

#### Using a tokenizer

```py
tokenizer = build('tokenizer', 'sentencepiece/v1')

src_tokenized = tokenizer.map(src_sentences, lang=args.src_lang)
tgt_tokenized = tokenizer.map(tgt_sentences, lang=args.tgt_lang)
```

#### Applying BLEUAlign

```py
from ilmulti.align import BLEUAlign

src_as_lines = '\n'.join(src_tokenized)
tgt_as_lines = '\n'.join(tgt_tokenized)
src_aligned, tgt_aligned = BLEUAlign.withString(src_as_lines, tgt_as_lines)

src_aligned = tokenizer.inv_map(src_aligned)
tgt_aligned = tokenizer.inv_map(tgt_aligned)
```

```py
def check(src, tgt):
    for src_sample, tgt_sample in  zip(src, tgt):
        print("> ", src_sample)
        print("< ", tgt_sample)
    print('-'*10)
```


```py
check(src_aligned, tgt_aligned)
```

<details>
<summary> Output </summary>
<p>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">केन्द्रीय स्वास्थ्य एवं परिवार कल्याण मंत्री डॉ. हर्षवर्धन ने तपेदिक के खिलाफ समर्थन, संचार और सामाजिक एकजुटता (एसीएसएम) से संबंधित एक जनांदोलन शुरू करने के लिए केन्द्रीय स्वास्थ्य मंत्रालय के वरिष्ठ अधिकारियों और अन्य विकास भागीदारों के साथ एक उच्च स्तरीय बैठक की।</div> <div style="background:#DDD; padding: 2px;">Harsh Vardhan, Union Minister of Health and Family Welfare today chaired a high-level meeting with senior officials of the Union Health Ministry and other Development Partners to launch a Jan-Andolan against Tuberculosis involving Advocacy, Communication and Social Mobilization (ACSM).</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">शुरुआत में डॉ.हर्षवर्धन ने टीबी के खिलाफ लड़ाई में राष्ट्रीय तपेदिक उन्मूलन कार्यक्रम (एनटीईपी) के अंतर्गत भारत सरकार द्वारा उठाए गए कदमों पर प्रकाश डाला, जिन्हें सकारात्मक कदमों और संसाधनों दोनों की व्यापक प्रतिबद्धताओं के साथ समर्थन दिया गया था। केन्द्रीय मंत्री ने कहा, हम 2021 को तपेदिक वर्ष के रूप में मनाना चाहते हैं। इस क्रम में उन्होंने पिछले कुछ साल के दौरान टीबी के लिए सभी मरीजों का मुफ्त उपचार जहां वह उपचार कराना चाहते हों, उच्च गुणवत्ता की देखभाल सुनिश्चित किए जाने में व्यापक प्रगति का उल्लेख किया और उन्होंने विश्वासजताया कि इससे सेवाओं के लिए मांग में खासी बढ़ोतरी होगी, बीमारी के प्रति शर्म की भावना खत्म होगी और 2025 तक टीबी मुक्त भारत के लक्ष्य को हासिल करने में मदद मिलेगी।</div> <div style="background:#DDD; padding: 2px;">At the outset, Dr. Harsh Vardhan outlined the various steps taken by the Government of Indiaunder the National Tuberculosis Elimination Programme (NTEP) in combating the disease of TB which were backed by bold commitments of both affirmative action and resources.We wish to make 2021 the year of Tuberculosis, stated the Minister as he outlined the tremendous progress in ensuring all patients, irrespective of where they seek care, received free-of-cost, high quality TB care in the last few years and expressed his confidence that these gains would feed into creating greater demand for services, de-stigmatize the disease and help realize the goal of a TB-free India by 2025.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">बीमारी से ऐतिहासिक स्तर पर पार पाने के लिए नई रणनीतियों और टीबी मुक्त भारत के लक्ष्य को हासिल करने के लिए तप्तरता से व निरंतर ध्यान देने की जरूरत के महत्व को रेखांकित करते हुए केन्द्रीय मंत्री ने कहा, भले ही राष्ट्रीय तपेदिक उन्मूलन कार्यक्रम में टीबी प्रबंधन और सेवा आपूर्ति को और मजबूत बनाने के लिए प्रयास जारी हैं, लेकिन ऐसा तभी हो सकता है जब व्यापक जनसंख्या अपने समुदायों के भीतर जागरूकता के प्रसार, स्वास्थ्य अनुकूल व्यवहार को प्रोत्साहन के माध्यम से लोकतंत्र और जनांदोलन की भावना से काम करेगी। साथ ही टीबी के प्रति शर्म के भाव को दूर करने से इस बीमारी के खिलाफ आंदोलन को सफलता मिलेगी।उन्होंने तत्पतरता से अधिकतम आबादी तक पहुंच कायम करने और समुदायों की पूर्ण भागीदारी व सहयोग सुनिश्चित करने के महत्व पर प्रकाश डाला, साथ ही कहा कि टीबी के विभिन्न चरणों में समुदाय आधारित समूहों की प्रतिक्रिया उनके इस आंदोलन के प्रमुख स्तम्भों में से एक है।</div> <div style="background:#DDD; padding: 2px;">Underscoring the importance of newer approaches to tackle the disease holistically and the need for accelerated and sustained focus to achieve the target of a TB Free India,the Minister said, While the National Tuberculosis Elimination Programme continues to augment efforts to further strengthen TB management and service delivery, it is only when the wider population uses the essence of democracy and the spirit of Jan Andolan through generation of awareness, encouragement of health care seeking behaviour within their communities, and de-stigmatization of TB, would the movement against the disease be a success. He highlighted the importance of reaching maximum population quickly, ensuring full participation and cooperation of communities and community-based groups in various stages of TB response as the foundational pillars of his brainchild movement.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">कोविड-19 प्रबंधन में भारत को महामारी से निपटने में न सिर्फ कामयाबी मिली बल्कि भारत एक अगुआ के रूप में सामने आया है और समाधान, निदान और टीकों के लिए दुनिया भारत की ओर देख रही है।</div> <div style="background:#DDD; padding: 2px;">Drawing inspiration from lessons in COVID-19 management, whereIndia has not only successfully dealt with the pandemic, but emerged as a beacon of hopewith the world looking up to India for solutions, diagnostics, and vaccines, Dr.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">इससे मिली प्रेरणा के संबंध में डॉ. हर्षवर्धन ने कहा, महामारी के बाद एक फिर सटीक जानकारियों और उचित व्यवहार व स्वच्छता प्रक्रियाओं पर जोर और जागरूकता की भूमिका बढ़ गई है।</div> <div style="background:#DDD; padding: 2px;">Harsh Vardhan said, The pandemic has brought the focus back on the role of focused and rigorous messaging in creating an appetite for accurate information and appropriate behaviours and hygiene practices.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">इसी प्रकार, टीबी के लक्षणों पर राष्ट्रव्यापी संदेशों से सूचना का स्तर बढ़ सकता है और देश में टीबी के संक्रमण पर नियंत्रण से संबंधित सतर्कतापूर्ण व्यवहार पर जागरूकता पैदा की जा सकती है। उन्होंने पोलियो के खिलाफ जागरूकता के प्रसार में दिल्ली के स्वास्थ्य मंत्री के रूप में उनके द्वारा उठाए गए कदमों को याद दिलाया, जिसमें पड़ोस की केमिस्ट की दुकानों की भागीदारी शामिल थी।</div> <div style="background:#DDD; padding: 2px;">Similar nation-wide messaging on TB symptoms can drive notification levels up and build awareness on the precautionary behaviour related to control of TB infection in the country. He recollected steps taken by him as Delhis Health Minister in generating awareness against Polio which involved the participation of neighbourhood chemist shops.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">उन्होंने नेशनल टेक्निकल सपोर्ट यूनिट (एनटीएसयू) पर हुई बैठक की अध्यक्षता की, जिसमें राष्ट्रीय स्तर पर और राज्यों में भारत सरकार के प्रयासों के समर्थन में विकास भागीदारों के साथ सहयोग काम करने का प्रस्ताव किया, जिससे टीबी कार्यक्रम के तहत उपलब्ध सेवाओं से जुड़ी मांग पैदा करने और जागरूकता के प्रसार के लिए विभिन्न समर्थक और संचार रणनीतियों को लागू करके जमीनी स्तर पर कार्यक्रम को मजबूती देने में मदद मिलेगी।</div> <div style="background:#DDD; padding: 2px;">He chaired deliberations on a National Technical Support Unit (NTSU) that is proposed to be set up in collaboration with development partners to support the Government of Indias efforts, both nationally and in states, to help strengthen on-ground program delivery by employing various advocacy and communications approaches to generate demand and create awareness on the services available under the TB program.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">टीबी कार्यक्रम के साथ काम कर रहे विकास भागीदारों ने इस अवसर पर पिछले कुछ साल केदौरान किए गए अपने कार्य के प्रभाव के बारे में बताया और प्रस्तावित जनांदोलन अभियान को समर्थन देने की अपनी योजनाएं साझा कीं।</div> <div style="background:#DDD; padding: 2px;">Development partners working with the TB program attending the eventcommunicated the impact of their work in the past few years and shared their plans to support the proposed Jan Andolan movement.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">केन्द्रीय स्वास्थ्य सचिव श्री राजेश भूषण, अतिरिक्त सचिव (स्वास्थ्य) श्रीमती आरती आहूजा, डीजीएचएस डॉ.</div> <div style="background:#DDD; padding: 2px;">Shri Rajesh Bhushan, Union Health Secretary, Smt. Arti Ahuja, Addl.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">सुनील कुमार और मंत्रालय के अन्य वरिष्ठ अधिकारी इस अवसर पर उपस्थित रहे।</div> <div style="background:#DDD; padding: 2px;">Secretary (Health), Dr. Sunil Kumar, DGHS and other senior officials of the Ministry were present.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">इस कार्यक्रम में डब्ल्यूएचओ के भारत में कंट्री रिप्रेजेंटेटिव डॉ. रोडेरिको ऑफ्रिन और बीएमजीएफ और यूएसएआईडी जैसे विकास भागीदारों के प्रतिनिधि भी उपस्थित रहे।</div> <div style="background:#DDD; padding: 2px;">Dr. Roderico Ofrin, Country Representative, India (WHO)and representatives of Development Partners like BMGF and USAID were also present at the event.</div></div>
</p>

</details>

## BLEUAligner: Using translation

```py
from ilmulti.align import BLEUAligner
translator = build('e2e_translator', 'm2en4')
aligner = BLEUAligner.fromE2ETranslator(translator)
src_aligned, tgt_aligned = aligner.align_forward(src, args.src_lang, tgt, args.tgt_lang)
```

```py
check(src_aligned, tgt_aligned)
```

<details>
<summary> Output </summary>
<p>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;">

<div style="background:#EEE; padding: 2px;">शुरुआत में डॉ.हर्षवर्धन ने टीबी के खिलाफ लड़ाई में राष्ट्रीय तपेदिक उन्मूलन कार्यक्रम (एनटीईपी) के अंतर्गत भारत सरकार द्वारा उठाए गए कदमों पर प्रकाश डाला, जिन्हें सकारात्मक कदमों और संसाधनों दोनों की व्यापक प्रतिबद्धताओं के साथ समर्थन दिया गया था। केन्द्रीय मंत्री ने कहा, हम 2021 को तपेदिक वर्ष के रूप में मनाना चाहते हैं। इस क्रम में उन्होंने पिछले कुछ साल के दौरान टीबी के लिए सभी मरीजों का मुफ्त उपचार जहां वह उपचार कराना चाहते हों, उच्च गुणवत्ता की देखभाल सुनिश्चित किए जाने में व्यापक प्रगति का उल्लेख किया और उन्होंने विश्वासजताया कि इससे सेवाओं के लिए मांग में खासी बढ़ोतरी होगी, बीमारी के प्रति शर्म की भावना खत्म होगी और 2025 तक टीबी मुक्त भारत के लक्ष्य को हासिल करने में मदद मिलेगी।</div> <div style="background:#DDD; padding: 2px;">Underscoring the importance of newer approaches to tackle the disease holistically and the need for accelerated and sustained focus to achieve the target of a TB Free India,the Minister said, While the National Tuberculosis Elimination Programme continues to augment efforts to further strengthen TB management and service delivery, it is only when the wider population uses the essence of democracy and the spirit of Jan Andolan through generation of awareness, encouragement of health care seeking behaviour within their communities, and de-stigmatization of TB, would the movement against the disease be a success. He highlighted the importance of reaching maximum population quickly, ensuring full participation and cooperation of communities and community-based groups in various stages of TB response as the foundational pillars of his brainchild movement.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">साथ ही टीबी के प्रति शर्म के भाव को दूर करने से इस बीमारी के खिलाफ आंदोलन को सफलता मिलेगी।उन्होंने तत्पतरता से अधिकतम आबादी तक पहुंच कायम करने और समुदायों की पूर्ण भागीदारी व सहयोग सुनिश्चित करने के महत्व पर प्रकाश डाला, साथ ही कहा कि टीबी के विभिन्न चरणों में समुदाय आधारित समूहों की प्रतिक्रिया उनके इस आंदोलन के प्रमुख स्तम्भों में से एक है।</div> <div style="background:#DDD; padding: 2px;">Drawing inspiration from lessons in COVID-19 management, whereIndia has not only successfully dealt with the pandemic, but emerged as a beacon of hopewith the world looking up to India for solutions, diagnostics, and vaccines, Dr.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">कोविड-19 प्रबंधन में भारत को महामारी से निपटने में न सिर्फ कामयाबी मिली बल्कि भारत एक अगुआ के रूप में सामने आया है और समाधान, निदान और टीकों के लिए दुनिया भारत की ओर देख रही है। इससे मिली प्रेरणा के संबंध में डॉ.</div> <div style="background:#DDD; padding: 2px;">Harsh Vardhan said, The pandemic has brought the focus back on the role of focused and rigorous messaging in creating an appetite for accurate information and appropriate behaviours and hygiene practices.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">हर्षवर्धन ने कहा, महामारी के बाद एक फिर सटीक जानकारियों और उचित व्यवहार व स्वच्छता प्रक्रियाओं पर जोर और जागरूकता की भूमिका बढ़ गई है। इसी प्रकार, टीबी के लक्षणों पर राष्ट्रव्यापी संदेशों से सूचना का स्तर बढ़ सकता है और देश में टीबी के संक्रमण पर नियंत्रण से संबंधित सतर्कतापूर्ण व्यवहार पर जागरूकता पैदा की जा सकती है। उन्होंने पोलियो के खिलाफ जागरूकता के प्रसार में दिल्ली के स्वास्थ्य मंत्री के रूप में उनके द्वारा उठाए गए कदमों को याद दिलाया, जिसमें पड़ोस की केमिस्ट की दुकानों की भागीदारी शामिल थी।</div> <div style="background:#DDD; padding: 2px;">Similar nation-wide messaging on TB symptoms can drive notification levels up and build awareness on the precautionary behaviour related to control of TB infection in the country. He recollected steps taken by him as Delhis Health Minister in generating awareness against Polio which involved the participation of neighbourhood chemist shops.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">उन्होंने नेशनल टेक्निकल सपोर्ट यूनिट (एनटीएसयू) पर हुई बैठक की अध्यक्षता की, जिसमें राष्ट्रीय स्तर पर और राज्यों में भारत सरकार के प्रयासों के समर्थन में विकास भागीदारों के साथ सहयोग काम करने का प्रस्ताव किया, जिससे टीबी कार्यक्रम के तहत उपलब्ध सेवाओं से जुड़ी मांग पैदा करने और जागरूकता के प्रसार के लिए विभिन्न समर्थक और संचार रणनीतियों को लागू करके जमीनी स्तर पर कार्यक्रम को मजबूती देने में मदद मिलेगी।</div> <div style="background:#DDD; padding: 2px;">He chaired deliberations on a National Technical Support Unit (NTSU) that is proposed to be set up in collaboration with development partners to support the Government of Indias efforts, both nationally and in states, to help strengthen on-ground program delivery by employing various advocacy and communications approaches to generate demand and create awareness on the services available under the TB program.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">टीबी कार्यक्रम के साथ काम कर रहे विकास भागीदारों ने इस अवसर पर पिछले कुछ साल केदौरान किए गए अपने कार्य के प्रभाव के बारे में बताया और प्रस्तावित जनांदोलन अभियान को समर्थन देने की अपनी योजनाएं साझा कीं।</div> <div style="background:#DDD; padding: 2px;">Development partners working with the TB program attending the eventcommunicated the impact of their work in the past few years and shared their plans to support the proposed Jan Andolan movement. Shri Rajesh Bhushan, Union Health Secretary, Smt.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">केन्द्रीय स्वास्थ्य सचिव श्री राजेश भूषण, अतिरिक्त सचिव (स्वास्थ्य) श्रीमती आरती आहूजा, डीजीएचएस डॉ.</div> <div style="background:#DDD; padding: 2px;">Secretary (Health), Dr.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">सुनील कुमार और मंत्रालय के अन्य वरिष्ठ अधिकारी इस अवसर पर उपस्थित रहे।</div> <div style="background:#DDD; padding: 2px;">Sunil Kumar, DGHS and other senior officials of the Ministry were present.</div></div>
<div style="margin: 1em; border: 1px dotted #ccc; border-left: 2px solid #ccc;"><div style="background:#EEE; padding: 2px;">इस कार्यक्रम में डब्ल्यूएचओ के भारत में कंट्री रिप्रेजेंटेटिव डॉ. रोडेरिको ऑफ्रिन और बीएमजीएफ और यूएसएआईडी जैसे विकास भागीदारों के प्रतिनिधि भी उपस्थित रहे।</div> <div style="background:#DDD; padding: 2px;">Dr. Roderico Ofrin, Country Representative, India (WHO)and representatives of Development Partners like BMGF and USAID were also present at the event.</div></div>

</p>
</details>




