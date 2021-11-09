from sympy import latex, print_latex

def save_to_pdf(n,H,H_matrix,evals,evects):
    """
    """
    image = f"""
    \\section{{Fractal N = {n}}}
    \\begin{{figure}}[h!]
      \\centering
      \\includegraphics[scale=0.7]{{output//N={str(n)}//N={str(n)}_lattice.png}}
      \\caption{{Lattice}}
    \\end{{figure}}
    """


    content = f"""
    \\subsection{{Hamoltionian}}
    $H={latex(H)}$

    \\subsection{{Matrix}}
    ${latex(H_matrix)}$

    \\subsection{{Eigen Values}}
    ${latex(evals)}$

    \\subsection{{Eigen Vectors}}
    ${latex(evects)}$
    """

    latex_template = r"""
\documentclass[11pt]{article}
\usepackage[landscape, letterpaper, margin=.75in]{geometry}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{multicol}
\begin{document}

"""+image+content+"""\end{document}"""
    
    filepath = f'N_{n}.tex'
    with open(filepath, 'w') as f:
            f.write(latex_template)

    from os import system
    system(f'pdflatex {filepath}')
