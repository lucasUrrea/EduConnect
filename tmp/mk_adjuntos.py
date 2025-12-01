import pathlib
p = pathlib.Path('media/adjuntos')
if not p.exists():
    p.mkdir(parents=True, exist_ok=True)
    print('Created', p.resolve())
else:
    print('Already exists', p.resolve())
