What words are used predominantly on Simple Wikipedia pages, vs. those on English Wikipedia?

The pipeline goes:

- `grab_subjects.py [list of Wikipedia categories, separated by spaces]`

- `grab_category_text.py [list of title files]`

- `make_tf_differences.py [text directory]`

### Initial analysis
I started off doing this on a small scale, with the math pages. That analysis
is available in the `initial-math-analysis` folder and the notebook here:
http://nbviewer.ipython.org/github/samzhang111/wikipedia-jargon/blob/master/initial-math-analysis/Jargon%20in%20Mathematics.ipynb

The included data files are
- `simple-wiki-math.xml` --> Simple Wikipedia math category pages
- `wiki-math.xml` --> English Wikipedia math category pages
- `*.p` --> pickled version of cleaned up, dictionary-fied content of the above
- `term_differences.csv` --> output, the actual differences in term frequencies
