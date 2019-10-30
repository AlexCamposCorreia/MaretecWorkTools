import os
import subprocess

f = open('latex/comparison_pdf.tex', 'w')
f.write(r'''
\documentclass{article}

\usepackage{graphicx}
\usepackage{float}

\begin{document}
''')

properties = ['temperature', 'salinity', 'density', 'oxygen']

cp_dirs = list(filter(lambda x: x.startswith('campanha'), list(next(os.walk('.')))[1]))

for cp_dir in cp_dirs:
    for prop_name in properties:
        f.write('\n\\begin{figure}')
        f.write('\n\t\\includegraphics[width=0.7\\textwidth]{../'+cp_dir+'/comparison/'+prop_name+'.pdf'+'}')
        f.write('\n\\end{figure}')
        f.write('\n')

for prop_name in properties:
        f.write('\n\\begin{figure}')
        f.write('\n\t\\includegraphics[width=\\textwidth]{../comparison/'+prop_name+'.pdf'+'}')
        f.write('\n\\end{figure}')
        f.write('\n')


f.write(r'\end{document}')
f.close()

os.chdir('./latex')

p = subprocess.Popen('xelatex.exe -synctex=1 -interaction=nonstopmode "comparison_pdf".tex')
p.wait()

