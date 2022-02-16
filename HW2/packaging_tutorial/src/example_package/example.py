import numpy
from PIL import Image


def generate_random_pic(filename: str):
    a = numpy.random.rand(30, 30, 3) * 255
    im_out = Image.fromarray(a.astype('uint8')).convert('RGB')
    im_out.save(f'{filename}.jpg')

from string import Template

LATEX_FILE_TEMPLATE_TABLE_SHAPE_PLACEHOLDER = "TABULAR_SHAPE"
LATEX_FILE_TEMPLATE_TABLE_CONTENT_PLACEHOLDER = "TABULAR_CONTENT"
LATEX_FILE_TEMPLATE = \
    Template("""\\documentclass{article}
\\usepackage{graphicx}
\\graphicspath{ {./} }
\\usepackage[utf8]{inputenc}

\\title{AdvancedPythonHW2}
\\author{psolikov15 }
\\date{February 2022}

\\begin{document}

\\maketitle

\\section{Introduction}
\\begin{center}
\\begin{tabular}{ $TABULAR_SHAPE }
 \\hline
 $TABULAR_CONTENT
 \\hline
\\end{tabular}
\\end{center}

\\includegraphics{lala}

\\end{document}
""")


def generate_latex_from_list(table: list):
    shape = "|" + "c|" * (len(table[0]))
    content = "".join([" ".join([f"{e} &" for e in row]) + ' \\\\ \n' for row in table])
    return LATEX_FILE_TEMPLATE.substitute({f"{LATEX_FILE_TEMPLATE_TABLE_SHAPE_PLACEHOLDER}": shape,
                                           f"{LATEX_FILE_TEMPLATE_TABLE_CONTENT_PLACEHOLDER}": content})


def save_latex(latex_str: str, filename: str):
    with open(f'{filename}.tex', 'w') as output_file:
        output_file.write(latex_str)


if __name__ == '__main__':
    test_list = [[1, 2, 3], [4, 5, 6]]
    save_latex(generate_latex_from_list(test_list), "test")

# if __name__ == '__main__':
#     generate_random_pic("lala")