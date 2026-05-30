# arXiv Source

arXiv can be automated because it provides an official API. Prefer the existing `arxiv-search` skill when available.

## Use Cases

- computer science
- physics
- quantitative biology
- mathematics
- statistics
- economics
- electrical engineering

## Retrieval Rules

- Convert Chinese user intent into 3-5 English academic keywords.
- Use `all:` for broad search.
- Use `cat:` for category constraints.
- Use Boolean operators `AND`, `OR`, `ANDNOT`.
- Respect the arXiv rate limit. Add 3-second delays between sequential API calls.

## Output Normalization

Map arXiv metadata into the same schema:

| Normalized field | arXiv field |
|---|---|
| `title` | title |
| `authors` | authors |
| `source` | primary category or arXiv |
| `year` | published year |
| `abstract` | summary |
| `keywords` | categories |
| `doi` | doi if present |
| `url` | entry URL |
| `pdf_url` | PDF link |

Then continue with per-paper coding.
