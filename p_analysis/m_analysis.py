def answer(df_study):
    print('getting final answer')
    df_possible_hires_raw = df_study[df_study['title'].str.match('.*Data Analyst.*|.*Data Scientist.*|.*Data Miner.*')]
    df_possible_hires = df_possible_hires_raw[df_possible_hires_raw['rural'].str.match('rural|countryside')]
    df_possible_hires.to_csv(r'./data/result/february_amazon_rural_candidates.csv', index=False)

    return df_possible_hires