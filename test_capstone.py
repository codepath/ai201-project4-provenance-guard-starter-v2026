"""Operational contract tests; model mocks are isolated from real HTTP evaluation."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import capstone
import config
import detector
import telemetry


class TelemetryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        root=Path(self.tmp.name)
        self.patches=[patch.object(telemetry,'TRACE_PATH',root/'requests.jsonl'),
                      patch.multiple(config,LOG_DIR=root,AUDIT_LOG=root/'audit.jsonl')]
        for p in self.patches: p.start()
        capstone.service.limiter.reset()
        self.client=capstone.app.test_client()

    def tearDown(self):
        for p in reversed(self.patches): p.stop()
        self.tmp.cleanup()

    def test_failed_input_is_correlated_once(self):
        response=self.client.post('/submit',data='{broken',content_type='application/json')
        rows=telemetry.read_traces()
        self.assertEqual(response.status_code,400)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['request_id'],response.headers['X-Request-ID'])
        self.assertEqual(rows[0]['output']['error'],'invalid_json')

    def test_model_failure_is_logged(self):
        with patch.object(detector,'model_signal',side_effect=detector.DetectorUnavailable('fixture')):
            response=self.client.post('/submit',json={'text':'A paragraph about tests.','creator_id':'test'})
        row=telemetry.read_traces()[0]
        self.assertEqual(response.status_code,503)
        self.assertEqual(row['status'],503)
        self.assertIn('model_ms',row['stages'])

    def test_no_prose_in_request_telemetry(self):
        secret='PRIVATE_PROSE_SHOULD_NOT_APPEAR'
        with patch.object(detector,'model_signal',return_value=.5):
            self.client.post('/submit',json={'text':secret,'creator_id':'test'})
        row=telemetry.read_traces()[0]
        self.assertNotIn(secret,json.dumps(row))
        self.assertEqual(row['input']['text_characters'],len(secret))
        self.assertEqual(len(row['input']['text_sha256']),64)
        self.assertEqual(set(row['stages']),{'model_ms','style_ms','combine_ms','audit_ms'})

    def test_dashboard_does_not_pollute_traces(self):
        for route in ['/','/ops/traces','/ops/export','/static/capstone.js','/static/capstone.css']:
            with self.client.get(route) as response:
                self.assertEqual(response.status_code,200)
        self.assertEqual(telemetry.read_traces(),[])

    def test_log_output_is_not_recursively_copied(self):
        self.client.get('/log')
        self.assertEqual(telemetry.read_traces()[0]['output'],{'count':0,'entries_omitted':True})

    def test_rate_limit_is_logged(self):
        with patch.object(detector,'model_signal',return_value=.5):
            responses=[self.client.post('/submit',json={'text':'A paragraph for the limiter.','creator_id':'limited'}) for _ in range(11)]
        self.assertEqual(responses[-1].status_code,429)
        rows=telemetry.read_traces()
        self.assertEqual(len(rows),11)
        self.assertEqual(rows[-1]['status'],429)

    def test_write_failure_keeps_response_and_reports_loss(self):
        with patch.object(telemetry,'TRACE_PATH',Path(self.tmp.name)):
            response=self.client.post('/ping',json={'message':'hello'})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.headers['X-Telemetry-Status'],'write_failed')


if __name__=='__main__':
    unittest.main()
