from mentormatch.pair.pair_base import Pair
from mentormatch.pair_compatibility import pair_checker_no_preference


class RandomPair(Pair):

    @property
    def compatible(self) -> bool:
        raise NotImplementedError

    @property
    def preferred(self):
        return False

    @property
    def random(self):
        return True
