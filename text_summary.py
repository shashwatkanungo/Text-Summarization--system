import spacy
from spacy.lang.en.stop_words import STOP_WORDS 
from string import punctuation
from heapq import nlargest

text = """ A laser is a device that emits light through a process of optical amplification based on the stimulated emission of electromagnetic radiation. The word laser is an anacronym that originated as an acronym for light amplification by stimulated emission of radiation.The first laser was built in 1960 by Theodore Maiman at Hughes Research Laboratories, based on theoretical work by Charles H.
Townes and Arthur Leonard Schawlow. A laser differs from other sources of light in that it emits light that is coherent. Spatial coherence allows a laser to be focused to a tight spot, enabling applications such as laser cutting and lithography. 
It also allows a laser beam to stay narrow over great distances (collimation), a feature used in applications such as laser pointers and lidar (light detection and ranging).
Lasers can also have high temporal coherence, which permits them to emit light with a very narrow frequency spectrum. Alternatively, temporal coherence can be used to produce ultrashort pulses of light with a broad spectrum but durations as short as a femtosecond."""
 

def summarizer(rawdocs):
    stopwords =list(STOP_WORDS)
    #print(stopwords)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    #print(doc)

    tokens = [token.text for token in doc]
    #print(tokens)

    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    #print(word_freq)

    max_freq = max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    #print(word_freq)

    sent_token = [sent for sent in doc.sents]

    #print(sent_token)

    sent_scores = {}
    for sent in sent_token:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]
    #print(sent_scores)


    select_len = int(len(sent_token)* 0.3)
    #print(select_len)
    summary = nlargest(select_len , sent_scores, key = sent_scores.get)
    #print(summary)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    # print(text)
    # print(summary)
    # print("Length of original text", len(text.split(' ')))
    # print("Length of summary text", len(summary.split(' ')))

    return summary, doc , len(rawdocs.split(' ')), len(summary.split(' '))




