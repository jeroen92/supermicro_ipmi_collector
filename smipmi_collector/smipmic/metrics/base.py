import re

from smipmic.core.config import ApplicationConfig


class BaseMetric(object):

    RE_VALUE = '.+'

    @classmethod
    def submit_value(cls, instance: str, value: str):
        value = re.match(cls.RE_VALUE, value).group(0)
        cls.METRIC.labels(instance=instance,
                          fqdn=ApplicationConfig.IPMI_FQDN).set(value)
