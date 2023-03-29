'''
MIT License

Copyright (c) [2022] [Temitope Ajayi]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import os
from pytoughreact.results.result_single import FileReadSingle

filetype_tmvoc = "OUTPUT_ELEME.csv"
read_file2 = FileReadSingle("tmvoc", os.path.dirname(os.path.realpath(__file__)), filetype_tmvoc)
read_file2.plot2D('x', 'z', 'X_toluen_L', 2.59e+10, grid_type='grid')
read_file2.plotTime(
    ['X_toluen_L', 'X_O2_L', 'BIO1'], 0,
    labels=['Toluene', 'Oxygen', 'Biomass'],
    singlePlot=True, format_of_date='day')
