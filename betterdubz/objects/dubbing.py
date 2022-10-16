from PyQt5.QtCore import QPoint, QRect
import ffmpeg

class DubUnit():

    def __init__(self, original: str, pos: QPoint, startTime: int, audio: str = None, dubbed: str = None):
        self.original = original
        self.pos = pos
        self.startTime = startTime
        self.audio = audio
        self.dubbed = dubbed
        pass

    @classmethod
    def fromFile(cls, filename: str, bound: QRect, start: int, end: int):
        cropped_fname = "cache/cropped-%d-%d-%s-%s.mp4" % \
                        (start, end, (str(bound.bottom()) + str(bound.left())), (str(bound.top()) + str(bound.right())))
        stream = ffmpeg.input(filename)\
            .crop(bound.left(), bound.top(), bound.width(), bound.height())\
            .trim(start="%dms" % start, end="%dms" % end)\
            .output(cropped_fname)\
            .run()
        return cls(cropped_fname, bound.topLeft(), start)

    def to_dict(self):
        # set to dubbed later
        return {"%s" % self.dubbed: [self.startTime, self.pos]}