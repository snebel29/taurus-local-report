'''
Taurus local report plot an interactive html report object that can
be used to visualize the results of http://gettaurus.org/ jmeter executor.

The tool can publish your object to your preferred cloud object storage
- Amazon S3
- Google cloud storage
- Azure blob

as well as to your local file system...
'''
import re
import sys
import argparse
from tlr.objects import ArtifactsDir, Report


def parse_args(args):
    '''Parse the arguments'''

    class CustomArgParser(argparse.ArgumentParser):
        '''Custom Argument Parse to print help on any error'''
        def error(self, message):
            self.print_help()
            sys.exit(1)

    parser = CustomArgParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__
    )

    parser.add_argument(
        '-a',
        '--artifacts-dir',
        type=str,
        required=True,
        help='The taurus artifacts dir'
    )
    parser.add_argument(
        '-r',
        '--report-file',
        type=str,
        required=False,
        default='report.html',
        help='The report file to output'
    ),
    parser.add_argument(
        '-c',
        '--chunks',
        type=int,
        required=False,
        help='Group by producing X number of chunks with max, avg and min values'
    )

    args = parser.parse_args(args)
    report_extension = 'html'
    if not re.match( r'.+\.' + report_extension + '$', args.report_file):
        args.report_file += '.' + report_extension

    return args


def main(args):
    artifacts_dir = ArtifactsDir(args.artifacts_dir)
    df = artifacts_dir.process(args.chunks)
    Report(df).create(args.report_file)

if __name__ == '__main__':
    main(parse_args(sys.argv[1:]))
