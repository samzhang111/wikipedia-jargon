# Wikipedia jargon analysis

What words are used predominantly on Simple Wikipedia pages, vs. those on English Wikipedia?

## Installation

`pip install -r requirements.txt`

## Usage

The pipeline goes:

- `grab_subjects.py [list of Wikipedia categories, separated by spaces]`

- `grab_text.py [list of title files]`

- `make_tf_differences.py [n-grams] [text directory]` (where n-gram refers to 1 for unigrams, 2 for bigrams, etc)

- `make_tables.py [term-diffs-dir]/*`

The categories that I used were:

* Anthropology
* Archaeology
* Astronomy
* Biology
* Chemistry
* Economics
* Engineering
* Linguistics
* Mathematics
* Music
* Physics
* Psychology
* Sociology

### Initial analysis
I started off doing this on a small scale, with the math pages. That analysis
is available in the `initial-math-analysis` folder and the notebook here:
http://nbviewer.ipython.org/github/samzhang111/wikipedia-jargon/blob/master/initial-math-analysis/Jargon%20in%20Mathematics.ipynb

The included data files are
- `simple-wiki-math.xml` --> Simple Wikipedia math category pages
- `wiki-math.xml` --> English Wikipedia math category pages
- `*.p` --> pickled version of cleaned up, dictionary-fied content of the above
- `term_differences.csv` --> output, the actual differences in term frequencies

### Warning

I wrote this code in 2015. Since then, I think I've gotten a little better at structuring these types of exploratory projects :) (and everything is Python 3 now!). I touched it up so I could finally publish a blog post about this: https://sam.zhang.fyi/projects/2017-04-25-wikipedia-jargon/.
