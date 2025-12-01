import os, subprocess
os.environ['USE_SQLITE']='1'
# Run dumpdata via manage.py
cmd = [r'.\\venv\\Scripts\\python', 'manage.py', 'dumpdata', 'EduConnectApp', '--indent', '2']
print('Running:', cmd)
proc = subprocess.run(cmd, capture_output=True, text=True)
if proc.returncode != 0:
    print('Error running dumpdata:', proc.stderr)
else:
    with open('edudata.json', 'w', encoding='utf-8') as f:
        f.write(proc.stdout)
    print('Wrote edudata.json size:', os.path.getsize('edudata.json'))
