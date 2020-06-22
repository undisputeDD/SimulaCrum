class Button:
    def __init__(self, msg, x, y, w, h, ic, ac, startText, textSurf, textRect, action=None, image=None):
        self._msg = msg
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._ic = ic
        self._ac = ac
        self._startText = startText
        self._textSurf = textSurf
        self._textRect = textRect
        self._action = action
        self._image = image

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_w(self):
        return self._w

    def get_h(self):
        return self._h

    def get_ic(self):
        return self._ic

    def get_ac(self):
        return self._ac

    def get_startText(self):
        return self._startText

    def get_textSurf(self):
        return self._textSurf

    def get_textRect(self):
        return self._textRect

    def get_action(self):
        return self._action

    def get_image(self):
        return self._image

    def perform_action(self):
        self._action()
