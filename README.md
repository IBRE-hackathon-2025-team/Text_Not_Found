# Text Not Found ...

Here we present a work analyzing the authorship of books by a very productive writer and private detective enthusiast. She is writing books for 26 years, for now there are 381 finished books, which means that on average she writing around 15! books per year or 1.2 in one month... It is suspicious, is not it? Some people believe that this writer's pugs (small dogs) help her write her books.

[место для статистики по книгам сам знаешь кого]

So we decided to analyse the authorship of these books to shed light on this mystery and to ensure that our work is not only entertaining, we plan to consider applying similar analysis in other areas.  We do not claim 100% truth in our conclusions and our analysis is not final. However, you can follow us on the path to solving this riddle. Let's go!

## Data description

- 341 books of the author of interest
- [ сколько-то других детективов ]
- 5 generated texts
- 5 interviews
- 2 fanfics
- And 6 pugs (ok, it is just a joke; 6 funny and positive people)

## Required packages

1) Stylo (in R), standart pipeline

2) Spacy (library for advanced Natural Language Processing - NLP), for preprocessing

```bash
conda install -c conda-forge spacy
python -m spacy download ru_core_news_sm # download russian language model
```

3) [Библиотеки для dimentionality reduction]

4) [Библиотеки для topology]

5) [Библиотеки для k-mer]

## Data preparation

1) Books can be downloaded in different formats, however for our analysis we decided to use .txt format, so we wrote convertor for .fb2 files, which you can see in [название файла]

2) We wanted to test different methods and ways of text preprocessing, so we tried several approaches, notebook can be found in file [название файла]:
- original text
- text, where words were reduced to lemmas (бегал → бегать, бежит → бегать; слону → слон, слона → слон)
- text, where words were reduced to lemmas, all punctuation and stop words were removed from text (*stop words - the most common words of the language)
- text, where words were reduced to the parts of speech (слон → NOUN, бегать → VERB, огромный → ADJ), all punctuation and stop words were removed from text
- text, where words were reduced to the parts of speech. Them parts of speech were encoded as one-letter:
(a) ADJ-adjective 
(b) ADP-adposition 
(c) ADV-adverb
(d) AUX-auxiliary verb 
(e) CCONJ-coordinating conjunction 
(f) DET-determiner 
(g) INTJ-interjection 
(h) NOUN-noun, PROPN-proper noun
(i) NUM-numeral 
(j) PART-particle
(k) PRON-pronoun
(m) SCONJ-subordinating conjunction
(n) SYM-symbol
(o) VERB-verb
(p) X-other

## Analysis

1) Classical method which is used in stulometry is stylo R package. [добавить описание этого пакета]. [Добавить описание результатов и картинки]

[example of the frequency table]

2) Dimentionality reduction based on table with frequences of words. These frequencies are obtained from the stylo package

- PCA
- tSNE

3) Topological analysis

The basic idea of the analysis is the following: we obtain frequency of each word/part_of_speech in the book. Then we performed paiwise comparison for these tables based on cosine distance. Next according to the algorithm we plotted obtained distances and tried to tune parameter of model to make clusters of these differences, so the idea in to find more or less similar paiwise differences. Details for math fans can be found in [ссылка на статью]


4) Adaptation of k-mer analysis from bioinformatics

[Андрей]