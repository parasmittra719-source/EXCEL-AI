class SalesStrategist:
    """Define target audience and generate marketing angles for a product.

    This module provides simple heuristics to create an audience profile based on
    supplied demographic data and interests, and then produces a few copy angles
    that could be used in affiliate marketing content.
    """

    def __init__(self):
        # In a real system this could load language models or templates.
        self.angle_templates = [
            "Discover how {product} can improve {benefit} for {audience}",
            "Why {audience} love {product}: {selling_point}",
            "Unlock {benefit} with {product} – perfect for {audience}",
        ]

    def profile_audience(self, demographics: dict, interests: list) -> dict:
        """Create a simple audience profile.

        Parameters
        ----------
        demographics: dict
            Keys like ``age_range``, ``location``, ``gender``.
        interests: list
            List of strings representing interests/hobbies.
        """
        profile = {
            "demographics": demographics,
            "interests": interests,
        }
        # Derive a readable description for templating.
        demo_parts = []
        for key, value in demographics.items():
            demo_parts.append(f"{key}: {value}")
        interests_str = ", ".join(interests)
        profile["description"] = f"{'; '.join(demo_parts)}; interests: {interests_str}"
        return profile

    def generate_angles(self, product_name: str, audience_profile: dict) -> list:
        """Generate marketing copy angles for a product.

        Parameters
        ----------
        product_name: str
            Name of the product to promote.
        audience_profile: dict
            Output from :meth:`profile_audience`.
        """
        # Simple heuristic: pick a benefit based on first interest.
        first_interest = audience_profile.get("interests", [""])[0]
        benefit = f"enhancing your {first_interest}" if first_interest else "adding value"
        selling_point = f"its unique features for {first_interest}" if first_interest else "its great features"
        audience_desc = audience_profile.get("description", "the target audience")
        angles = []
        for tmpl in self.angle_templates:
            angles.append(
                tmpl.format(
                    product=product_name,
                    benefit=benefit,
                    audience=audience_desc,
                    selling_point=selling_point,
                )
            )
        return angles

# Example usage (remove in production)
if __name__ == "__main__":
    strategist = SalesStrategist()
    demo = strategist.profile_audience(
        demographics={"age_range": "25-34", "location": "USA", "gender": "any"},
        interests=["fitness", "wellness"]
    )
    angles = strategist.generate_angles("SuperFit Tracker", demo)
    for a in angles:
        print(a)
