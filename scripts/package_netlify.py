"""Build a static Netlify ZIP. Default seed is public; never includes private state."""
import argparse,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--state',type=Path,help='Explicit public project JSON to bundle; never use for private financial data');p.add_argument('--output',type=Path,default=ROOT/'artifacts/caixa-leve-netlify.zip');args=p.parse_args()
state=json.loads((args.state or ROOT/'data/seed.json').read_text());args.output.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(args.output,'w',compression=zipfile.ZIP_STORED) as z:
 for name in ['index.html','landing.html','style.css','app.js','zip.js']:z.write(ROOT/'web'/name,name)
 z.writestr('project.json',json.dumps(state,ensure_ascii=False,indent=2))
 z.writestr('_redirects','/landing /landing.html 200\n')
 z.writestr('_headers','/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: same-origin\n  Content-Security-Policy: default-src \'self\'; script-src \'self\'; style-src \'self\'; img-src \'self\' data:; connect-src \'self\'; frame-ancestors \'none\'; base-uri \'self\'\n/app.js\n  Cache-Control: no-cache\n/project.json\n  Cache-Control: no-store\n')
 z.writestr('COMO-PUBLICAR.txt','1. Extraia este ZIP.\n2. No Netlify Drop, envie a pasta que contém index.html.\n3. Abra o endereço gerado pelo Netlify.\n4. Aba Trocar dados com ChatGPT: exportar ZIP e anexar na conversa.\n5. Importe o ZIP de dados devolvido pelo ChatGPT.\n6. Para atualizar o site inteiro, faça novo deploy no MESMO site. Dados do navegador são preservados; para aplicar o plano do ZIP, use o botão específico.\n7. O site não tem login. Não inclua dados privados nos arquivos publicados. Os dados editados ficam somente no navegador, sem sincronização automática.\n')
print(args.output)
