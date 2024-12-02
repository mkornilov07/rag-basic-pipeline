import wikipedia
articlesRequested = ["Stardust Crusaders", "Jotaro Kujo", "Joseph Joestar", "Diamond is Unbreakable", "Stone Ocean", "Jolyne Kujo", "List of Jojo's Bizarre Adventure Characters"]
for i, query in enumerate(articlesRequested):
    results = wikipedia.search(query)
    # print(f"got results {results}")
    for j in range(len(results)):
        try:
            article = wikipedia.page(title=results[j])
        except:
            pass
        else:
            print(f"Fetched '{article.title}' at {article.url}")
            file = open(f"data/{i}.txt", "w", encoding="utf8")
            file.write(article.content)
            file.close()
            break
    