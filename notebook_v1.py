#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
an object-oriented version of the notebook toolbox
"""
from types import CellType
from notebook_v0 import load_ipynb, save_ipynb


class Cell:
    def __init__(self):
        pass

class CodeCell(Cell):
    r"""A Cell of Python code in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.
        execution_count (int): number of times the cell has been executed.

    Usage:

        >>> code_cell = CodeCell({
        ...     "cell_type": "code",
        ...     "execution_count": 1,
        ...     "id": "b777420a",
        ...     'source': ['print("Hello world!")']
        ... })
        >>> code_cell.id
        'b777420a'
        >>> code_cell.execution_count
        1
        >>> code_cell.source
        ['print("Hello world!")']
    """

    def __init__(self, ipynb):
        self.execution_count = ipynb['execution_count']
        self.id = ipynb['id']
        self.source = ipynb['source']
        self.type = ipynb['cell_type']

class MarkdownCell(Cell):
    r"""A Cell of Markdown markup in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.

    Usage:

        >>> markdown_cell = MarkdownCell({
        ...    "cell_type": "markdown",
        ...    "id": "a9541506",
        ...    "source": [
        ...        "Hello world!\n",
        ...        "============\n",
        ...        "Print `Hello world!`:"
        ...    ]
        ... })
        >>> markdown_cell.id
        'a9541506'
        >>> markdown_cell.source
        ['Hello world!\n', '============\n', 'Print `Hello world!`:']
    """

    def __init__(self, ipynb):
        self.id = ipynb['id']
        self.source = ipynb['source']
        self.type = ipynb['cell_type']
        

class Notebook:
    r"""A Jupyter Notebook.

    Args:
        ipynb (dict): a dictionary representing a Jupyter Notebook.

    Attributes:
        version (str): the version of the notebook format.
        cells (list): a list of cells (either CodeCell or MarkdownCell).

    Usage:

        - checking the verion number:

            >>> ipynb = toolbox.load_ipynb("samples/minimal.ipynb")
            >>> nb = Notebook(ipynb)
            >>> nb.version
            '4.5'

        - checking the type of the notebook parts:

            >>> ipynb = toolbox.load_ipynb("samples/hello-world.ipynb")
            >>> nb = Notebook(ipynb)
            >>> isinstance(nb.cells, list)
            True
            >>> isinstance(nb.cells[0], Cell)
            True
    """
    def __init__(self, ipynb):
        self.version = f"{ipynb['nbformat']}.{ipynb['nbformat_minor']}"
        
        list_of_cells = []
        for cell in ipynb['cells']:
            if cell['cell_type'] == 'markdown':
                list_of_cells.append(MarkdownCell(cell))
            if cell['cell_type'] == 'code':
                list_of_cells.append(CodeCell(cell))
        self.cells = list_of_cells 


    @staticmethod
    def from_file(filename):
        r"""Loads a notebook from an .ipynb file.

        Usage:

            >>> nb = Notebook.from_file("samples/minimal.ipynb")
            >>> nb.version
            '4.5'
        """
        data = load_ipynb(filename)
        return Notebook(data)


    def __iter__(self):
        r"""Iterate the cells of the notebook.

        Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
        """
        return iter(self.cells)


class PyPercentSerializer:
    r"""Prints a given Notebook in py-percent format.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:
            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> ppp = PyPercentSerializer(nb)
            >>> print(ppp.to_py_percent()) # doctest: +NORMALIZE_WHITESPACE
            # %% [markdown]
            # Hello world!
            # ============
            # Print `Hello world!`:
            <BLANKLINE>
            # %%
            print("Hello world!")
            <BLANKLINE>
            # %% [markdown]
            # Goodbye! 👋
    """
    def __init__(self, notebook):
        self.notebook = notebook

    def to_py_percent(self):
        r"""Converts the notebook to a string in py-percent format.
        """
        script = ""
        for cell in self.notebook:
            if isinstance(cell, MarkdownCell):
                if cell == self.notebook.cells[0]:
                    script += "# %% [markdown]\n# "
                    script += "# ".join(cell.source)
                    script += "\n"
                else:
                    script += "\n# %% [markdown]\n# "
                    script += "# ".join(cell.source)
                    script += "\n"

            elif isinstance(cell, CodeCell):
                if cell == self.notebook.cells[0]:
                    script += "# %%\n"
                    script += "".join(cell.source)
                    script += "\n"
                else:
                    script += "\n# %%\n"
                    script += "".join(cell.source)
                    script += "\n"
        return script

    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = PyPercentSerializer(nb)
                >>> s.to_file("samples/hello-world-serialized-py-percent.py")
        """
        with open(filename, 'w') as file:
            file.write(self.to_py_percent())


class Serializer(Notebook):
    r"""Serializes a Jupyter Notebook to a file.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:

        >>> nb = Notebook.from_file("samples/hello-world.ipynb")
        >>> s = Serializer(nb)
        >>> pprint.pprint(s.serialize())  # doctest: +NORMALIZE_WHITESPACE
            {'cells': [{'cell_type': 'markdown',
                'id': 'a9541506',
                'metadata': {},
                'source': ['Hello world!\n',
                           '============\n',
                           'Print `Hello world!`:']},
               {'cell_type': 'code',
                'execution_count': 1,
                'id': 'b777420a',
                'metadata': {},
                'outputs': [],
                'source': ['print("Hello world!")']},
               {'cell_type': 'markdown',
                'id': 'a23ab5ac',
                'metadata': {},
                'source': ['Goodbye! 👋']}],
            'metadata': {},
            'nbformat': 4,
            'nbformat_minor': 5}
        >>> s.to_file("samples/hello-world-serialized.ipynb")
    """

    def __init__(self, notebook):
        self.notebook = notebook

    def serialize(self):
        r"""Serializes the notebook to a JSON object

        Returns:
            dict: a dictionary representing the notebook.
        """
        dic = {}
        dic['cells'] = []
        for cell in self.notebook:
            if isinstance(cell, CodeCell):
                new_cell = {'cell_type': cell.type, 'execution_count' : cell.execution_count, 'id': cell.id, 'metadata':{}, 'outputs':[], 'source': cell.source}
                dic['cells'].append(new_cell)
            elif isinstance(cell, MarkdownCell):
                new_cell = {'cell_type': cell.type, 'id': cell.id, 'metadata':{}, 'source': cell.source}
                dic['cells'].append(new_cell)
        dic['metadata'] = {}
        dic['nbformat'] = int(self.notebook.version[0])
        dic['nbformat_minor'] = int(self.notebook.version[2])     
        return dic 
        

    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = Serializer(nb)
                >>> s.to_file("samples/hello-world-serialized.ipynb")
                >>> nb = Notebook.from_file("samples/hello-world-serialized.ipynb")
                >>> for cell in nb:
                ...     print(cell.id)
                a9541506
                b777420a
                a23ab5ac
        """
        save_ipynb(self.serialize(), filename)

class Outliner(Notebook):
    r"""Quickly outlines the strucure of the notebook in a readable format.

    Args:
        notebook (Notebook): the notebook to outline.

    Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> o = Outliner(nb)
            >>> print(o.outline()) # doctest: +NORMALIZE_WHITESPACE
                Jupyter Notebook v4.5
                └─▶ Markdown cell #a9541506
                    ┌  Hello world!
                    │  ============
                    └  Print `Hello world!`:
                └─▶ Code cell #b777420a (1)
                    | print("Hello world!")
                └─▶ Markdown cell #a23ab5ac
                    | Goodbye! 👋
    """
    def __init__(self, notebook):
        self.notebook = notebook

    def outline(self):
        r"""Outlines the notebook in a readable format.

        Returns:
            str: a string representing the outline of the notebook.
        """
        script = f"Jupyter Notebook v{self.notebook.version}"
        for cell in self.notebook.cells:
            if isinstance(cell, MarkdownCell):
                script += f"\n└─▶ Markdown cell #{cell.id}\n"
                if len(cell.source) > 1:
                    script += f"    ┌  {cell.source[0]}"
                    for k in range(1, len(cell.source)-1):
                        script += f"    │  {cell.source[k]}"
                    script += f"    └  {cell.source[-1]}"
                else:
                    script += f"    | {cell.source[0]}\n"
            elif isinstance(cell, CodeCell):
                script += f"\n└─▶ Code cell #{cell.id} ({cell.execution_count})\n"
                if len(cell.source) > 1:
                    script += f"    ┌  {cell.source[0]}"
                    for k in range(1, len(cell.source)):
                        script += f"    │  {cell.source[k]}"
                    script += f"    └  {cell.source[-1]}"
                else:
                    script += f"    | {cell.source[0]}"
        return script