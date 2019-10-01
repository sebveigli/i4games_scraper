import pandas as pd

from src.repositories.i4g_repository import i4gRepository


class RawDataFetcherService:
    @staticmethod
    def run_for_all_users():
        latest_user = i4gRepository.get_most_recent_user()

        print('Most recently registered user is {0}, searching from UID 1 -> {0}'.format(latest_user))
        for user_id in range(1, latest_user + 1):
            RawDataFetcherService.run_for_user(user_id)

    @staticmethod
    def run_for_user(user_id):
        i4g_repo = i4gRepository(user_id)

        print(f'Fetching records for user {user_id}')
        records = i4g_repo.get_all_records()

        if len(records) > 0:
            df = pd.DataFrame.from_records(records)

            df.to_csv('raw\\{}.csv'.format(user_id), index=False)
