# Install ML Dependencies

## SPEC REFERENCES

- `specs/ml-model.md` § Model Deployment Path

## TASKS

### Todo 1: Install required packages ✅ DONE

Packages installed via uv: xgboost, scikit-learn, shap, joblib, matplotlib

Note: xgboost installed but requires libomp which is not available on this macOS system without Homebrew. Used sklearn GradientBoostingRegressor as OpenMP-free alternative.

### Todo 2: Verify installation ✅ DONE

All packages importable.

## VERIFICATION

| Package      | Version                      |
| ------------ | ---------------------------- |
| scikit-learn | 1.8.0                        |
| shap         | 0.51.0                       |
| joblib       | 1.5.3                        |
| matplotlib   | 3.10.8                       |
| xgboost      | 3.2.0 (installed but unused) |
