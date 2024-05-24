class Lead:

    def __init__(self, name, prefs=None):
        self.name = name
        if prefs is None:
            self.prefs = []
        else:
            self.prefs = prefs




class Compliment:

    def __init__(self, name, prefs=None):
        self.name = name
        if prefs is None:
            self.prefs = []
        else:
            self.prefs = prefs