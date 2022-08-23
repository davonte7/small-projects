# Top Level
import argparse
import logging # comment at end
import numpy as np 
from sklearn.ensemble import RandomForestClassifier
from sched import scheduler
# Commented Out import nmap
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def cli() -> argparse.Namespace:
    """CLI interface."""
    parser = argparse.ArgumentParser()

    parser.add_argument("--n-estimators", type=int, required=True)
    parser.add_argument("--n-samples", type=int, required=True)

    return parser.parse_args()


def main() -> None:
    """Main program."""

    # Parse CLI
    args = cli()

    # Generate data    
    logger.info("Generating data")
    X = np.random.normal(0, 1, (args.n_samples, 2))
    y = np.random.binomial(1, 0.5, args.n_samples)

    # Classifier
    logger.info("Training model")
    clf = RandomForestClassifier(n_estimators=args.n_estimators).fit(X, y)

    # Make predictions
    logger.info("Making predictions")
    y_score = clf.predict_proba(X)
    print(y_score)

    # Random imports here
    import io
    import pandas as pd
    pd.bdate_range()
    # Duplicate import here
    import numpy as np
    # Unused
    import dbm


if __name__ == "__main__":
    # Random import here
    from os import path
    import sys

    main()
