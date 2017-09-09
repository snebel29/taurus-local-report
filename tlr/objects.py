import os
import numpy as np
import pandas as pd
from glob import glob

import plotly
from plotly.graph_objs import Scatter, Layout

from tlr.errors import \
    InvalidArtifactsDirError, \
    InvalidJtlFileError

class ArtifactsDir(object):
    '''Represents the taurus artifacts directory (jmeter)'''

    def __init__(self, path):
        self.path = path

        if not os.path.isdir(self.path):
            raise InvalidArtifactsDirError(
                'The directory {0} is invalid'.format(self.path)
            )

    def process(self, chunks):
        '''Process the directory and produce the necessary data structures'''
        #TODO: Make it work with multiple kpi files

        for file in glob(self.path + '/kpi*.jtl'):

            print('Processing {}...'.format(file))
            csv = pd.read_csv(file)
            df = []

            if not chunks:
                chunks = csv['elapsed'].count()

            for chunk in np.array_split(csv.iloc[:, 0:2], chunks):
                mean = lambda x: int(round(np.mean(x)))

                #TODO: If granularity is max only plot elapsed time
                # since there is no min, max
                df1 = {
                    'timeStamp': mean(chunk['timeStamp']),
                    'max': max(chunk['elapsed']),
                    'mean': mean(chunk['elapsed']),
                    'min': min(chunk['elapsed'])
                }

                df.append(df1)

            df = pd.DataFrame(df)
            return df


class Report(object):
    def __init__(self, df):
        self.df = df

    def create(self, rp):

        #TODO: Add granularity value to the plot graph
        #TODO: Print time as timestamp
        #TODO: Integrate multiple files (hide/unhide)
        #TODO: Integrate other values such as cpu, mem usage or a 
        #####  functional value (processed entities)?
        #TODO: Express Y values as ms in the plot

        self.report_file = rp
        x = self.df['timeStamp']
        scatters = [
            #TODO: Simplify Scatter structures
            Scatter(
                x = x,
                y = self.df['min'],
                name = 'Min value',
                mode = 'lines',
                fill = 'tonexty',
                line=dict(
                    width=0.5
                )
            ),
            Scatter(
                x = x,
                y = self.df['mean'],
                name = 'Arithmetic mean',
                mode = 'lines',
                fill = 'tonexty',
                line=dict(
                    width=0.5
                )
            ), 
            Scatter(
                x = x,
                y = self.df['max'],
                name = 'Max value',
                mode = 'lines',
                fill = 'tonexty',
                    line=dict(
                    width=0.5
                )
            )
        ]

        plotly.offline.plot({
                'data': scatters,
                'layout': Layout(
                    title = 'req process time (ms)',
                    xaxis = {
                        'tickmode': 'auto',
                        'nticks': 20
                    }
                )
            },
            auto_open = False,
            filename = os.path.join(self.report_file)
        )

class Publisher(object):
    pass