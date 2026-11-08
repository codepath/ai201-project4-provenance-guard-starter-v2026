"""Verify the actual app.py process over HTTP, using the real cached GPT-2 model.

This is a regression check, not the unavailable staff attack set or five-criterion evaluation.
"""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import uuid
import requests


def main():
    root = Path(__file__).resolve().parent
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 0))
        port = probe.getsockname()[1]
    base = f'http://127.0.0.1:{port}'
    env = dict(os.environ, HOST='127.0.0.1', PORT=str(port), AI201_DEBUG='0',
               HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')
    rows = []
    run = uuid.uuid4().hex[:10]
    samples = json.loads((root/'samples.json').read_text(encoding='utf-8'))
    log_path = root/'results/live_verification_server.log'
    with log_path.open('w', encoding='utf-8') as output:
        process = subprocess.Popen([sys.executable, 'app.py'], cwd=root, env=env, stdout=output, stderr=subprocess.STDOUT)
        try:
            for _ in range(120):
                if process.poll() is not None:
                    raise RuntimeError('app.py exited; see server log')
                try:
                    health = requests.get(base+'/health', timeout=1)
                    if health.status_code == 200:
                        break
                except requests.RequestException:
                    pass
                time.sleep(.5)
            else:
                raise RuntimeError('App did not start')
            assert health.json()['rate_limiting'] is True
            start = requests.get(base+'/log', timeout=10).json()['count']

            def call(name, route, expected, **kwargs):
                response = requests.post(base+route, timeout=180, **kwargs)
                body = response.json()
                rows.append({'name': name, 'expected_status': expected, 'status': response.status_code, 'response': body})
                assert response.status_code == expected, rows[-1]
                return body

            for trial in range(1, 4):
                prefix = f'live-{run}-{trial}'
                call(f'trial {trial}: ping', '/ping', 200, json={'message':'live check'})
                expected = {'Irregular synthetic fixture':'human', 'AI-generated expository prose':'unsure', 'Repetitive AI fixture':'ai'}
                for sample in samples:
                    if sample['name'] in expected:
                        body = call(f'trial {trial}: {sample["name"]}', '/submit', 200,
                                    json={'text':sample['text'], 'creator_id':prefix+'-'+expected[sample['name']]})
                        assert body['guess'] == expected[sample['name']], body
                        assert body['status'] == 'decided'
                        for field in ('confidence', 'model_score', 'style_score'):
                            assert 0 <= body[field] <= 1
                        reason = f'Automated regression appeal fixture {prefix}'
                        appeal = call(f'trial {trial}: appeal {body["guess"]}', '/appeal', 200,
                                      json={'content_id':body['content_id'], 'reasoning':reason})
                        assert appeal['status'] == 'under_review'
                call(f'trial {trial}: unknown appeal', '/appeal', 404,
                     json={'content_id':prefix+'-unknown', 'reasoning':'Regression fixture'})
                cases = [({},400), ({'text':' ', 'creator_id':prefix+'-blank'},400),
                         ({'text':'Valid text.', 'creator_id':[]},400),
                         ({'text':'x'*20001,'creator_id':prefix+'-oversize'},413)]
                for index, (payload, status) in enumerate(cases):
                    call(f'trial {trial}: invalid {index}', '/submit', status, json=payload)
                call(f'trial {trial}: malformed JSON', '/submit', 400, data='{broken', headers={'Content-Type':'application/json'})
                creator = prefix+'-flood'
                for index in range(15):
                    call(f'trial {trial}: flood {index+1}', '/submit', 200 if index < 10 else 429,
                         json={'text':samples[0]['text'], 'creator_id':creator})
                call(f'trial {trial}: independent creator after flood', '/submit', 200,
                     json={'text':samples[0]['text'], 'creator_id':prefix+'-independent'})
                print(f'Trial {trial}: labels, appeals, invalid input, 10 accepted / 5 rejected, creator isolation PASS', flush=True)

            # A valid exact-size submission passes through the real tokenizer/model.
            call('inclusive 20000-character boundary', '/submit', 200,
                 json={'text':('The system works. '*1200)[:20000], 'creator_id':f'live-{run}-boundary'})
            entries = requests.get(base+'/log', timeout=10).json()['entries'][start:]
            required = {'timestamp','content_id','creator_id','guess','model_score','style_score','combined_score','label','status'}
            decisions = [e for e in entries if e['status']=='decided']
            assert len(decisions) == 43, len(decisions)
            assert all(required <= e.keys() for e in decisions)
            for row in rows:
                body = row['response']
                if row['status']==200 and body.get('status')=='decided':
                    matches = [e for e in decisions if e['content_id']==body['content_id']]
                    assert len(matches)==1
                    event = matches[0]
                    assert event['combined_score']==body['confidence']
                    assert all(event[key]==body[key] for key in ('guess','label','model_score','style_score'))
                if row['status']==200 and body.get('status')=='under_review':
                    events = [e for e in entries if e.get('content_id')==body['content_id']]
                    assert len(events)==2 and events[0]['status']=='decided' and events[1]['status']=='under_review'
                    assert events[0]['creator_id']==events[1]['creator_id']
            rejected = [e for e in entries if e['status']=='rejected']
            assert len(rejected)==33, len(rejected)
            assert sum(e.get('reason')=='rate_limited' for e in rejected)==15
            final_health = requests.get(base+'/health', timeout=10).json()
            assert final_health['detector_loaded'] is True
            evidence = {'result':'PASS', 'trials':3, 'requests':rows, 'new_audit_entries':entries,
                        'health':final_health, 'checks':{'decisions':len(decisions),'appeals':9,'rejections':len(rejected),'rate_limit_rejections':15}}
            (root/'results/live_verification.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
            print(f'PASS: {len(rows)} HTTP requests; 43 decisions, 9 appeals, 33 rejections verified in GET /log.', flush=True)
        finally:
            process.terminate()
            process.wait(timeout=15)


if __name__ == '__main__':
    main()
