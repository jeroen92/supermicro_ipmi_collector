import argparse
import os
import enum


class ApplicationConfig(argparse.Namespace):
    pass

class ApplicationArguments(enum.Enum):
    DEBUG = '--debug'
    INTERVAL = '--interval'
    IPMI_FQDN = '--ipmi-host'
    IPMI_PASSWORD = '--ipmi-password'
    IPMI_USERNAME = '--ipmi-username'
    IPMITOOL_LOCATION = '--ipmitool-path'
    PROMETHEUS_HTTP_PORT = '--prometheus-http-port'

    def __repr__(self):
        return self.value

    def __str(self):
        return self.value


parser = argparse.ArgumentParser()

core_group = parser.add_argument_group('Application arguments')

core_group.add_argument(ApplicationArguments.DEBUG.value,
                        action='store_true',
                        help='Increase verbosity to debug level',
                        default=False,
                        dest=ApplicationArguments.DEBUG.name)

core_group.add_argument(ApplicationArguments.INTERVAL.value,
                        action='store',
                        type=int,
                        help="The interval in seconds to query for new metrics. Defaults to 60 seconds",
                        dest=ApplicationArguments.INTERVAL.name,
                        default=os.getenv(ApplicationArguments.INTERVAL.name, 60))


backend_group = parser.add_argument_group('IPMI interface arguments')

backend_group.add_argument(ApplicationArguments.IPMI_FQDN.value,
                    action='store',
                    help="The hostname or IP address of the IPMI interface",
                    dest=ApplicationArguments.IPMI_FQDN.name,
                    default=os.getenv(ApplicationArguments.IPMI_FQDN.name, None))

backend_group.add_argument(ApplicationArguments.IPMI_PASSWORD.value,
                    action='store',
                    help="The password to use for authentication against the IPMI interface",
                    dest=ApplicationArguments.IPMI_PASSWORD.name,
                    default=os.getenv(ApplicationArguments.IPMI_PASSWORD.name, None))

backend_group.add_argument(ApplicationArguments.IPMI_USERNAME.value,
                    action='store',
                    help="The username to use for authentication against the IPMI interface",
                    dest=ApplicationArguments.IPMI_USERNAME.name,
                    default=os.getenv(ApplicationArguments.IPMI_USERNAME.name, None))

backend_group.add_argument(ApplicationArguments.IPMITOOL_LOCATION.value,
                    action='store',
                    help="Location of the SMCIPMITool.jar",
                    dest=ApplicationArguments.IPMITOOL_LOCATION.name,
                    required=True,
                    default=os.getenv(ApplicationArguments.IPMITOOL_LOCATION.name, None))

prometheus_group = parser.add_argument_group('Prometheus arguments')

prometheus_group.add_argument(ApplicationArguments.PROMETHEUS_HTTP_PORT.value,
                    action='store',
                    type=int,
                    help="The HTTP port to use for exposing Prometheus metrics",
                    dest=ApplicationArguments.PROMETHEUS_HTTP_PORT.name,
                    default=os.getenv(ApplicationArguments.PROMETHEUS_HTTP_PORT.name, 8000))


parser.parse_args(namespace=ApplicationConfig)
