<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ movie.title }} — Film Archive</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --paper:    #f3eee3;
    --card:     #fbf8f1;
    --ink:      #2a2520;
    --ink-dim:  #6f6457;
    --ink-faint:#a89c8c;
    --rule:     #d8cdb9;
    --rule-dark:#c2b49a;
    --accent:   #b5402c;
    --accent-2: #2f5a4f;
    --gold:     #c08a35;
    --radius: 3px;
    --container: 820px;
  }

  *{ box-sizing: border-box; }

  body{
    margin:0;
    background: var(--paper);
    color: var(--ink);
    font-family: 'Inter', system-ui, sans-serif;
    line-height: 1.6;
    background-image:
      repeating-linear-gradient(180deg, transparent, transparent 31px, rgba(0,0,0,0.025) 32px);
  }

  a{ color: var(--accent); text-decoration: none; }
  a:hover{ text-decoration: underline; }

  header{
    border-bottom: 3px double var(--rule-dark);
    padding: 20px clamp(16px, 4vw, 40px);
  }
  .breadcrumb{
    max-width: var(--container);
    margin: 0 auto;
    font-family: 'IBM Plex Mono', monospace;
    font-size: .76rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--ink-dim);
  }

  main{
    max-width: var(--container);
    margin: 0 auto;
    padding: clamp(28px, 5vw, 48px) clamp(16px, 4vw, 40px) 80px;
  }

  .record-id{
    font-family: 'IBM Plex Mono', monospace;
    font-size: .72rem;
    letter-spacing: .25em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 12px;
  }

  h1{
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: clamp(2rem, 6vw, 3.2rem);
    margin: 0 0 6px;
    line-height: 1.1;
  }

  .release{
    color: var(--ink-dim);
    font-family: 'IBM Plex Mono', monospace;
    font-size: .9rem;
    margin-bottom: 22px;
  }

  .stat-row{
    display:flex;
    gap: 28px;
    flex-wrap: wrap;
    padding: 18px 0;
    border-top: 1px solid var(--rule);
    border-bottom: 1px solid var(--rule);
    margin-bottom: 26px;
  }
  .stat{
    display:flex;
    flex-direction:column;
    gap: 4px;
  }
  .stat .label{
    font-family: 'IBM Plex Mono', monospace;
    font-size: .68rem;
    letter-spacing: .15em;
    text-transform: uppercase;
    color: var(--ink-faint);
  }
  .stat .value{
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 1.4rem;
  }
  .stat .value.rating{ color: var(--gold); }

  .genres{
    display:flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 28px;
  }
  .genre-tag{
    font-family: 'IBM Plex Mono', monospace;
    font-size: .72rem;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--accent-2);
    border: 1px solid var(--accent-2);
    border-radius: 999px;
    padding: 4px 12px;
  }

  .description{
    font-size: 1.02rem;
    color: var(--ink);
    margin-bottom: 30px;
    max-width: 68ch;
  }

  .credits{
    display:grid;
    grid-template-columns: 140px 1fr;
    gap: 10px 20px;
    font-size: .92rem;
    border-top: 1px solid var(--rule);
    padding-top: 22px;
  }
  .credits dt{
    font-family: 'IBM Plex Mono', monospace;
    font-size: .72rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--ink-faint);
    align-self: start;
    padding-top: 3px;
  }
  .credits dd{
    margin:0;
    color: var(--ink-dim);
  }

  .back-link{
    display:inline-flex;
    align-items:center;
    gap: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: .8rem;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-top: 36px;
    color: var(--ink-dim);
    border: 1px solid var(--rule-dark);
    border-radius: var(--radius);
    padding: 10px 18px;
  }
  .back-link:hover{
    border-color: var(--accent);
    color: var(--accent);
    text-decoration: none;
  }

  footer{
    border-top: 3px double var(--rule-dark);
    text-align:center;
    color: var(--ink-dim);
    font-family: 'IBM Plex Mono', monospace;
    font-size: .76rem;
    letter-spacing: .08em;
    padding: 24px 20px;
  }

  @media (max-width: 480px){
    .credits{ grid-template-columns: 1fr; }
    .credits dt{ padding-top: 0; }
  }
</style>
</head>
<body>

<header>
  <div class="breadcrumb"><a href="/">&larr; Back to Index</a></div>
</header>

<main>
  <div class="record-id">Catalog Entry No. {{ "%05d"|format(movie.id) }}</div>
  <h1>{{ movie.title }}</h1>
  <div class="release">{{ movie.release_date }}{% if movie.duration %} &middot; {{ movie.duration }}{% endif %}</div>

  <div class="stat-row">
    {% if movie.rating %}
    <div class="stat">
      <span class="label">Rating</span>
      <span class="value rating">★ {{ "%.1f"|format(movie.rating) }} / 10</span>
    </div>
    {% endif %}
    {% if movie.votes %}
    <div class="stat">
      <span class="label">Votes</span>
      <span class="value">{{ "{:,}".format(movie.votes|int) }}</span>
    </div>
    {% endif %}
    {% if movie.duration_minutes %}
    <div class="stat">
      <span class="label">Runtime</span>
      <span class="value">{{ movie.duration_minutes|int }} min</span>
    </div>
    {% endif %}
  </div>

  {% if movie.genres %}
  <div class="genres">
    {% for g in movie.genres.split(',') %}
      {% if g.strip() %}<span class="genre-tag">{{ g.strip() }}</span>{% endif %}
    {% endfor %}
  </div>
  {% endif %}

  {% if movie.description %}
  <p class="description">{{ movie.description }}</p>
  {% endif %}

  <dl class="credits">
    {% if movie.directed_by %}
    <dt>Directed by</dt>
    <dd>{{ movie.directed_by }}</dd>
    {% endif %}
    {% if movie.written_by %}
    <dt>Written by</dt>
    <dd>{{ movie.written_by }}</dd>
    {% endif %}
  </dl>

  <a class="back-link" href="/">&larr; Return to Index</a>
</main>

<footer>Film Archive Database</footer>

</body>
</html>
