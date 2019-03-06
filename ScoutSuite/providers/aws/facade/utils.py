import boto3

from ScoutSuite.providers.utils import run_concurrently


# TODO: Add docstrings
class AWSFacadeUtils:
    _clients = {}

    @staticmethod
    async def get_all_pages(service: str, region: str, paginator_name: str, response_key: str, **paginator_args):
        client = AWSFacadeUtils.get_client(service, region)
        # Building a paginator doesn't require any API call so no need to do it concurrently:
        paginator = client.get_paginator(paginator_name).paginate(**paginator_args)

        # Getting all pages from a paginator requires API calls so we need to do it concurrently:
        return await run_concurrently(lambda: AWSFacadeUtils._get_all_pages_from_paginator(paginator, response_key))

    @staticmethod
    def _get_all_pages_from_paginator(paginator, key):
        resources = []
        # There's an API call hidden behind each iteration:
        for page in paginator:
            resources.extend(page[key])

        return resources

    @staticmethod
    def get_client(service: str, region: str):
        # TODO: investigate the use of a mutex to avoid useless creation of a same type of client among threads:
        client = boto3.client(service, region_name=region)
        return AWSFacadeUtils._clients.setdefault((service, region), client)
