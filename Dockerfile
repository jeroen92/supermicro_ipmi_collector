FROM python:3.7

ARG SMCIPMITOOL_PATH

ENV PATH="/ipmitool/jre/bin:${PATH}"

EXPOSE 8000/tcp

WORKDIR /tmp

ADD $SMCIPMITOOL_PATH /ipmitool
ADD smipmi_collector /smipmi_collector

RUN pip install prometheus_client
RUN pip install /smipmi_collector

ENTRYPOINT ["smipmi_collector", "--ipmitool-path", "/ipmitool/SMCIPMITool.jar"]
