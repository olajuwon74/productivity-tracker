import os
import sys
import pandas as pd


def fill_total_seconds(filename, output_filename):
    """
    create a new column with the cummulative sum of used seconds in the seconds columns of previous rows per day
    """

    # create temporary date column from start_timestamp
    df = pd.read_csv(filename)
    df['date'] = df['start_timestamp'].apply(lambda x: x.split(' ')[0])

    # get total seconds so far for each row per day
    df['total_seconds'] = df.groupby('date')['seconds'].cumsum()
    # drop the date column
    df.drop('date', axis=1, inplace=True)

    print("saving to ", output_filename)
    df.to_csv(output_filename, index=False)
    print('Done!')


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print('File not found!')
            sys.exit(1)
    except IndexError:
        print('Please provide a file name!')
        print('Usage: python total_seconds_filler.py <path_to_file>')
        sys.exit(1)

    output_filename = filename.split('.')[0] + '_+total_seconds.csv'
    fill_total_seconds(filename=filename, output_filename=output_filename)
