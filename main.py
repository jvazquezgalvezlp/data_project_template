import argparse
import p_acquisition.m_acquisition as acq
import p_wrangling.m_wrangling as wra
import p_analysis.m_analysis as anal


def argument_parser():
    '''
    parser arguments
    '''

    parser = argparse.ArgumentParser(description = 'parse arguments')

    parser.add_argument('-p', '--path', help= 'specify the path of the database', type = str, required = True)

    args = parser.parse_args()

    return args

def main(arguments):
    print('project starting')

    path = arguments.path

    country_info, career_info = acq.import_databases(path)
    data_jobs = acq.df_api(career_info)
    country_codes = acq.df_webscraping()
    country_codes_info = wra.list_country_codes(country_codes)
    df_study = wra.merge(country_codes_info, country_info, data_jobs, career_info)
    df_possible_hires = anal.answer(df_study)


    print('finished process')


if __name__ == '__main__':
    arguments= argument_parser()
    main(arguments)

