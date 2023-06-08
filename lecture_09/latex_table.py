"""

written by: Oliver Cordes 2021-11-30
changed by: Oliver Cordes 2021-12-16
"""

import numpy as np



class LatexTable(object):
    def __init__(self, data,
                use_booktabs=False,
                header=None,
                header_bottom_hline=True,
                header_top_hline=False,
                footer_hline=False,
                col_type='c',
                col_descr=None,         # overwrite the col_description, default is col_type for all colums
                col_siunitx=None,
                col_precision=None,
                precision_format=True   # use the f-string notation
                ):
        """
        Initialise a LatexTable object with all data structures. The LaTeX table will be created with __str__
        or save_file method. This methods checks all parameters carefully and raises TypeError- and ValueError-error
        upon wrong used parameters.

        Parameters
        ----------
        data: list or tuple
            List of data columns.
        header: list or tuple, optional
            List of header strings to describe the tabular data. The number of entries must be
            the same as the number of data columns.
        header_bottom_hline: bool, optional
            Prints a line below the header.
        header_top_hline: bool, optional
            Prints a line above the header.
        footer_hline: bool, optional
            Prints a line at the end of the table.
        col_type: char, optional
            Type of all columns in LaTeX coding, 'l', 'c', 'r', 'S' (from siunitx).
        col_descr: list or tuple, optional
            Sets the col_type individually for all columns. The number of entries must be the same
            as the number of data columns. (There is no check of correctness!)
        col_siunitx: list, tuple or str, optional
            Sets the siunitx converter for all columns or with a list/tuple for each column individually. 
            Default ist None.
        col_precision: list, tuple or str, optional
            Sets the precision for all all columns or with a list/tuple for each column individually. 
            Default ist None.
        precision_format: bool, optional
            Style of the precision format, Default==True, use f-string-style, False is the old-Style
        """

        self._length = -1
        self._check_data(data)   # if error it will never come back ...

        # save some information
        self._data = data
        self._nritems = len(data)

        # check for booktabs package
        if use_booktabs:
            self._hline = ['\\toprule', '\\midrule', '\\bottomrule']
        else:
            self._hline = ['\\hline'] * 3


        # handle the columnn descriptions
        if col_descr is None:
            if col_type not in ['c', 'l', 'r', 'S']:
                raise ValueError(
                    'col_type must be one of \'l\',\'c\',\'r\',\'S\'')
            self._col_descr = ''.join([col_type for i in range(self._nritems)])
            self._col_type = col_type
        else:
            self._col_descr = col_descr
            self._col_type = None

        # apply a special format for siunitx declarations
        if (col_siunitx is not None) and  isinstance(col_siunitx, (list, tuple)):
            if len(col_siunitx) != self._nritems:
                raise ValueError('col_siunitx must have the same length as the number of columns')
            self._col_siunitx = col_siunitx
        else:       
            self._col_siunitx = [col_siunitx] * self._nritems

        # apply a precision formatting for columns
        if (col_precision is not None) and isinstance(col_precision, (list, tuple)):
            if len(col_precision) != self._nritems:
                raise ValueError('col_precision must have the same length as the number of columns')
            self._col_precision = col_precision
        else:
            #self._col_precision = [col_precision for i in range(self._nritems)]
            self._col_precision = [col_precision] * self._nritems

        # check for header descriptions
        if header is not None:
            if isinstance(header, (list, tuple)):
                if len(header) != self._nritems:
                    raise ValueError('header must have same length as number of columns')
                if (self._col_type is not None) and (self._col_type == 'S'):   
                    # change for siunitx
                    header = ['{%s}' % i for i in header]

            else:
                raise ValueError('header must be list or tuple')

        self._header = header
        self._header_top_hline = header_top_hline
        self._header_bottom_hline = header_bottom_hline
        self._footer_hline = footer_hline

        self._precision_format = precision_format
        

    def _check_data(self, data):
        # check if data is list or tuple
        if isinstance(data, (list, tuple)):
            self._data = data
        else:
            raise TypeError('TableData must be list or tuple')

        if len(data) == 0:
            raise TypeError('TableData is empty')

        # check if columns are lists/tuples or numpy arrays and have same length
        for i in data:
            if isinstance(i, (list, tuple, np.ndarray)):
                if isinstance(i, np.ndarray):
                    if i.ndim > 1:
                        raise TypeError('numpy array must have only one dimension')
                if self._length == -1:
                    self._length = len(i)
                else:
                    if len(i) != self._length:
                        raise TypeError('Columns have different length')
            else:
                raise TypeError('Column must be list, tuple or np.ndarray')


    def _print_header(self):
        """
        Creates the header of the table
        """
        s = '\\begin{tabular}{'+self._col_descr+'}\n'
        if self._header_top_hline:
            s += self._hline[0]+'\n'
        if self._header is not None:
            for cols in range(self._nritems):
                s += f'{self._header[cols]}'
                if cols < (self._nritems-1):
                    s += ' & '
            s += ' \\\\ \n'

        if self._header_bottom_hline:
            s += self._hline[1]+'\n'

        return s


    def _print_footer(self):
        """
        Creates the footer part of the table
        """
        s = ''
        if self._footer_hline:
            s += self._hline[2]+'\n'

        s += '\\end{tabular} \n'
        return s


    def _print_table(self):
        """
        Creates the body of the table
        """
        s = ''
        for lines in range(self._length):
            for cols in range(self._nritems):
                s += self._print_value(cols, self._data[cols][lines])
                if cols < (self._nritems-1):
                    s += ' & '
            s += ' \\\\ \n'

        return s


    def _print_value(self, col, value,):
        """
        Converts a value into something useful
        """

        if self._col_siunitx[col] is None:
            if self._col_precision[col] is None:
                s = f'{value}'
            else:
                if self._precision_format:
                    # convert with the python precision and rounding using f-string style
                    s = '{%s}' % self._col_precision[col]
                    s = s.format(value)
                else:
                    # convert with the python precision and rounding old style
                    s = self._col_precision[col] % value
        else:
            # convert with the LaTeX precision and rounding
            s = self._col_siunitx[col]+'{'f'{value}'+'}'

        return s


    def __str__(self):
        """
        Converts the data columns into a LaTeX table represented as an ascii string.
        """
        return self._print_header() + self._print_table() + self._print_footer()


    def save_file(self, filename):
        """
        Saves the table into filename.

        Parameters:
        -----------
        filename: The name of the file to save the table.
        """
        with open(filename, mode='w' ) as f:
            f.write(self.__str__())
