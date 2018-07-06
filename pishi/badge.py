class Badge(object):
    ROYAL = 0
    FULL_HOUSE = 1
    STRAIGHT = 2
    ONE_PAIR = 3
    ORACLE = 4
    NOSTRADAMUS = 5
    TRELAWNEY = 6
    NOTHING = 8

    normal_types = (
        (ROYAL, "Royal"),
        (FULL_HOUSE, "Full House"),
        (STRAIGHT, "Straight"),
        (ONE_PAIR, "One Pair")
    )

    exceptional_types = (
        (ORACLE, "Oracle"),
        (NOSTRADAMUS, "Nostradamus"),
        (TRELAWNEY, "Trelawney"),
        (NOTHING, "Nothing")
    )

    @staticmethod
    def get_value(badge):
        if badge == Badge.ROYAL:
            return BadgeScore.ROYAL
        if badge == Badge.FULL_HOUSE:
            return BadgeScore.FULL_HOUSE
        if badge == Badge.STRAIGHT:
            return BadgeScore.STRAIGHT
        if badge == Badge.ONE_PAIR:
            return BadgeScore.ONE_PAIR
        if badge == Badge.ORACLE:
            return BadgeScore.ORACLE
        if badge == Badge.NOSTRADAMUS:
            return BadgeScore.NOSTRADAMUS
        if badge == Badge.TRELAWNEY:
            return BadgeScore.TRELAWNEY
        return 0

    @staticmethod
    def get_probability(badge):
        if badge == Badge.ORACLE:
            return BadgeProbability.ORACLE
        if badge == Badge.NOSTRADAMUS:
            return BadgeProbability.NOSTRADAMUS
        if badge == Badge.TRELAWNEY:
            return BadgeProbability.TRELAWNEY
        return BadgeProbability.ALL

    index_dict = {
        "ROYAL": ROYAL,
        "FULL_HOUSE": FULL_HOUSE,
        "STRAIGHT": STRAIGHT,
        "ONE_PAIR": ONE_PAIR,
        "ORACLE": ORACLE,
        "NOSTRADAMUS": NOSTRADAMUS,
        "TRELAWNEY": TRELAWNEY
    }


class BadgeScore(object):
    ROYAL = 20
    FULL_HOUSE = 12
    STRAIGHT = 8
    ONE_PAIR = 2
    ORACLE = 20
    NOSTRADAMUS = 15
    TRELAWNEY = 10
    PENALTY = 5


class BadgeProbability(object):
    ORACLE = 0.1
    NOSTRADAMUS = 0.2
    TRELAWNEY = 0.3
    ALL = 1