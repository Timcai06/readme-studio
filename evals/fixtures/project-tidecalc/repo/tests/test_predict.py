from tidecalc import Constituent, predict


def test_single_constituent_peaks_at_phase():
    assert predict([Constituent("M2", 1.0, 0.0)], [0])[0] == 1.0
