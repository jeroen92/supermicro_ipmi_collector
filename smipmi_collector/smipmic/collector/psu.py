import logging
import time
import threading
import prometheus_client
import shutil
import os


from smipmic.core.config import ApplicationConfig
from smipmic.core.errors import CommandError, MessageParsingError, ApplicationExit
from smipmic.collector import message
from smipmic.metrics.psu import PsuMetricRegistry
from smipmic.util import command


LOG = logging.getLogger(__name__)


class PsuInstance(object):
    def __init__(self, name: str):
        self._name = name

    def update_metrics(self, message: message.PminfoMessage):
        for metric_attribute_name, metric_cls in PsuMetricRegistry.REGISTRY.items():
            metric_cls.submit_value(
                instance=self._name,
                value=message.attributes.get(metric_attribute_name))

class PsuCollector(object):

    JAVA_EXEC = shutil.which('java')
    CMD = [
            JAVA_EXEC,
            '-jar',
            ApplicationConfig.IPMITOOL_LOCATION,
            ApplicationConfig.IPMI_FQDN,
            ApplicationConfig.IPMI_USERNAME,
            ApplicationConfig.IPMI_PASSWORD,
            'shell']
    INTERVAL = 5
    SHELL_VERB = 'pminfo'

    def __init__(self):
        LOG.info('PSU collector is starting...')
        self._instances = dict()
        self._buffer_remainder = ''
        self._process = command.BackgroundProcess(self.CMD)
        self._process.init()
        self._collector_thread = threading.Thread(target=self._collect_interval)
        self._collector_thread.start()

    def _collect_interval(self):
        LOG.debug('Starting PSU shell writer thread')
        while True:
            try:
                self._process.tell(self.SHELL_VERB)
                time.sleep(self.INTERVAL)
            except CommandError as ex:
                LOG.info('PSU collector process has exited. Aborting collection of PSU metrics')
                return

    def _get_messages(self):
        messages = None
        data = self._process.get_data()
        if data is False:
            raise ApplicationExit('PSU message reader received an exit message. Exiting')
        self._buffer_remainder += data
        self._buffer_remainder, messages = message.PminfoMessage.from_data(data=self._buffer_remainder)
        return messages

    def _update_instances(self, message: message.PminfoMessage):
        instance = message.get_module()
        if instance not in self._instances:
            LOG.info('Discovered a new PSU instance with ID `{id}`'.format(
                id=instance))
            self._instances[instance] = PsuInstance(name=instance)
        self._instances[instance].update_metrics(message=message)
        

    def run(self):
        LOG.info('Succesfully started the PSU collector')
        while True:
            try:
                messages = self._get_messages()
                for message in messages:
                    message.parse()
                    self._update_instances(message=message)
            except MessageParsingError as ex:
                LOG.error(ex)
                self._buffer_remainder = ''
                continue
            except ApplicationExit as ex:
                raise ex
