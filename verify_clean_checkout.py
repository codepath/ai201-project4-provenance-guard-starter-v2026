"""Check committed source in an isolated local clone, reusing installed packages."""
import importlib.metadata
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests

root=Path(__file__).parent.resolve()
temp=Path(tempfile.mkdtemp(prefix='ai201-capstone-check-')).resolve()
checkout=temp/'checkout'
subprocess.run(['git','clone','--shared','--branch','capstone/observability',str(root),str(checkout)],check=True,capture_output=True,text=True)
commit=subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'],text=True).strip()
output=(temp/'server.txt').open('w',encoding='utf-8')
env=os.environ.copy()
env.pop('CAPSTONE_TRACE_PATH',None)
process=subprocess.Popen([sys.executable,'capstone.py','--port','5051'],cwd=checkout,stdout=output,stderr=subprocess.STDOUT,env=env,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
try:
    base='http://127.0.0.1:5051'
    for _ in range(120):
        if process.poll() is not None: raise RuntimeError('Clean source server exited before ready')
        try:
            home=requests.get(base+'/',timeout=2)
            if home.status_code==200: break
        except requests.RequestException:
            pass
        time.sleep(.5)
    else: raise RuntimeError('Clean source startup timed out')
    ping=requests.post(base+'/ping',json={'message':'clean checkout'},timeout=10)
    assert ping.status_code==200 and ping.json()['you_sent']=='clean checkout'
    invalid=requests.post(base+'/submit',json={},timeout=10)
    assert invalid.status_code==400
    start=time.perf_counter()
    decision=requests.post(base+'/submit',json={'text':'My notebook fell out of my bag near the library yesterday. A friend found it and sent me a message. I was grateful to have the notes back before our study session.','creator_id':'clean-checkout-fixture'},timeout=180)
    elapsed=time.perf_counter()-start
    assert decision.status_code==200, decision.text
    assets={route:requests.get(base+route,timeout=10).status_code for route in ['/static/capstone.css','/static/capstone.js','/ops/traces','/ops/export']}
    assert all(status==200 for status in assets.values())
    rows=requests.get(base+'/ops/traces',timeout=10).json()['entries']
    assert any(r['request_id']==invalid.headers['X-Request-ID'] and r['status']==400 for r in rows)
    result={'source_commit':commit,'source_clean_clone':True,'checkout':str(checkout),
            'start_command':f'{sys.executable} capstone.py --port 5051',
            'environment':'Existing installed Python packages reused; fresh dependency installation NOT tested.',
            'packages':{name:importlib.metadata.version(name) for name in ['Flask','Flask-Limiter','requests','transformers','torch','certifi']},
            'home_http':home.status_code,'home_has_title':'Provenance Guard' in home.text,
            'ping':ping.json(),'invalid_http':invalid.status_code,
            'real_model_http':decision.status_code,'real_model_output':decision.json(),
            'first_real_request_seconds':elapsed,'assets':assets,'request_traces':rows,
            'visual_browser_qa':'Unavailable; no visual verification claimed'}
    path=root/'results'/'capstone'/'clean-checkout.json'
    path.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
finally:
    process.terminate()
    process.wait(timeout=20)
    output.close()
