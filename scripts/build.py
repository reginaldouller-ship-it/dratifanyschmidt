"""Build the homepage's initial HTML from the same source as its interactions.
Run: python scripts/build.py (requires Node and requirements-build.txt).
"""
import copy, json, re, subprocess
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'src/home.html').read_text(encoding='utf-8')
values = json.loads(subprocess.check_output(['node', str(ROOT/'scripts/render-values.cjs'), str(ROOT/'src/home.html')], encoding='utf-8'))

def lookup(expr, scope):
    value = scope
    for part in expr.strip().split('.'):
        value = value[int(part)] if isinstance(value, list) else value.get(part, '') if isinstance(value, dict) else ''
    return value

def replace(text, scope):
    return re.sub(r'{{\s*(.*?)\s*}}', lambda m: str(lookup(m[1], scope)), text)

def render(node, scope):
    for child in list(node.children):
        if isinstance(child, Comment): child.extract()
        elif isinstance(child, NavigableString): child.replace_with(replace(str(child), scope))
        elif child.name == 'sc-for':
            expression = child['list'].strip('{} ').strip()
            for item in lookup(expression, scope):
                local = dict(scope, **{child['as']: item})
                for item_node in list(child.children):
                    wrapper = BeautifulSoup('<div></div>', 'html.parser').div
                    wrapper.append(copy.copy(item_node))
                    render(wrapper, local)
                    for rendered in list(wrapper.contents): child.insert_before(rendered.extract())
            child.decompose()
        else:
            for attr, value in list(child.attrs.items()):
                if attr.startswith('sc-') or attr.startswith('on') or attr == 'id': del child.attrs[attr]
                else: child[attr] = replace(' '.join(value) if isinstance(value, list) else value, scope)
            render(child, scope)

soup = BeautifulSoup(source, 'html.parser')
component = soup.find('x-dc')
helmet = component.find('helmet')
styles = ''.join(str(tag) for tag in helmet.find_all(['style', 'link']))
helmet.decompose()
render(component, values)
for button in component.select('button'): button.decompose()
for quiz in component.select('.quiz-card'): quiz.find_parent('section').decompose()
# All answers and service descriptions remain readable without JS.
for el in component.select('[style]'):
    el['style'] = re.sub(r'max-height:\s*0px', 'max-height:none', el['style'])
for el in component.select('.quiz-wrap, .quiz-shell'): el.decompose()
static = '<main id="static-content">' + component.decode_contents() + '</main>'
template = re.search(r'<x-dc>[\s\S]*?</x-dc>', source).group(0)
output = source.replace(template, '<template id="interactive-template">'+template+'</template>\n'+static)
output = output.replace('</head>', styles + '''
<style>
x-dc {display:none}
#static-content .reveal,#static-content .reveal-stagger>* {opacity:1!important;transform:none!important}
#static-content .proc-desc {max-height:none!important;opacity:1!important}
#static-content .quiz-section {display:none}
#static-content .gallery-grid,#static-content .testi-track {overflow-x:auto}
</style></head>''')
output = output.replace('</body>', '''
<script>
// Keep the real HTML usable until the interactive version has mounted.
(function(){
  var template=document.getElementById('interactive-template');
  template.replaceWith(template.content.cloneNode(true));
  var observer=new MutationObserver(function(){
    if(document.querySelector('#dc-root .hero')){
      var initial=document.getElementById('static-content');
      if(initial)initial.remove();
      observer.disconnect();
    }
  });
  observer.observe(document.body,{childList:true,subtree:true});
})();
</script></body>''')
(ROOT/'index.html').write_text(output, encoding='utf-8')
print('Homepage generated from src/home.html')
