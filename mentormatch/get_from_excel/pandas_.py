import pandas as pd
import pathlib
import xlrd
from rtm.main.exceptions import RTMValidatorError

from mentormatch.get_from_excel.find_header_row import find_header_row


def get_df(excel_path, excel_sheet_name, header_row=1):
    try:
        return pd.read_excel(
            io=excel_path,
            sheet_name=excel_sheet_name,
            header=header_row-1,
            dtype=object,
        )
    except FileNotFoundError:
        raise RTMValidatorError(f'<{excel_path}> not valid file.')
    except xlrd.biffh.XLRDError:
        raise RTMValidatorError(f"<{excel_sheet_name}> sheet not found")


if __name__ == '__main__':
    path = pathlib.Path(__file__).parent.parent.parent/'test_rtm.xlsx'
    sheet_name = 'pandas_experiment'
    headers = 'hello good bye'.split()
    try:
        header_row = find_header_row(path, sheet_name, headers)
        df = get_df(path, sheet_name, header_row)
        print(df)
    except RTMValidatorError as e:
        print(e)


# import pandas as pd
#
# d = {'one' : pd.Series([1., 2., 3.],     index=['a', 'b', 'c']),
#      'two' : pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
#
# df = pd.DataFrame(d)
#
# print("Starting with this dataframe\n", df)
#
# print("The first column is a", type(df['one']), "\nconsisting of\n", df['one'])
#
# dfToList = df['one'].tolist()
#
# dfList = list(df['one'])
#
# dfValues = df['one'].values
#
# print("dfToList is", dfToList, "and it's a", type(dfToList))
# print("dfList is  ", dfList,   "and it's a", type(dfList))
# print("dfValues is", dfValues, "and it's a", type(dfValues))
