from commons.dataclasses import BaseDataClass
from commons.models.configuration import Configuration
from commons.patterns.runnable import Runnable


class GetAllConfigDataClass(BaseDataClass):
    configs: dict


class GetConfigurationService(Runnable):

    @classmethod
    def run(cls, key: str) -> dict:
        return Configuration.objects.get(key=key).content

    @classmethod
    def get_all_config(cls):
        results = Configuration.objects.values("key", "content")

        configs = dict()

        for result in results:
            if 'is_enabled' in result['content']:
                configs[f"is_{result['key']}_enabled"] = result['content']['is_enabled']

        return GetAllConfigDataClass(configs=configs)
