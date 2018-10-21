import logging
import typing
import subprocess
import threading
import queue
import time


from smipmic.core.errors import CommandError


LOG = logging.getLogger(__name__)


def run(cmd: typing.List[str]):
    try:
        LOG.debug('Running command: `{cmd}`'.format(cmd=' '.join(cmd)))
        proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    except FileNotFoundError as ex:
        raise CommandError('Command executable was not found')
    if proc.returncode:
        LOG.error('Command exited with returncode `{ret}`'.format(ret=proc.returncode))
        LOG.error('==== Starting output dump of command ====')
        for line in stderr.split('\n'):
            LOG.error('    {line}'.format(line=line.strip()))
        LOG.error('==== Ending output dump of command ====')
        raise CommandError('Command exited with returncode `{ret}`'.format(ret=proc.returncode))
    return proc.stdout


class BackgroundProcess(object):
    def __init__(self, cmd: typing.List[str]):
        self._cmd = cmd
        self._queue = queue.Queue()
        self._exit = False

    def init(self):
        LOG.debug('Starting subprocess: `{cmd}`'.format(cmd=' '.join(self._cmd)))
        self._process = subprocess.Popen(
                            self._cmd,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        thread = threading.Thread(target = self._reader)
        thread.start()

    def _log_stderr(self):
        if self._process.poll():
            LOG.error('Command exited with returncode `{ret}`'.format(ret=self._process.returncode))
            LOG.error('==== Starting output dump of command ====')
            stdout, stderr = self._process.communicate()
            for line in stderr.decode('utf-8').split('\n'):
                if not len(line):
                    continue
                LOG.error('    {line}'.format(line=line.strip()))
            LOG.error('==== Ending output dump of command ====')
            self._exit = True
            raise CommandError('Command exited with returncode `{ret}`'.format(ret=self._process.returncode))

    def _reader(self):
        while True:
            if self._process.poll() is not None:
                LOG.debug('Stdout reader detected exit of subprocess. Signaling queue peer and exiting')
                self._queue.put(False)
                return
            line = self._process.stdout.readline()
            line = line.decode('utf-8')
            self._queue.put(line)
            time.sleep(0.1)

    def tell(self, input):
        self._log_stderr()
        input += '\n'
        try:
            self._process.stdin.write(input.encode('utf-8'))
            self._process.stdin.flush()
        except BrokenPipeError as ex:
            raise CommandError('Child has exited')

    def get_data(self):
        LOG.debug('Attempting to retrieve data from the background process stdout queue')
        data = self._queue.get()
        if data is False:
            LOG.debug('Queue data reader received an exit signal from its queue peer. Exiting.')
            return False
        LOG.debug(f'Got data from stdout queue: `{data[:-1]}`')
        return data
