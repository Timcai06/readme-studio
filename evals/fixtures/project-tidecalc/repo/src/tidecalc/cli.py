import argparse
from . import load_csv, predict


def sparkline(values):
    bars = "▁▂▃▄▅▆▇█"
    lo, hi = min(values), max(values)
    return "".join(bars[int((v - lo) / (hi - lo or 1) * 7)] for v in values)


def main(argv=None):
    p = argparse.ArgumentParser(prog="tidecalc")
    sub = p.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("predict", help="predict water levels")
    pr.add_argument("station", help="CSV of constituents: name,amplitude,phase")
    pr.add_argument("--hours", type=int, default=24)
    pr.add_argument("--step", type=float, default=1.0)
    pr.add_argument("--datum", type=float, default=0.0)
    pr.add_argument("--spark", action="store_true", help="print a one-line sparkline")
    a = p.parse_args(argv)
    hours = [i * a.step for i in range(int(a.hours / a.step) + 1)]
    levels = predict(load_csv(a.station), hours, a.datum)
    if a.spark:
        print(sparkline(levels))
    else:
        for t, h in zip(hours, levels):
            print(f"{t:5.1f}h  {h:+.3f} m")


if __name__ == "__main__":
    main()
