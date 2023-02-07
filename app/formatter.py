import pandas as pd 


def df_formatter(df):
    final_df = df[0:1].T
    final_df = final_df.reset_index()
    final_df.rename(columns = {'index':'Title',0:'Value'},inplace=True )
    new_list = []
    for i in range(final_df.shape[0]):
        new_list.append(f'1.1.{i+1}')
    final_df['index'] = new_list
    a = 1
    b=  2
    c = 1
    prev_search_key = final_df.iloc[0][1]
    for i in range(df.shape[0]):
        j = i + 1 
        temp_df = df[i:j].T
        temp_df = temp_df.reset_index()
        temp_df.rename(columns = {'index':'Title',i:'Value'},inplace=True )
        new_search_key = temp_df.iloc[0][1]
        if new_search_key != prev_search_key:
            a += 1
            b = 1
        index_col = []
        for c in range(1,temp_df.shape[0]+1):
            index = f'{a}.{b}.{c}'
            index_col.append(index)
        temp_df['index'] = index_col
        b += 1
        prev_search_key = new_search_key 
        final_df = final_df.append(temp_df)
    return final_df
        