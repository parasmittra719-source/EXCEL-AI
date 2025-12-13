class Publisher:
    """Generate simple HTML landing pages for affiliate products.

    The generated page includes the product name, a short description (copy),
    and optionally an image. This is a minimal implementation that can be
    extended to include CSS styling, analytics, or affiliate tracking links.
    """

    def __init__(self, stylesheet: str = None):
        # Optional custom CSS stylesheet URL or inline CSS.
        self.stylesheet = stylesheet

    def generate_landing_page(self, product_name: str, copy: str, image_url: str = None) -> str:
        """Return an HTML string for a landing page.

        Parameters
        ----------
        product_name: str
            Name of the product.
        copy: str
            Marketing copy (HTML safe).
        image_url: str, optional
            URL to a product image.
        """
        import textwrap
        style_tag = f"<link rel='stylesheet' href='{self.stylesheet}'>" if self.stylesheet else ""
        img_tag = f"<img src='{image_url}' alt='{product_name}' style='max-width:100%;'/>" if image_url else ""
        html = f"""
        <!DOCTYPE html>
        <html lang='en'>
        <head>
            <meta charset='UTF-8'>
            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
            <title>{product_name} - Affiliate Offer</title>
            {style_tag}
        </head>
        <body style='font-family:Arial,Helvetica,sans-serif; margin:2rem;'>
            <h1>{product_name}</h1>
            {img_tag}
            <div>{copy}</div>
        </body>
        </html>
        """
        return textwrap.dedent(html).strip()

# Example usage (remove in production)
if __name__ == "__main__":
    pub = Publisher()
    html = pub.generate_landing_page("SuperFit Tracker", "<p>Track your workouts effortlessly.</p>")
    print(html)
