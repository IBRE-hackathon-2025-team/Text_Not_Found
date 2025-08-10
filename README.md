# Text Not Found ...

Here we present a work analyzing the authorship of books by a very productive writer and private detective enthusiast.  
She has been writing for 26 years and has already published **381 books**.  
This means she writes around **15 books per year** — or **1.2 per month**.  
 
<img src="plots/writing_stat.png" alt="Writing trend" width="400">

Suspicious, isn’t it? Some people even believe that the writer’s pugs (yes, small dogs!) help her type the books. 🐕


<img src="images/pug_detective.jpeg" alt="Pug detective" width="100">

*The real ghostwriters? We may never know...*

So, we decided to analyse the authorship of these books to shed light on this mystery. We also hope this project can inspire similar analyses in other fields.  
Of course, we do not claim **100% truth** in our conclusions — but you can join us on this journey to solve the riddle.

A small spoiler: we created a **pipeline for text authorship analysis using k-mers**. This is a new approach for stylometry, so be patient and read until the end!


## Data description

- **341 books** of the author of interest
- **10 other detective novels** (control group 1)
- **10 other detective novels** (control group 2)
- **10 other detective novels** (control group 3)
- **5 generated texts**
- **5 interviews**
- **2 fan-fiction**
- **And 6 pugs** (ok, that last one is a joke — actually 6 funny and positive people 😄)

## Required packages

1. **[Stylo](https://github.com/computationalstylistics/stylo)** (R package for stylometry)
2. **[spaCy](https://spacy.io/usage/spacy-101#whats-spacy)** (advanced NLP library for Python), used for preprocessing
3. **[GigaChain](https://github.com/ai-forever/gigachain)** used for text generation in the style of the author
4. **[scikit-learn](https://scikit-learn.org/stable/)** used for dimentionality reduction
5. [Библиотеки для topology]
6. **[NetworkX](https://networkx.org/documentation/stable/tutorial.html)** used for construction of graphs

## Data preparation

1) Books come in different formats, but we decided to use .txt. We wrote a converter from .fb2 → .txt, which can be found here: [fb2_txt_converter.py](code/fb2_txt_converter.py)

2) We tested several preprocessing methods (see [название файла]):

- Original text
- Lemmatized text (e.g., бегал → бегать, слону → слон)
- Lemmatized text without punctuation and stopwords (stopwords — the most common words in a language).
- Reduced to parts of speech (e.g., слон → NOUN, бегать → VERB) without stopwords/punctuation
- Parts of speech encoded as one-letter codes:
  - a = ADJ   (adjective)
  - b = ADP   (adposition)
  - c = ADV   (adverb)
  - etc...

## Generation of Neuroversion of our author books



## Analysis

1) We used the stylo R package — a standard tool in stylometry for comparing texts using word frequencies.

Анализ в библиотеке Stylo основан на дельте Берроуза. Эта метрика позволяет определить насколько тексты похожи или отличаются друг от друга. В первую очередь по всему корпусу рассчитываются частоты для определнного числа слов. На основе полученных частот строится матрица расстояний для каждой пары книг из корпуса.

#### Автор относительно других авторов детективов

Мы определили, что наш выбранный автор отделяется от других писателей, работающих в этом стиле, значит особенности стиля этого автора не определяются только принаджлежностью к литературному жанру.

<img src="images/author_in_detective_field.png" alt="Detective tree" width="600">

#### Изменение стиля автора с течением времени

Благодаря метрикам стилометрии можно определить изменился ли стиль автора текста с течением времени. Наш загадочный автор очень продуктивный и пишет непрерывно больше 20 лет. Можно ли заметить разницу в стиле (а может и авторстве) произведений?

<img src="images/author_in_time.jpg" alt="Author's style" width="600">

<img src="images/author_in_time_graph.png" alt="Author's style graph" width="600">

Да! Можно однозначно сказать, что ранние произведения автора слабо похожи на более поздние и совсем не похожие на самые последние. Мы не готовы сделать однозначный вывод о причинах наблюдаемых закономерностей, но предполагаем, что это связано либо с большим количеством редактуры, либо с плагиатом, а возможно с написанием книги специально нанятым человеком.

[example of the frequency table]

2) Based on word frequency tables from stylo, we applied dimentionality reduction:

- PCA
- tSNE

[картинки результатов и описание]

3) Topological analysis

The idea:

1. Get frequency of each word/POS (part of speech) in each book.
2. Compute pairwise distances (cosine distance).
3. Plot distances as a topological graph and tune parameters to detect clusters.

Details for math fans: [ссылка на статью]

[картинки результатов и описание]

4) Adaptation of k-mer analysis from bioinformatics

We wanted to analyze how much an author maintains its grammatical style, how it changes and evolves throughout the works. So we adapted k-mer frequency analysis to grammar patterns. For k from 2 to 10, we calculated frequency of POS sequences for each book. By comparing sets between books and with the general pool of k-dimensional sets, we can check how similar each text is to the next. Then we cluster the results.

[картинки результатов и описание]
