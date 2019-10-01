from src.services.raw_compiler_service import RawCompilerService
from src.services.raw_data_fetcher_service import RawDataFetcherService


class ServiceFactory:
    @staticmethod
    def get_raw_compiler_service():
        return RawCompilerService()

    @staticmethod
    def get_raw_data_fetcher_service():
        return RawDataFetcherService()
