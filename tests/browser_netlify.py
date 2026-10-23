"""End-to-end static ZIP roundtrip, persistence, conflict and validation."""
import shutil, functools, http.server, json, subprocess, tempfile, threading, zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
 folder=Path(tmp);subprocess.run(['python',str(ROOT/'scripts/package_netlify.py'),'--output',str(folder/'site.zip')],check=True)
 with zipfile.ZipFile(folder/'site.zip') as z:
  assert 'index.html' in z.namelist();assert 'server.py' not in z.namelist();assert 'data/state.json' not in z.namelist();z.extractall(folder/'site')
 handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(folder/'site'))
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(headless=True, executable_path=shutil.which("chromium"));context=browser.new_context(accept_downloads=True);page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto('http://127.0.0.1:'+str(server.server_port));page.wait_for_selector('#project input');assert page.locator('#project input').nth(2).input_value()=='500'
   page.locator('#project input').first.fill('Projeto no navegador');page.locator('#save').click();assert 'Salvo neste navegador' in page.locator('#message').inner_text()
   page.reload();page.wait_for_selector('#project input');assert page.locator('#project input').first.input_value()=='Projeto no navegador'
   with page.expect_download() as dl:page.locator('#export-package').click()
   export=folder/'export.zip';dl.value.save_as(export)
   with zipfile.ZipFile(export) as z:d=json.loads(z.read('project.json'));assert d['project']['name']=='Projeto no navegador'
   d['project']['name']='Atualizado pelo assistente'
   with zipfile.ZipFile(folder/'update.zip','w',compression=zipfile.ZIP_STORED) as z:z.writestr('project.json',json.dumps(d))
   page.on('dialog',lambda dialog:dialog.accept())
   with page.expect_download():page.locator('#import').set_input_files(str(folder/'update.zip'))
   page.wait_for_function("document.querySelector('#project input').value==='Atualizado pelo assistente'")
   page.reload();page.wait_for_selector('#project input');assert page.locator('#project input').first.input_value()=='Atualizado pelo assistente'
   # Redeploy public seed must not overwrite saved browser data.
   seed=json.loads((folder/'site/project.json').read_text());seed['project']['name']='Novo plano publicado';(folder/'site/project.json').write_text(json.dumps(seed))
   page.reload();page.wait_for_selector('#project input');assert page.locator('#project input').first.input_value()=='Atualizado pelo assistente'
   with page.expect_download():page.locator('#apply-bundled').click()
   page.wait_for_function("document.querySelector('#project input').value==='Novo plano publicado'")
   (folder/'invalid.json').write_text('{"project": {"name":"inválido"}}');page.locator('#import').set_input_files(str(folder/'invalid.json'));page.wait_for_function("document.querySelector('#message').textContent.includes('Importação:')");assert page.locator('#project input').first.input_value()=='Novo plano publicado'
   # Another tab must not silently overwrite a newer saved revision.
   other=page.context.new_page();other.goto(page.url);other.wait_for_selector('#project input');page.locator('#project input').first.fill('Aba principal');page.locator('#save').click();other.locator('#project input').first.fill('Aba antiga');other.locator('#save').click();assert 'Outra aba' in other.locator('#message').inner_text()
   assert not errors,errors
   page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(ROOT/'artifacts/painel-mobile.png'),full_page=True)
   browser.close();print('PASS: static deployment, ZIP export/import, persistence, redeploy, bundled update, invalid import, tab conflict, no JS errors')
 finally:server.shutdown();server.server_close();thread.join()
