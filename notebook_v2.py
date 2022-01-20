#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
an object-oriented version of the notebook toolbox
"""
from notebook_v0 import load_ipynb, get_format_version, get_cells

## on recopie ici la classe PyPercentSerialize du notebook_v1 car on en aura besoin pouir la denrière question
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


class Cell:
    def __init__(self, id, source):
        self.id = id 
        self.source = source

class CodeCell(Cell):
    r"""A Cell of Python code in a Jupyter notebook.

    Args:
        id (str): The unique ID of the cell.
        source (list): The source code of the cell, as a list of str.
        execution_count (int): The execution count of the cell.

    Attributes:
        id (str): The unique ID of the cell.
        source (list): The source code of the cell, as a list of str.
        execution_count (int): The execution count of the cell.

    Usage:

        >>> code_cell = CodeCell("b777420a", ['print("Hello world!")'], 1)
        ... })
        >>> code_cell.id
        'b777420a'
        >>> code_cell.execution_count
        1
        >>> code_cell.source
        ['print("Hello world!")']
    """
    def __init__(self, id, source, execution_count):
        self.execution_count = execution_count
        super().__init__(id, source)
        

class MarkdownCell(Cell):
    r"""A Cell of Markdown markup in a Jupyter notebook.

    Args:
        id (str): The unique ID of the cell.
        source (list): The source code of the cell, as a list of str.

    Attributes:
        id (str): The unique ID of the cell.
        source (list): The source code of the cell, as a list of str.

    Usage:

        >>> markdown_cell = MarkdownCell("a9541506", [
        ...     "Hello world!",
        ...     "============",
        ...     "Print `Hello world!`:"
        ... ])
        >>> markdown_cell.id
        'a9541506'
        >>> markdown_cell.source
        ['Hello world!', '============', 'Print `Hello world!`:']
    """
    def __init__(self, id, source):
        super().__init__(id, source)

class Notebook:
    r"""A Jupyter Notebook

    Args:
        version (str): The version of the notebook format.
        cells (list): The cells of the notebook (either CodeCell or MarkdownCell).

    Attributes:
        version (str): The version of the notebook format.
        cells (list): The cells of the notebook (either CodeCell or MarkdownCell).

    Usage:

        >>> version = "4.5"
        >>> cells = [
        ...     MarkdownCell("a9541506", [
        ...         "Hello world!",
        ...         "============",
        ...         "Print `Hello world!`:"
        ...     ]),
        ...     CodeCell("b777420a", ['print("Hello world!")'], 1),
        ... ]
        >>> nb = Notebook(version, cells)
        >>> nb.version
        '4.5'
        >>> isinstance(nb.cells, list)
        True
        >>> isinstance(nb.cells[0], MarkdownCell)
        True
        >>> isinstance(nb.cells[1], CodeCell)
        True
    """

    def __init__(self, version, cells):
        self.version = version
        self.cells = cells
    
    def __iter__(self):
        r"""Iterate the cells of the notebook.
        """
        return iter(self.cells)

class NotebookLoader:
    r"""Loads a Jupyter Notebook from a file

    Args:
        filename (str): The name of the file to load.

    Usage:
            >>> nbl = NotebookLoader("samples/hello-world.ipynb")
            >>> nb = nbl.load()
            >>> nb.version
            '4.5'
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
    """
    def __init__(self, filename):
        self.filename = filename 

    def load(self):
        r"""Loads a Notebook instance from the file.
        """
        ipynb = load_ipynb(self.filename)
        version = get_format_version(ipynb)
        cells = []
        for cell in get_cells(ipynb):
            if cell['cell_type'] == 'markdown':
                cell = MarkdownCell(cell['id'], cell['source'])
                cells.append(cell)
            elif cell['cell_type'] == 'code':
                cell = CodeCell(cell['id'], cell['source'], cell['execution_count'])
                cells.append(cell)
        return Notebook(version, cells)
       

class Markdownizer:
    r"""Transforms a notebook to a pure markdown notebook.

    Args:
        notebook (Notebook): The notebook to transform.

    Usage:

        >>> nb = NotebookLoader("samples/hello-world.ipynb").load()
        >>> nb2 = Markdownizer(nb).markdownize()
        >>> nb2.version
        '4.5'
        >>> for cell in nb2:
        ...     print(cell.id)
        a9541506
        b777420a
        a23ab5ac
        >>> isinstance(nb2.cells[1], MarkdownCell)
        True
        >>> Serializer(nb2).to_file("samples/hello-world-markdown.ipynb")
    """

    def __init__(self, notebook):
        self.notebook = notebook

    def markdownize(self):
        r"""Transforms the notebook to a pure markdown notebook.
        """
        version = self.notebook.version 
        cells = []
        for cell in self.notebook.cells:
            if isinstance(cell, CodeCell):
                new_source = '''python
                {cell.source}
                '''
                cell = MarkdownCell(cell.id, new_source)
                cells.append(cell)
            else:
                cells.append(cell)
        return Notebook(version, cells)

class MarkdownLesser:
    r"""Removes markdown cells from a notebook.

    Args:
        notebook (Notebook): The notebook to transform.

    Usage:

            >>> nb = NotebookLoader("samples/hello-world.ipynb").load()
            >>> nb2 = MarkdownLesser(nb).remove_markdown_cells()
            >>> print(Outliner(nb2).outline())
            Jupyter Notebook v4.5
            └─▶ Code cell #b777420a (1)
                | print("Hello world!")
    """
    def __init__(self, notebook):
        self.notebook = notebook

    def remove_markdown_cells(self):
        r"""Removes markdown cells from the notebook.

        Returns:
            Notebook: a Notebook instance with only code cells
        """
        version = self.notebook.version 
        cells = []
        for cell in self.notebook.cells:
            if isinstance(cell, CodeCell):
                cells.append(cell)
        return Notebook(version, cells)

class PyPercentLoader:
    r"""Loads a Jupyter Notebook from a py-percent file.

    Args:
        filename (str): The name of the file to load.
        version (str): The version of the notebook format (defaults to '4.5').

    Usage:

            >>> # Step 1 - Load the notebook and save it as a py-percent file
            >>> nb = NotebookLoader("samples/hello-world.ipynb").load()
            >>> PyPercentSerializer(nb).to_file("samples/hello-world-py-percent.py")
            >>> # Step 2 - Load the py-percent file
            >>> nb2 = PyPercentLoader("samples/hello-world-py-percent.py").load()
            >>> nb.version
            '4.5'
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
    """

    def __init__(self, filename, version="4.5"):
        self.filename = filename 
        self.version = version 

    def load(self):
        r"""Loads a Notebook instance from the py-percent file.
        """
        
        with open(self.filename, 'r') as file:
            data = file.read()
        
        lines = data.split('\n')
        cells = []
        i = 0 
        while i+1 < len(lines):
            if lines[i] == '# %% [markdown]':
                source = []
                while lines[i+1] != '' and i+1 < len(lines):
                    i += 1
                    source.append(lines[i][2:])
                cell = MarkdownCell('id', source)
                cells.append(cell)
                i += 1 
            
            elif lines[i] == '# %%':
                source = []
                while lines[i+1] != '' and i+1 < len(lines):
                    i += 1
                    source.append(lines[i][2:])
                cell = CodeCell('id', source, 'execution_count')
                cells.append(cell)
                i += 1
            
            i += 1
        
        return Notebook(self.version, cells)