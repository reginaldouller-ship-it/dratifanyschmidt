import json, re, unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

class SiteTests(unittest.TestCase):
    def test_static_descriptions_are_visible_on_desktop(self):
        html = (ROOT/'index.html').read_text(encoding='utf-8')
        self.assertTrue(bool(re.search(r'#static-content \.proc-desc\s*\{[^}]*display:block!important', html)))

    def test_whatsapp_does_not_include_quiz_or_procedure_inquiry(self):
        from urllib.parse import urlparse, parse_qs
        for file in [ROOT/'index.html', *ROOT.glob('*-balneario-camboriu/index.html')]:
            soup = BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
            for a in soup.select('a[href^="https://wa.me/"]'):
                message=parse_qs(urlparse(a['href']).query).get('text',[''])[0].lower()
                self.assertFalse(any(term in message for term in ['quiz','toxina','lábios','labial','preenchimento','ponto de partida']))

    def test_home_works_without_javascript(self):
        soup = BeautifulSoup((ROOT / 'index.html').read_text(encoding='utf-8'), 'html.parser')
        for el in soup.select('script, template'): el.decompose()
        self.assertNotIn('{{', soup.get_text())
        self.assertNotIn('R$ 200', soup.get_text())
        links = soup.select('a[href^="https://wa.me/5547997722437"]')
        self.assertGreater(len(links), 2)
        self.assertIn('O procedimento pode ser realizado no mesmo dia', soup.get_text())

    def test_landing_pages(self):
        for slug in ['avaliacao-facial-balneario-camboriu', 'preenchimento-labial-balneario-camboriu']:
            with self.subTest(slug=slug):
                path = ROOT / slug / 'index.html'
                self.assertTrue(path.exists(), f'Página ausente: {slug}')
                s = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
                self.assertIn('Balneário Camboriú', s.title.text)
                self.assertEqual(len(s.select('h1')), 1)
                self.assertNotIn('R$ 200', s.get_text())
                self.assertTrue(s.select('a[href^="https://wa.me/5547997722437"]'))
                self.assertEqual(s.select_one('link[rel=canonical]')['href'], f'https://dratifanyschmidt.com.br/{slug}/')
                self.assertIn(f'/{slug}/', (ROOT/'sitemap.xml').read_text())
                for image in s.select('img[src]'):
                    self.assertTrue((ROOT / image['src'].lstrip('/')).exists())

    def test_structured_data_and_no_false_promise(self):
        s = BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'), 'html.parser')
        for node in s.select('script[type="application/ld+json"]'): json.loads(node.string)
        self.assertNotIn('Nenhum procedimento é feito no mesmo dia', str(s))
        self.assertNotIn('quiz_resultado', str(s))

if __name__ == '__main__': unittest.main()
