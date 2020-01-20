from mentormatch.pairs.pair_base import BasePair
from mentormatch.pairs import checks


class RandomPair(BasePair):

    @property
    def compatible(self) -> bool:
        return all((
            super().compatible,
            checks.mentee_sees_no_dealbreakers(self.mentor, self.mentee),
            self.level_delta >= 0,
            self.years_delta >= 0,
        ))

    @property
    def preferred(self):
        return False

    @property
    def random(self):
        return True
