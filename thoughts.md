# Data Mining (Thoughts)

> Clustering Last.fm users according to their listening profiles (music tastes, temporal distribution of listening events, mainstreaminess, novelty/openness, diversity

**The data** will be fetched from **Last.fm**

## What should be possible?

- Check the listening events per day/week/month (heavy usage, normal usage, rare usage)
- Any songs loved on Last.fm (get higher weight)
  - Check if loved songs changed over time
- Check mainstreaminess based on current top charts of:
  - Tags (lower weight)
  - Artists (medium weight)
  - Tracks (highest weight)
  - (not optimal) Check artists of the user, and check the artist similarity. If there similar artists it be also be counted as mainstream (max 3 similar artists)

### Define diversity

- Music from different countries
- Play count of different tracks/genre

## What is not possible?

- Check how long the users heard a song. Based on that, the song (and its genre/tag) have another weight

## Hints

- Skips, anhand von timestamps
- Wenn mit TSNE dann mit unterschiedlichen Werten experimentieren
- LatentDirichletAllocation (LDA)
- [sklearn.manifold](http://scikit-learn.org/stable/modules/classes.html#module-sklearn.manifold) (bissi experimentieren, ersten 3 und TSNE)
- Zeitfenster Months, Charts ausrechnen, Daten von allen Usern
- Diversity / entropy von Genres
