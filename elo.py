import math as m

def pwin(A, B):
    ''' Calculates the probability that playerA (A) will defeat playerB (B).

    @type A: float
    @param A: ELO rating for playerA
    @type B: float
    @param B: ELO rating for playerB
    @rtype: float
    @return: The probability (0-1) player A wins the match.
    '''

    return 1 / (1 + 10 ** ((B - A) / 400))


def new_elo(old_elo, pwin, score, mov=1, mvm=1, k=32):
    '''
    Calculates the new ELO rating for a match with win probability, pwin and
    actual outcome, score.

    @type old_elo: float
    @param old_elo: Initial ELO rating
    @type pwin: float
    @param pwin: The probability of winning the match (0-1)
    @type score: float
    @param score: The actual score for the match. Loss:0, Draw:0.5, Win:1
    @type mov: float
    @param mov: The margin of victory (MOV) for the match.
    @type k: float
    @param k: The k-factor for the ELO calculation.
    @rtype: float
    @return: The player's new ELO ranking.

    '''

    return old_elo + (mov * mvm) * k * (score - pwin)

def mov(cp_w, ap_w, cp_l, ap_l):
    ''' This should calculate the margin of victory (mov) for each match. The
    more you crush your opponent the more points you get.

    @type cp_w: int
    @param cp_w: The number of control points scored by the winner.
    @type ap_w: int
    @param ap_w: The number of army points destroyed by the winner.
    @type cp_l: int
    @param cp_l: The number of control points scored by the loser.
    @type ap_l: int
    @param ap_l: The number of army points destroyed by the loser.
    @rtype: float
    @return: The margin of victory (MOV) between the winner and loser.

    '''

    cp_diff = cp_w - cp_l

    # the margin of victory modifier (MOVM) from fivethirtyeight
    movm = m.log(abs(ap_w / ap_l + cp_diff) + 1)

    if movm <= 0:
        movm = 0.1

    return movm

def mvm(elo_w, elo_l):
    ''' This calculates the margin of victory mulitplier (MVM)for each match.
    The MVM is used in the score adjustment phase and multiplied by the K
    factor. So a bigger MVM means the match is worth more. When the players are
    similar in ELO the match is worth more. A high rated player stomping a
    lower rated player isn't worth much.

    '''

    # the MVM from fivethirtyeight
    corr_m = 2.2 / ((elo_w - elo_l) * 0.001 + 2.2)

    return corr_m

