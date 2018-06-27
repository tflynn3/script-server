import requests
import subprocess
import json

command_link = 'http://127.0.0.1:5000/commands'
results_link = 'http://127.0.0.1:5000/results'
r = requests.get(command_link, verify=False)
commands = json.loads(r.content)['commands']


def post_result(id, code, result):
    data = {
            'id': id,
            'code': code,
            'result': result
            }
    r = requests.post(url = results_link, headers={'Content-Type': 'application/json'}, data = json.dumps(data), verify=False)


for c in commands:
    try:
        command = c['command']
        process = c['process']
        print('Running command {}: {}'.format(c['id'], command))
        p = subprocess.Popen('{} {}'.format(process, command), stdout=subprocess.PIPE)
        result = p.communicate()[0].decode()
        #print(result)
        post_result(c['id'], 0, result)
    except Exception as e:
        print(e)