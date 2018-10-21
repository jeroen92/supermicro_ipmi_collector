import prometheus_client
import typing

from smipmic.core.config import ApplicationConfig
from smipmic.metrics.base import BaseMetric
from smipmic.metrics.registry import MetricRegistry

class PsuMetricRegistry(MetricRegistry):

    REGISTRY = dict()

    @classmethod
    def register(cls, attribute: str):

        def _wrapper(metric_cls):
            cls.REGISTRY[attribute] = metric_cls

        return _wrapper


@PsuMetricRegistry.register(attribute='Temperature 1')
class Temperature(BaseMetric):
    METRIC = prometheus_client.Gauge('smipmic_psu_temperature_celsius', 'PSU Temperature', ['fqdn', 'instance'])
    RE_VALUE = '(\d+)(?=C)'

@PsuMetricRegistry.register(attribute='Main Output Power')
class OutputPower(BaseMetric):
    METRIC = prometheus_client.Gauge('smipmic_psu_output_power_watts', 'PSU Output Power', ['fqdn', 'instance'])
    RE_VALUE = '(\d+)(?=\sW)'

@PsuMetricRegistry.register(attribute='Input Power')
class InputPower(BaseMetric):
    METRIC = prometheus_client.Gauge('smipmic_psu_input_power_watts', 'PSU Input Power', ['fqdn', 'instance'])
    RE_VALUE = '(\d+)(?=\sW)'

@PsuMetricRegistry.register(attribute='Fan 1')
class FanSpeed(BaseMetric):
    METRIC = prometheus_client.Gauge('smipmic_psu_fan_speed_rpm', 'PSU Fan Speed', ['fqdn', 'instance'])
    RE_VALUE = '(\d+)(?=\s)'
