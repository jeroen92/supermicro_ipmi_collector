import re
import typing


from smipmic.core.errors import NotImplementedError, MessageParsingError

class Message(object):

    RE_MESSAGE = re.compile(r"^(.+)(?:\n|\r\n?)((?:(?:\n|\r\n?).+)+)", re.MULTILINE)
    MSG_KEYWORDS = list()

    def __new__(cls, data: str):
        if not cls._test(data):
            return None
        return super().__new__(cls)

    def __init__(self, data: str):
        start = self.RE_MODULE.search(data).span(0)[0]
        self._data = data[start:]
        self._attributes = dict()

    @classmethod
    def _test(cls, data: str):
        re_match = cls.RE_MODULE.search(data)
        kw_match = all([kw in data for kw in cls.MSG_KEYWORDS])
        return re_match and kw_match

    @classmethod
    def from_data(cls, data: str):
        messages = []
        remainder = ''
        for message in data.split('\n\n'):
            msg = cls(data=message)
            if not msg:
                remainder += f'{message}\n'
                continue
            remainder = ''
            messages.append(msg)
        return remainder, messages

    def parse(self):
        data = self._data.split('\n')[self.PREAMBLE_LEN:]
        for line in data:
            try:
                attr = self.RE_FIELDS.match(line).groupdict()
            except AttributeError as ex:
                raise MessageParsingError(f'Could not parse the following line: `{line}`. Skipping message.')
            self._attributes.update(**{
                attr.get('key'): attr.get('val')
            })

    @property
    def attributes(self) -> typing.Dict[str, str]:
        return self._attributes
