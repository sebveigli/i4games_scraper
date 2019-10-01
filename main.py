from src.service_factory import ServiceFactory

if __name__ == '__main__':
    rdfs = ServiceFactory.get_raw_data_fetcher_service()
    rcs = ServiceFactory.get_raw_compiler_service()
    print('Getting all user record data')
    rdfs.run_for_all_users()
    print('Compiling...')
    rcs.compile_all_records()
    print('Done!')
