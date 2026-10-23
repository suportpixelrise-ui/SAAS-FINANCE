"""Local project control panel. No external dependencies or production authentication."""
import json, os, threading, tempfile
from datetime import datetime, timezone
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlsplit
ROOT = Path(__file__).resolve().parent
STATE = ROOT / 'data/state.json'
LOCK = threading.Lock()
MAX_BODY = 1024 * 1024

def read_state():
    return json.loads((STATE if STATE.exists() else ROOT / 'data/seed.json').read_text())

def validate(d):
    if not isinstance(d, dict): raise ValueError('Objeto JSON obrigatório')
    if set(d) != {'project','tasks','campaigns','creatives','decisions','updated_at','revision'}: raise ValueError('Estrutura inválida')
    if not isinstance(d['revision'],int) or d['revision'] < 0: raise ValueError('Revisão inválida')
    p=d['project']
    if not isinstance(p,dict) or set(p) != {'name','stage','budget','price','audience','goal','notes'}: raise ValueError('Projeto inválido')
    for k in ['name','stage','audience','goal','notes']:
        if not isinstance(p[k],str) or len(p[k])>10000: raise ValueError('Texto inválido')
    for k in ['budget','price']:
        if type(p[k]) not in (int,float) or not 0 <= p[k] <= 1000000000: raise ValueError('Valor inválido')
    schemas={'tasks':{'id','title','status','owner'},'campaigns':{'id','name','spend','leads','activated','customers','revenue'},'creatives':{'id','name','hook','angle','status'},'decisions':{'id','date','text'}}
    for group, keys in schemas.items():
        if not isinstance(d[group],list) or len(d[group])>1000: raise ValueError('Lista inválida')
        ids=set()
        for row in d[group]:
            if not isinstance(row,dict) or set(row)!=keys: raise ValueError('Registro inválido')
            for k,v in row.items():
                if group=='campaigns' and k not in ['id','name']:
                    if type(v) not in (int,float) or not 0 <= v <= 1000000000: raise ValueError('Métrica inválida')
                    if k in ['leads','activated','customers'] and int(v)!=v: raise ValueError('Contagem inválida')
                elif not isinstance(v,str) or len(v)>10000: raise ValueError('Texto inválido')
            if not row['id'] or row['id'] in ids: raise ValueError('ID duplicado')
            ids.add(row['id'])
            if group=='campaigns' and not row['customers']<=row['activated']<=row['leads']: raise ValueError('Use clientes ≤ ativados ≤ leads para a mesma coorte')
    json.dumps(d,allow_nan=False)

class Handler(BaseHTTPRequestHandler):
    def respond(self,status,payload,kind='application/json; charset=utf-8'):
        b=payload if isinstance(payload,bytes) else json.dumps(payload,ensure_ascii=False).encode()
        self.send_response(status); self.send_header('Content-Type',kind); self.send_header('Content-Length',str(len(b)))
        self.send_header('Cache-Control','no-store'); self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'self'")
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        path=urlsplit(self.path).path
        if path=='/api/state':
            with LOCK: self.respond(200,read_state())
            return
        files={'/project.json':'project.json','/zip.js':'zip.js','/':'index.html','/landing':'landing.html','/app.js':'app.js','/style.css':'style.css'}
        if path not in files: self.respond(404,{'error':'Não encontrado'}); return
        f=ROOT/'data/seed.json' if path=='/project.json' else ROOT/'web'/files[path]
        kind={'.json':'application/json; charset=utf-8','.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8'}[f.suffix]
        self.respond(200,f.read_bytes(),kind)
    def do_PUT(self):
        if self.path!='/api/state': self.respond(404,{'error':'Não encontrado'}); return
        # Browsers from another origin cannot mutate this local service.
        origin=self.headers.get('Origin')
        if origin and urlsplit(origin).netloc != self.headers.get('Host'): self.respond(403,{'error':'Origem não permitida'}); return
        if self.headers.get('Sec-Fetch-Site')=='cross-site': self.respond(403,{'error':'Origem não permitida'}); return
        if self.headers.get('Content-Type','').split(';')[0]!='application/json': self.respond(415,{'error':'Envie application/json'}); return
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<=MAX_BODY: raise ValueError('Tamanho inválido')
            d=json.loads(self.rfile.read(n)); validate(d)
            with LOCK:
                if d['revision']!=read_state()['revision']: self.respond(409,{'error':'Dados alterados em outra sessão. Recarregue antes de salvar.'}); return
                d['revision']+=1; d['updated_at']=datetime.now(timezone.utc).isoformat()
                with tempfile.NamedTemporaryFile(mode='w',dir=STATE.parent,suffix='.tmp',delete=False) as f:
                    json.dump(d,f,ensure_ascii=False,indent=2,allow_nan=False); temp=f.name
                os.replace(temp,STATE)
            self.respond(200,d)
        except (ValueError,TypeError,KeyError) as e: self.respond(400,{'error':str(e)})

if __name__=='__main__':
    server=ThreadingHTTPServer((os.environ.get('HOST','127.0.0.1'),int(os.environ.get('PORT','8000'))),Handler)
    print('Painel iniciado; uso local, sem autenticação. Não exponha à internet.',flush=True)
    server.serve_forever()
