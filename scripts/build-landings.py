"""Generate the two service pages using shared, editable content and layout."""
from pathlib import Path
from urllib.parse import quote
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
pages = [
    dict(slug='avaliacao-facial-balneario-camboriu', title='Avaliação facial em Balneário Camboriú', heading='O primeiro passo é entender você.', intro='Uma consulta individual com a Dra. Tifany Schmidt para conversar sobre seus objetivos, avaliar seu rosto e construir um plano de cuidados.', eyebrow='Avaliação facial · Balneário Camboriú', action='Quero agendar minha consulta', subject='uma avaliação facial', about='Um plano que começa pela conversa', detail='A avaliação reúne o que você deseja valorizar, seu histórico e o olhar profissional da Dra. Tifany. As possibilidades, os limites e os valores são explicados antes de qualquer decisão.', extra_q='Preciso saber qual procedimento quero fazer?', extra_a='Não. Você pode trazer suas dúvidas e o que gostaria de valorizar. A consulta serve justamente para entender quais opções fazem sentido para o seu caso.'),
    dict(slug='preenchimento-labial-balneario-camboriu', title='Preenchimento labial em Balneário Camboriú', heading='Seus lábios, com planejamento individual.', intro='Converse com a Dra. Tifany Schmidt sobre suas expectativas e descubra se o preenchimento labial é indicado para você.', eyebrow='Preenchimento labial · Balneário Camboriú', action='Agendar avaliação dos lábios', subject='uma avaliação para preenchimento labial', about='A indicação vem antes do procedimento', detail='O planejamento considera as proporções do rosto, as características dos lábios e suas expectativas. Durante a consulta, a Dra. explica as possibilidades, os riscos, os cuidados e o orçamento. Não há um volume ou resultado padrão para todas as pessoas.', extra_q='O resultado é igual para todas as pessoas?', extra_a='Não. As características individuais e a avaliação profissional orientam o planejamento. Imagens de referência não representam promessa de um resultado específico.'),
]
for page in pages:
    url = 'https://dratifanyschmidt.com.br/'+page['slug']+'/'
    message = "Oi Dra. Tifany! Gostaria de agendar uma consulta. Vi que custa R$ 200, com valor abatido no procedimento posterior."
    wa = 'https://wa.me/5547997722437?text='+quote(message)
    faq = [
      ('Quanto custa a consulta?', 'A consulta custa R$ 200. Esse valor é abatido caso você realize o procedimento posteriormente. O valor do procedimento é informado após a avaliação individual.'),
      ('Posso fazer o procedimento no mesmo dia?', 'Existe essa possibilidade, conforme indicação após a avaliação, disponibilidade de horário e sua decisão. Avise no agendamento se tiver interesse, para organizarmos o tempo necessário.'),
      ('Preciso decidir no dia da consulta?', 'Não. Você pode tirar suas dúvidas e decidir com calma. Não é necessário realizar o procedimento no mesmo dia para ter o valor da consulta abatido posteriormente.'),
      (page['extra_q'], page['extra_a']),
      ('Onde fica o consultório?', 'Rua 700, nº 489, sala 2404, Ed. Benvenutti Business Center — C.Cliniq, Centro, Balneário Camboriú/SC. CEP 88330-620. Atendimento com hora marcada.'),
    ]
    structured = {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq]}
    details = '\n'.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q,a in faq)
    html = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{page['title']} | Dra. Tifany Schmidt</title>
<meta name="description" content="{escape(page['intro'],quote=True)} Consulta de R$ 200, com abatimento no procedimento posterior.">
<link rel="canonical" href="{url}"><link rel="icon" href="/assets/favicon.png">
<meta property="og:title" content="{page['title']} | Dra. Tifany Schmidt"><meta property="og:description" content="Avaliação individual, com hora marcada, no Centro de Balneário Camboriú.">
<meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:image" content="https://dratifanyschmidt.com.br/assets/og-image.jpg">
<link rel="stylesheet" href="/assets/landing.css"><script src="/assets/measurement.js" defer></script>
<script type="application/ld+json">{json.dumps(structured,ensure_ascii=False)}</script></head><body>
<header><a href="/" aria-label="Dra. Tifany Schmidt — página inicial"><img src="/assets/logo-lettering-creme.png" alt="Dra. Tifany Schmidt"></a><a class="header-cta" href="{wa}" target="_blank" rel="noopener">Agendar pelo WhatsApp</a></header>
<main><section class="hero"><div class="wrap hero-grid"><div class="hero-copy"><p class="eyebrow">{page['eyebrow']}</p><h1>{page['heading']}</h1><p class="lead">{page['intro']}</p>
<p class="offer"><strong>Consulta de R$ 200</strong><br>Valor abatido caso você realize o procedimento posteriormente.</p><a class="cta hero-cta" href="{wa}" target="_blank" rel="noopener">{page['action']}</a><p class="note">Biomédica esteta · CRBM-5 014010<br>Atendimento com hora marcada, no Centro de Balneário Camboriú.</p></div>
<figure style="margin:0"><img class="hero-photo" src="/assets/foto-hero.jpg" alt="Retrato da Dra. Tifany Schmidt" width="800" height="1067"></figure></div></section>
<section class="section"><div class="wrap"><p class="eyebrow">Como funciona</p><h2>{page['about']}</h2><p style="max-width:800px">{page['detail']}</p><div class="cards">
<article class="card"><span>01 · CONVERSA</span><h3>Seus objetivos e seu histórico</h3><p>Um momento para entender o que você busca e esclarecer suas dúvidas.</p></article>
<article class="card"><span>02 · AVALIAÇÃO</span><h3>Indicação individual</h3><p>A Dra. avalia as possibilidades e apresenta um plano com valores e orientações.</p></article>
<article class="card"><span>03 · DECISÃO</span><h3>Você decide com tranquilidade</h3><p>Quando houver indicação e tempo disponível, o procedimento pode ser realizado no mesmo dia. Também é possível agendar para depois.</p></article></div></div></section>
<section class="section soft"><div class="wrap split"><div><p class="eyebrow">Quem atende você</p><h2>Dra. Tifany Schmidt</h2><p>Biomédica esteta, registrada no CRBM-5 sob o nº 014010. Atendimento individual, explicação de cada etapa e acompanhamento conforme o plano de cuidados.</p></div><div><p class="eyebrow">Localização</p><h2>No Centro de Balneário Camboriú</h2><p>Rua 700, nº 489, sala 2404<br>Ed. Benvenutti Business Center — C.Cliniq<br>CEP 88330-620 · Balneário Camboriú/SC</p><a href="https://www.google.com/maps/search/?api=1&amp;query=Rua%20700%20489%20Balneario%20Camboriu" target="_blank" rel="noopener">Ver como chegar</a></div></div></section>
<section class="section"><div class="wrap faq"><p class="eyebrow">Antes de agendar</p><h2>Perguntas frequentes</h2>{details}</div></section>
<section class="section soft"><div class="wrap"><h2>Vamos conversar sobre você?</h2><p>Fale pelo WhatsApp para consultar os horários disponíveis.</p><a class="cta dark pre-cta-btn" href="{wa}" target="_blank" rel="noopener">Agendar minha consulta</a></div></section></main>
<footer><div class="wrap"><span>Dra. Tifany Schmidt · CRBM-5 014010</span><a href="/">Página inicial</a><a href="/privacidade.html">Privacidade</a><button type="button" data-cookie-settings>Preferências de cookies</button></div></footer>
<a class="mobile-cta" href="{wa}" target="_blank" rel="noopener">Consultar horários no WhatsApp</a></body></html>'''
    folder = ROOT/page['slug']; folder.mkdir(exist_ok=True)
    (folder/'index.html').write_text(html,encoding='utf-8')
print('2 páginas de destino geradas')
