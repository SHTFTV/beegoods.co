from pathlib import Path
from html.parser import HTMLParser
import json
from PIL import Image
root=Path(__file__).parent/'public';errors=[];pages=list(root.rglob('index.html'))
class Read(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.meta={};self.h1=0;self.time=0
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='h1':self.h1+=1
  if t=='time':self.time+=1
  if t in ['img','script','source','link','a']:
   u=d.get('src') or d.get('href','')
   if u.startswith('/') and not u.startswith('//'):self.links.append(u)
  if t=='meta':self.meta[d.get('property') or d.get('name')]=d.get('content')
for p in pages:
 r=Read();r.feed(p.read_text());url='/'+str(p.parent.relative_to(root))+'/'
 if r.h1!=1:errors.append((url,'h1',r.h1))
 for u in r.links:
  path=u.split('?')[0].split('#')[0];target=root/path.lstrip('/')
  if not target.exists() and not (target/'index.html').exists():errors.append((url,'missing',u))
 og=r.meta.get('og:image','').replace('https://beegoods.co/','')
 if not og or not (root/og).exists():errors.append((url,'share missing'))
 elif Image.open(root/og).size!=(1200,630):errors.append((url,'share size'))
print(json.dumps({'pages':len(pages),'errors':errors},indent=2));assert not errors
