import pandas as pd
import re

def list_country_codes(country_codes):

    print('df scrapping good')
    list_country_codes = [c.text.strip().split('\n') for c in country_codes]
    list_country_codes2 = [[l for l in sub if len(l) > 1] for sub in list_country_codes]
    list_country_codes3 = [l for sub in list_country_codes2 for l in sub]
    codes_raw = []
    countries = []
    for i in list_country_codes3:
        if len(i) < 5 or i == '(XK[1])' or i == '(CN_X_HK)':
            codes_raw.append(i)
        else:
            countries.append(i)
    codes_str = ''.join(codes_raw)
    codes = re.sub(r'[^a-zA-Z ]', ' ', codes_str).split()
    codes[57] = 'CN_X_HK'
    del codes[58]
    del codes[58]
    codes_df = pd.DataFrame(codes)
    countries_df = pd.DataFrame(countries)
    country_codes_info = pd.concat([codes_df, countries_df.reindex(codes_df.index)], axis=1)
    country_codes_info.columns = ['country_code', 'country']

    return country_codes_info

def merge(country_codes_info, country_info, data_jobs, career_info):

    print('merge ok')
    df_merge_countries = pd.merge(country_codes_info,
                                  country_info,
                                  on='country_code')
    df_merge_countries = df_merge_countries[['uuid', 'country_code', 'country', 'rural']]
    df_merge_jobs = pd.merge(data_jobs, career_info, how='inner', left_on=['uuid'], right_on=['normalized_job_code'])
    df_merge_jobs['quantity'] = df_merge_jobs.groupby('normalized_job_code')['normalized_job_code'].transform('count')
    df_merge_jobs['percentage'] = (100 * (df_merge_jobs['quantity'] / df_merge_jobs['quantity'].sum())).round(6).astype(
        str) + '%'
    df_raw = pd.merge(df_merge_countries, df_merge_jobs, left_on='uuid', right_on='uuid_y')
    df_raw.drop(
        ['uuid_x', 'parent_uuid', 'error', 'uuid_y', 'dem_education_level', 'dem_full_time_job', 'normalized_job_title',
         'normalized_job_code'], axis=1, inplace=True)
    df_study = df_raw[df_raw['title'].notna()]

    return df_study



