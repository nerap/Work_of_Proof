from hashlib import sha256
import time
from enum import Enum
from srcs.Transactions.Input import Input
from srcs.Transactions.Output import Output

class Status(Enum):
    CREATING = 'Creating'
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'

class Transactions:

    __slots__ = '_hash', '_status', '_timestamp', '_confirmations', '_inputs', '_outputs'

    def __init__(self, inputs, outputs, status=Status.CREATING, timestamp=None, confirmations=0) -> None:
        self._inputs = inputs
        self._outputs = outputs
        self._timestamp = timestamp or int(time.time())
        self._status = status.value
        self._hash = None
        self._confirmations = confirmations


    @property
    def hash(self):
        if self._hash:
            return self._hash
        input_hash = sha256((str([inputs.as_dict for inputs in self._inputs]) + str(self._timestamp)).encode()).hexdigest()
        for output in self._outputs:
            output._input_hash = input_hash
        hash_string = '{}{}{}'.format([inputs.as_dict for inputs in self._inputs], [outputs.as_dict for outputs in self._outputs], self._timestamp)
        self._hash = sha256(sha256(hash_string.encode()).hexdigest().encode('utf8')).hexdigest()
        return self._hash

    @property
    def as_dict(self) -> dict:
        input_hash = sha256((str([inputs.as_dict for inputs in self._inputs]) + str(self._timestamp)).encode()).hexdigest()
        for output in self._outputs:
            output._input_hash = input_hash
        return {
            "_status" : self._status,
            "_timestamp" : self._timestamp,
            "_confirmations" : self._confirmations,
            "_inputs" : [inputs.as_dict for inputs in self._inputs],
            "_outputs" : [outputs.as_dict for outputs in self._outputs],
            "_hash" : self.hash
        }

    @classmethod
    def from_dict(cls, data):
        _inputs = [Input.from_dict(inputs) for inputs in data['_inputs']]
        _outputs = [Output.from_dict(outputs) for outputs in data['_outputs']]

        input_hash = sha256((str([inputs.as_dict for inputs in _inputs]) + str(data['timestamp'])).encode()).hexdigest()
        for output in _outputs:
            output._input_hash = input_hash
        inst = cls(
            _inputs,
            _outputs,
            data['_status'],
            data['_timestamp'],
            data['_confirmations'],
        )
        inst._hash = None
        return inst