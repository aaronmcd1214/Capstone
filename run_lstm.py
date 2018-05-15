import sys


def get_data(playerID):
    df = pd.read_csv('src/data/uncondensed.csv')
    df.drop(['Unnamed: 0', 'yearID'], axis=1, inplace=True)
    df = pd.get_dummies(df, columns=['pos'])
    df.set_index('playerID', inplace=True, drop=True)

    X = df.groupby('playerID').head(6)
    y = pd.DataFrame(df['avg'].groupby('playerID').tail(6))
    # separate interested player from group
    if check_player(playerID):
        X1 = X[X.index == playerID]
        y1 = y[y.index == playerID]
    else:
        print('PlayerID not found in eligible players')


    return X, y

def check_player(df, playerID):
    exists = False
    while exists == False:
        if playerID == 'q':
            sys.exit()
        elif playerID in df.index:
            return True
        else:
            playerID = input("Please try another playerID or enter 'q' to quit: ")

def dict_convert(df):
    length = pd.value_counts(df.index)[0]
    def_dict = defaultdict(dict)
    if length == 1:
        return df.T.to_dict()
    for i in range(length):
        year = 'year' + str(i + 1)
        def_dict[year] = df.groupby('playerID').nth(i).T.to_dict('index')
    return def_dict

def format_data(X_df, y_df):
    # convert to dicts
    X_dict = dict_convert(X_df)
    y_dict = dict_convert(y_df)
    # convert to panels
    X_panel = pd.Panel(X_dict)
    y_panel = pd.Panel(y_dict)
    # convert to matrices
    X_mat = X_panel.as_matrix().astype('float32')
    y_mat = y_panel.as_matrix().astype('float32')
    # reorganize axis
    X_mat = np.moveaxis(X_mat, 0, 1)
    y_mat = np.moveaxis(y_mat, 0, 1)

    return X_mat, y_mat

if __name__ == '__main__':
    playerID = sys.argv[1]
    X_df_all, y_df_all, X_df_1, y_df_1 = get_data(playerID) # get initial dataset and format
    X_format, y_format = format_data(X_df, y_df) # format dataset
