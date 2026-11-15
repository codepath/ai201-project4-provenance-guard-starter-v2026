"""Real HTTP evaluation. No model doubles; preserve every response and trace."""
import argparse
import json
import statistics
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import requests

TEXTS = [
    'The implementation of an effective framework requires careful consideration of several key factors. First, organizations should establish clear objectives and define measurable outcomes. Furthermore, consistent communication helps stakeholders understand their responsibilities and work toward shared goals.',
    'I left my blue notebook beside the library printer on Tuesday. When I came back, somebody had tucked a receipt inside the cover. It said to ask at the front desk. The librarian had saved my notes, which was lucky because the exam was the next morning.',
    'Stop! The violet kettle slid beneath my grandmother\'s crooked kitchen chair, trailing sparks and a ribbon of steam. Why, though? I ran. My brother stood in the doorway, laughing so hard that he could barely hold the camera steady.',
]


def run(base, phase):
    records = []
    def call(route, payload=None, raw=None):
        start = time.perf_counter()
        response = requests.post(base+route, json=payload, timeout=180) if raw is None else requests.post(base+route, data=raw, headers={'Content-Type':'application/json'}, timeout=180)
        elapsed = (time.perf_counter()-start)*1000
        try:
            body = response.json()
        except ValueError:
            body = {'non_json_response': response.text[:500]}
        record = {'route':route,'status':response.status_code,'request_id':response.headers.get('X-Request-ID'), 'client_ms':round(elapsed,4),'output':body}
        records.append(record)
        return record

    warmup = call('/submit', {'text':TEXTS[0], 'creator_id':'warmup-'+uuid.uuid4().hex})
    if warmup['status'] != 200:
        raise RuntimeError('Real model unavailable: '+json.dumps(warmup))
    trials=[]
    for trial in range(1,4):
        successes=[call('/submit', {'text':text,'creator_id':f'{phase}-{trial}-{i}-'+uuid.uuid4().hex}) for i,text in enumerate(TEXTS)]
        failures=[call('/submit',raw='{broken'),call('/submit',{'creator_id':'missing-'+uuid.uuid4().hex}),
                  call('/submit',{'text':'A valid paragraph. Another sentence.','creator_id':' '}),
                  call('/submit',{'text':'x'*20001,'creator_id':'oversize-'+uuid.uuid4().hex}),
                  call('/appeal',{'content_id':str(uuid.uuid4()),'reasoning':'Unknown decision fixture.'})]
        body=successes[0]['output']; content_id=body.get('content_id','missing')
        before=requests.get(base+'/log',timeout=30).json()['entries']
        appeal=call('/appeal',{'content_id':content_id,'reasoning':'Synthetic capstone appeal fixture, requesting manual review.'})
        after=requests.get(base+'/log',timeout=30).json()['entries']
        rows=requests.get(base+'/ops/traces',timeout=30).json()['entries']
        def matches(rec):
            return [r for r in rows if r['request_id']==rec['request_id']]
        required={'timestamp','input','output','status','wall_ms','cpu_ms','request_id'}
        c1=sum(r['status']==200 and len(matches(r))==1 and required<=matches(r)[0].keys() for r in successes)
        c2=sum(r['status']==expected and len(matches(r))==1 and matches(r)[0]['status']==expected and matches(r)[0]['output'].get('error')==r['output'].get('error') for r,expected in zip(failures,[400,400,400,413,404]))
        def stage_ok(rec):
            rs=matches(rec)
            if len(rs)!=1: return False
            row=rs[0]; st=row['stages']
            return st.get('model_ms',0)>0 and all(st.get(k,-1)>=0 for k in ['style_ms','combine_ms','audit_ms']) and sum(st.values())<=row['wall_ms']+1
        c3=sum(stage_ok(r) for r in successes)
        c4=sum(r['status']==200 and r['client_ms']<5000 for r in successes)
        original=[r for r in before if r.get('content_id')==content_id and r.get('status')=='decided']
        preserved=[r for r in after if r.get('content_id')==content_id and r.get('status')=='decided']
        c5=int({'content_id','guess','confidence','label','model_score','style_score','status'}<=body.keys() and len(original)==1 and original==preserved and appeal['status']==200 and any(r.get('content_id')==content_id and r.get('status')=='under_review' for r in after))
        trials.append({'trial':trial,'counts':[c1,c2,c3,c4,c5],'targets':[3,5,3,3,1], 'successes':successes,'failures':failures,'appeal':appeal,'traces':rows})
    costs=[]
    for i in range(10):
        rec=call('/submit',{'text':TEXTS[i%3],'creator_id':'cost-'+uuid.uuid4().hex})
        rows=requests.get(base+'/ops/traces',timeout=30).json()['entries']
        matches=[r for r in rows if r['request_id']==rec['request_id']]
        if rec['status']!=200 or len(matches)!=1: raise RuntimeError('Cost run missing its real trace')
        costs.append(matches[0])
    result={'phase':phase,'timestamp':datetime.now(timezone.utc).isoformat(),'model':'gpt2','model_mode':'real, no mocks','warmup':warmup,'trials':trials,'requests':records,'cost_samples':costs,
            'mean_cpu_seconds':statistics.mean(r['cpu_ms'] for r in costs)/1000,
            'mean_wall_seconds':statistics.mean(r['wall_ms'] for r in costs)/1000,
            'verdicts':['MET' if all(t['counts'][i]==t['targets'][i] for t in trials) else 'MISSED' for i in range(5)]}
    path=Path(__file__).parent/'results'/'capstone'/f'{phase}.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'phase':phase,'verdicts':result['verdicts'],'trials':[t['counts'] for t in trials], 'warmup_ms':warmup['client_ms'],'mean_cpu_seconds':result['mean_cpu_seconds'],'mean_wall_seconds':result['mean_wall_seconds'],'evidence':str(path)},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--base',default='http://127.0.0.1:5050')
    parser.add_argument('--phase',choices=['before','after'],required=True)
    args=parser.parse_args()
    run(args.base,args.phase)
