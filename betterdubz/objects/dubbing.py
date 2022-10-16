from PyQt5.QtCore import QPoint, QRect
import ffmpeg
from betterdubz.API.w2l_api import W2LAPI

w2l = W2LAPI()

class DubUnit():

    def __init__(self, original: str, pos: QPoint, startTime: int, audio: str = None, dubbed: str = None):
        self.original = original
        self.pos = pos
        self.startTime = startTime
        self.audio = audio
        self.dubbed = dubbed

    def render(self):
        output = "dubs/%s" % (self.original.split("/")[-1]).split('.')[:-1] + '-dubbed.mp4'
        audio_trimmed = "cache/%s" % self.audio.split("/")[-1]
        metadata = ffmpeg.probe(self.original)
        duration = metadata['streams'][0]['duration']
        ffmpeg.input(self.audio).audio.filter('atrim', duration=duration).output(audio_trimmed).run()
        w2l.get_dubbed(self.original, audio_trimmed, output)
        self.dubbed = output

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
        return {"%s" % self.dubbed: [self.startTime, self.pos]}