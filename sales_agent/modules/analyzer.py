from duckduckgo_search import DDGS
import time

class ProductAnalyzer:
    def __init__(self):
        self.ddgs = DDGS()

    def find_trending_products(self, niche, limit=5, region="wt-wt"):
        """
        Searches for trending products in the specified niche.
        Returns a list of dictionaries containing product info.
        """
        print(f"[*] Searching for trending '{niche}' products in region '{region}'...")
        query = f"best selling {niche} products 2025 reviews"
        results = []
        
        try:
            # simple text search with region
            search_results = self.ddgs.text(query, region=region, max_results=limit*2)
            
            for r in search_results:
                title = r.get('title', '')
                link = r.get('href', '')
                body = r.get('body', '')
                
                # Basic filtering: Try to extract a product-like name or just use the title
                # For now, we'll treat the search result itself as a "lead"
                results.append({
                    "title": title,
                    "link": link,
                    "snippet": body,
                    "score": 0 # Placeholder for scoring logic
                })
                
                if len(results) >= limit:
                    break
                    
        except Exception as e:
            print(f"[!] Error searching for products: {e}")
            
        return results

    def analyze_opportunity(self, product_lead):
        """
        Analyzes a specific product lead to determine affiliate potential.
        (Placeholder logic for now)
        """
        # Simple heuristic: longer snippets with keywords like "review", "price", "buy" might be better
        score = 0
        text = (product_lead['title'] + " " + product_lead['snippet']).lower()
        
        keywords = ["review", "best", "top", "guide", "price", "buy"]
        for kw in keywords:
            if kw in text:
                score += 10
                
        product_lead['score'] = score
        return product_lead
