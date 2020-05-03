from flask import Flask, render_template, redirect, request
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
nlp = spacy.load("en_core_web_sm")
app= Flask(__name__)


def text_summarizer(raw_docx,max_lines):
    raw_text = raw_docx
    docx = nlp(raw_text)
    print(docx)
    stopwords = list(STOP_WORDS)
    # Build Word Frequency
    # word.text is tokenization in spacy
    word_frequencies = {}
    for word in docx:
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)
    # Sentence Tokens
    sentence_list = [sentence for sentence in docx.sents]

    # Calculate Sentence Score and Ranking
    sentence_scores = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Find N Largest
    summary_sentences = nlargest(max_lines, sentence_scores, key=sentence_scores.get)
    final_sentences = [w.text for w in summary_sentences]
    summary = ' '.join(final_sentences)
    #print('\n\nSummarized Document\n')
    #print(summary)
    #print("Total Length:", len(summary))
    return summary
def reading_time(summary):
    total_words_tokens = [token.text for token in nlp(summary)]
    estimatedtime = len(total_words_tokens) / 200

    return estimatedtime

@app.route("/")
def hello():
    return render_template("in.html")
@app.route("/",methods=['POST'])
def summar():
    if request.method =='POST':
        content=request.form['message']
        line=int(request.form['max'])

        final=text_summarizer(content,line)

    return render_template("in.html", your_final= final,time=reading_time(final))


if __name__=='__main__':
    app.run(debug=True)
