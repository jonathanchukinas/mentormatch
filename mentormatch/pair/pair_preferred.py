from mentormatch.pair.pair_base import Pair


class PreferredPair(Pair):

    @property
    def preferred(self):
        return True

    @property
    def random(self):
        return False
