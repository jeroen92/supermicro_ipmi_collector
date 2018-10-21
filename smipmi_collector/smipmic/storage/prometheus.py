import prometheus_client
import logging

from smipmic.core.config import ApplicationConfig
from smipmic.storage.backend import StorageBackend


LOG = logging.getLogger(__name__)


class PrometheusStorageBackend(StorageBackend):

    @staticmethod
    def start():
        LOG.debug('Starting the Prometheus HTTP server')
        prometheus_client.start_http_server(ApplicationConfig.PROMETHEUS_HTTP_PORT)
        LOG.info('Succesfully started the Prometheus HTTP server')
