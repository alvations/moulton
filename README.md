# moulton

<!--
Cos I was asked to list **all of my papers** on an spreadsheet and populate information about my publications from Google and Semantic Scholar (by end of **_today_**)


Come on, we seriously have more important things to do!!!
-->

Install
====

```
pip install -U moulton
```

Usage
====

```python
from moulton import get_gscholar

gscholar_url = 'https://scholar.google.nl/citations?user=qGuYgMsAAAAJ&hl=en'
path_to_json_output = 'et-al.gscholar.json'

get_gscholar(path_to_json_output)
```
