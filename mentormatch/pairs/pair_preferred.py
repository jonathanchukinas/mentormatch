from mentormatch.pairs.pair_base import BasePair


class PreferredPair(BasePair):

    @property
    def preferred(self):
        return True

    @property
    def random(self):
        return False
