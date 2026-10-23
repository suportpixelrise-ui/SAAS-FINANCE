import copy, importlib.util, json, tempfile, threading, unittest, urllib.request, urllib.error
from pathlib import Path
spec=importlib.util.spec_from_file_location('panel',Path(__file__).resolve().parents[1]/'server.py')
panel=importlib.util.module_from_spec(spec);spec.loader.exec_module(panel)
class PanelTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.old=panel.STATE; panel.STATE=Path(self.tmp.name)/'state.json'
  self.server=panel.ThreadingHTTPServer(('127.0.0.1',0),panel.Handler); self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start();self.url='http://127.0.0.1:'+str(self.server.server_port)
 def tearDown(self):
  self.server.shutdown();self.server.server_close();self.thread.join();panel.STATE=self.old;self.tmp.cleanup()
 def request(self,path='/',data=None,headers=None):
  h={'Content-Type':'application/json'};h.update(headers or {})
  req=urllib.request.Request(self.url+path,data=json.dumps(data).encode() if data is not None else None,method='PUT' if data is not None else 'GET',headers=h)
  try:
   with urllib.request.urlopen(req) as res:return res.status,res.read()
  except urllib.error.HTTPError as e:return e.code,e.read()
 def test_pages_and_no_traversal(self):
  for p,text in [('/',b'Caixa Leve'),('/landing',b'R$ 79'),('/app.js',b'fetch'),('/style.css',b'background')]:
   code,body=self.request(p);self.assertEqual(code,200);self.assertIn(text,body)
  self.assertEqual(self.request('/../server.py')[0],404)
 def test_persistence_and_conflict(self):
  code,body=self.request('/api/state');self.assertEqual(code,200);d=json.loads(body);old=copy.deepcopy(d)
  d['project']['name']='Projeto atualizado';d['campaigns']=[{'id':'a','name':'Teste','spend':150,'leads':10,'activated':4,'customers':2,'revenue':158}]
  code,body=self.request('/api/state',d);self.assertEqual(code,200);saved=json.loads(body);self.assertEqual(saved['revision'],1)
  self.assertEqual(json.loads(panel.STATE.read_text())['project']['name'],'Projeto atualizado')
  self.assertEqual(json.loads(self.request('/api/state')[1]),saved)
  self.assertEqual(self.request('/api/state',old)[0],409)
 def test_invalid_and_cross_origin_writes(self):
  d=json.loads(self.request('/api/state')[1]);d['project']['budget']=-1
  self.assertEqual(self.request('/api/state',d)[0],400)
  d['project']['budget']=1500
  self.assertEqual(self.request('/api/state',d,{'Origin':'https://untrusted.example'})[0],403)
  self.assertEqual(self.request('/api/state',d,{'Content-Type':'text/plain'})[0],415)
  d['campaigns']=[{'id':'a','name':'Bad cohort','spend':1,'leads':1,'activated':0,'customers':2,'revenue':1}]
  self.assertEqual(self.request('/api/state',d)[0],400)
  self.assertFalse(panel.STATE.exists())
if __name__=='__main__':unittest.main()
