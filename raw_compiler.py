import csv
import pandas as pd

from os import listdir
from os.path import isfile, join


class RawCompiler:
    @staticmethod
    def compile_all_records():
        records = [f for f in listdir('raw\\') if isfile(join('raw\\', f))]

        final_df = pd.DataFrame()

        for record_file in records:
            f = open('raw\\{}'.format(record_file))
            text = csv.DictReader(f)
            df = pd.DataFrame.from_dict(text)
            f.close()

            final_df = final_df.append(df)

        final_df.to_csv('compiled\\all.csv')
