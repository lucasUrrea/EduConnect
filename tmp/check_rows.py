p = 'tmp/dashboard_debug.html'
with open(p,encoding='utf-8') as f:
    s = f.read()
    print('dashboard contains consulta-row:', s.count('class="consulta-row"'))

p2 = 'tmp/mis_consultas_debug.html'
with open(p2,encoding='utf-8') as f:
    s = f.read()
    print('mis-consultas contains consulta-row:', s.count('consulta-row'))
    # print a short snippet
    i = s.find('<!--')
    print('len mis_consultas html', len(s))
