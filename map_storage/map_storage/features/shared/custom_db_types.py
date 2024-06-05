import pickle
from io import BytesIO
from typing import Optional, Sequence

import cv2
import numpy as np
from sqlalchemy import LargeBinary
from sqlalchemy.types import TypeDecorator


class NumpyArray(TypeDecorator):
    impl = LargeBinary

    def process_bind_param(self, value, dialect):
        if value is None:
            return value

        np_bytes = BytesIO()
        np.save(np_bytes, value, allow_pickle=True)
        return np_bytes.getvalue()

    def process_result_value(self, value, dialect):
        if value is None:
            return value

        np_bytes = BytesIO(value)
        return np.load(np_bytes, allow_pickle=True)


class SURFKeyPoints(TypeDecorator):
    impl = LargeBinary

    def process_bind_param(self,
                           value: Sequence[cv2.KeyPoint],
                           dialect) -> Optional[bytes]:
        if value is None:
            return value

        tuples = [(kp.pt, kp.size, kp.angle, kp.response, kp.octave, kp.class_id)
                  for kp in value]

        return pickle.dumps(tuples)

    def process_result_value(self,
                             value: bytes,
                             dialect) -> Optional[Sequence[cv2.KeyPoint]]:
        if value is None:
            return value

        tuples = pickle.loads(value)

        return [cv2.KeyPoint(
                    x=t[0][0], y=t[0][1],
                    size=t[1],
                    angle=t[2],
                    response=t[3],
                    octave=t[4],
                    class_id=t[5]
                )
                for t in tuples]
