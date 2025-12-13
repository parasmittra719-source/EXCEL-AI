class CampaignManager:
    """Organize selected products, generated content, and prepare campaigns.

    This class ties together the outputs of the `ProductScorer`, `SalesStrategist`,
    and `ContentGenerator` modules. It stores a list of selected product entries
    (each entry is a dict with product metadata and a generated score) and can
    produce a simple campaign package consisting of marketing angles and copy.
    """

    def __init__(self):
        # In a real implementation this could be persisted to a DB or file.
        self.campaigns = []

    def add_product(self, product_info: dict, score: float, strategist, content_gen):
        """Add a product to the campaign list.

        Parameters
        ----------
        product_info: dict
            Information about the product (e.g., name, url, affiliate link).
        score: float
            Score from `ProductScorer`.
        strategist: SalesStrategist instance
            Used to generate audience profile and angles.
        content_gen: ContentGenerator instance
            Used to generate copy based on the angles.
        """
        # Generate audience profile (placeholder demographics/interests)
        demographics = product_info.get("demographics", {"age_range": "all", "location": "global", "gender": "any"})
        interests = product_info.get("interests", [])
        audience_profile = strategist.profile_audience(demographics, interests)
        angles = strategist.generate_angles(product_info.get("name", "Product"), audience_profile)
        # For simplicity, generate copy for the first angle only.
        copy = content_gen.generate_sales_copy(product_info.get("name", "Product"), angles[0], audience_profile["description"])
        campaign_entry = {
            "product": product_info,
            "score": score,
            "audience_profile": audience_profile,
            "angles": angles,
            "copy": copy,
        }
        self.campaigns.append(campaign_entry)
        return campaign_entry

    def list_campaigns(self):
        """Return a list of all prepared campaign entries."""
        return self.campaigns

    def export_campaigns(self, format: str = "json"):
        """Export campaigns to the requested format.

        Currently supports JSON (default) and a simple markdown report.
        """
        import json
        if format == "json":
            return json.dumps(self.campaigns, indent=2)
        elif format == "markdown":
            lines = []
            for idx, camp in enumerate(self.campaigns, 1):
                lines.append(f"## Campaign {idx}: {camp['product'].get('name', 'Unnamed')}\n")
                lines.append(f"**Score:** {camp['score']}\n")
                lines.append(f"**Audience:** {camp['audience_profile']['description']}\n")
                lines.append("**Angles:**\n")
                for a in camp['angles']:
                    lines.append(f"- {a}\n")
                lines.append("**Copy:**\n")
                lines.append(f"{camp['copy']}\n")
                lines.append("---\n")
            return "\n".join(lines)
        else:
            raise ValueError(f"Unsupported export format: {format}")

# Example usage (remove in production)
if __name__ == "__main__":
    from sales_agent.modules.strategist import SalesStrategist
    from sales_agent.modules.content_generator import ContentGenerator
    manager = CampaignManager()
    strategist = SalesStrategist()
    content_gen = ContentGenerator()
    product = {
        "name": "SuperFit Tracker",
        "demographics": {"age_range": "25-34", "location": "USA", "gender": "any"},
        "interests": ["fitness", "wellness"]
    }
    entry = manager.add_product(product, score=0.85, strategist=strategist, content_gen=content_gen)
    print(manager.export_campaigns("markdown"))
