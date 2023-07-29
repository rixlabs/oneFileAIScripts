import arxiv
def arxiv_search():
    summary = ''
    search = arxiv.Search(
      query = "language model",
      max_results = 1,
      sort_by = arxiv.SortCriterion.SubmittedDate
    )
    for result in search.results():
        summary = f"Title: {result.title}, Abstract: {result.summary}, URL: {result.entry_id}"

    return summary