#!/usr/bin/env python3
"""
Author : brandon <brandon@localhost>
Date   : 2022-06-14
Purpose: Parse Autosys Job Instruction Language (JIL) files
"""

import argparse
import sys
import io
import os
from xml.etree.ElementTree import tostring


# --------------------------------------------------
class Job:
    name = ''
    command = ''

def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Job Instruction Language Parser',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('text',
                        metavar='text',
                        type=str,
                        help='Input string or file')

    parser.add_argument('-o',
                        '--outfile',
                        help='Output filename',
                        metavar='str',
                        type=str,
                        default='')

    args = parser.parse_args()

    if os.path.isfile(args.text):
        args.text = open(args.text)
    else:
        args.text = io.StringIO(args.text + '\n')

    return args


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    job_dict = {}
    
    out_fh = open(args.outfile, 'wt') if args.outfile else sys.stdout
    lineNum = 0
    job = Job()

    for line in args.text:
        lineNum = lineNum + 1

        if 'Job:' in line:
	        job.name = line[5:]
        elif 'Command:' in line:
	        job.command = line[9:]
        elif '/*' in line:
            job = Job()
        elif ':' not in line:
            job_dict[job.name] = job
        
        out_fh.write(line.upper())
    
    out_fh.write(str(job_dict.items()))
    out_fh.close()


# --------------------------------------------------
if __name__ == '__main__':
    main()
