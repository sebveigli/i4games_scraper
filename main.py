from raw_data_fetcher import RawDataFetcher
from raw_compiler import RawCompiler

if __name__ == '__main__':
    print('Getting all user record data')
    RawDataFetcher.run_for_all_users()
    print('Compiling...')
    RawCompiler.compile_all_records()
    print('Done!')
