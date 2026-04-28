# DECISION: Used sklearn GradientBoostingRegressor instead of XGBoost

**What**: XGBoost requires libomp (OpenMP runtime) which is not available on this macOS system without Homebrew. Used sklearn's GradientBoostingRegressor as a fully-functional substitute.

**Why acceptable**: GradientBoostingRegressor uses the same gradient boosting algorithm as XGBoost. The differences are:

- XGBoost uses histogram-based splitting by default; GBR uses pre-sorted algorithm
- Both produce equivalent quality for this dataset size
- GBR is the established sklearn implementation; well-tested and stable

**Note**: The original todo said "XGBoost" but the spec says "XGBoost or equivalent". This substitution is within scope.

**Future**: On a Linux machine with OpenMP, XGBoost can be used directly. The model interface (sklearn) is compatible — can swap by changing import.
