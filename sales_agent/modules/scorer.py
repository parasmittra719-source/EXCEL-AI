import pandas as pd

class ProductScorer:
    """Score products for affiliate marketing potential.

    The scoring algorithm combines:
    - demand_score: a numeric indicator of market demand (e.g., search volume).
    - commission_rate: expected commission percentage or flat amount.
    - competition_score: a measure of how saturated the niche is (lower is better).

    The final score is higher for products with high demand, good commission, and low competition.
    """

    def __init__(self, weight_demand: float = 0.5, weight_commission: float = 0.3, weight_competition: float = 0.2):
        self.weight_demand = weight_demand
        self.weight_commission = weight_commission
        self.weight_competition = weight_competition

    def compute_score(self, demand: float, commission: float, competition: float) -> float:
        """Calculate a composite score.

        Parameters
        ----------
        demand: float
            Normalized demand metric (0-1).
        commission: float
            Normalized commission metric (0-1).
        competition: float
            Normalized competition metric (0-1, where lower is better).
        """
        # Invert competition so that lower competition yields higher contribution
        competition_inv = 1 - competition
        score = (
            self.weight_demand * demand +
            self.weight_commission * commission +
            self.weight_competition * competition_inv
        )
        return round(score, 4)

    def score_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add a `score` column to a DataFrame containing product metrics.

        Expected columns in `df`:
        - `demand_score`
        - `commission_rate`
        - `competition_score`
        """
        required_cols = {'demand_score', 'commission_rate', 'competition_score'}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            raise ValueError(f"Missing required columns for scoring: {missing}")
        df = df.copy()
        df['score'] = df.apply(
            lambda row: self.compute_score(
                demand=row['demand_score'],
                commission=row['commission_rate'],
                competition=row['competition_score']
            ),
            axis=1
        )
        # Sort by highest score first
        df.sort_values('score', ascending=False, inplace=True)
        return df

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    sample_data = pd.DataFrame({
        "product": ["A", "B", "C"],
        "demand_score": [0.8, 0.6, 0.9],
        "commission_rate": [0.1, 0.15, 0.08],
        "competition_score": [0.4, 0.7, 0.3]
    })
    scorer = ProductScorer()
    scored = scorer.score_dataframe(sample_data)
    print(scored)
