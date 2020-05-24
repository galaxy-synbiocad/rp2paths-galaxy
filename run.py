#!/usr/bin/env python3

from shutil import move as shutil_move
from tempfile import TemporaryDirectory as tempfile_tempdir
from argparse import ArgumentParser as argparse_ArgParser
from os import path as os_path
from sys import path as sys_path
sys_path.insert(0, '/home/src')
from RP2paths import entrypoint as tool_entrypoint
from RP2paths import NoScopeMatrix as tool_exception



if __name__ == "__main__":

    parser = argparse_ArgParser('Python wrapper for the python RP2paths script')
    parser.add_argument('-_file_rp2_pathways', type=str)
    parser.add_argument('-rp2paths_pathways', type=str)
    parser.add_argument('-rp2paths_compounds', type=str)
    parser.add_argument('-timeout', type=int)
    parser.add_argument('-server_url', type=str)
    parser.add_argument('-galaxy', type=str)
    params = parser.parse_args()

    if (params.timeout < 0):
        logging.error('Time out cannot be less than 0: '+str(params.timeout))
        exit(1)

    with tempfile_tempdir() as tmpdirname:
        args = [
            'all',
            params._file_rp2_pathways,
            '--outdir', tmpdirname,
            '--timeout', str(params.timeout)
            ]

        try:
            tool_entrypoint(args)
            shutil_move(tmpdirname+'/out_paths.csv', params.rp2paths_pathways)
        except tool_exception:
            # No solution found, then create empty file
            open(params.rp2paths_pathways,"w+").close()
        shutil_move(tmpdirname+'/compounds.txt', params.rp2paths_compounds)
