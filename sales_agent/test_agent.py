import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.analyzer import ProductAnalyzer
from modules.scorer import ProductScorer
from modules.strategist import SalesStrategist
from modules.content_generator import ContentGenerator
from modules.campaign_manager import CampaignManager
from modules.publisher import Publisher
import pandas as pd

def test_end_to_end():
    print("Starting End-to-End Test...")

    # 1. Market Analysis
    print("[1] Testing Market Analysis...")
    analyzer = ProductAnalyzer()
    # Mocking the search to avoid network calls during quick test, 
    # or we can actually run it. Let's try a real run but catch errors.
    try:
        products = analyzer.find_trending_products("eco friendly water bottle", limit=2)
        if not products:
            print("   Warning: No products found (network issue?), using mock data.")
            products = [{"title": "Mock Eco Bottle", "link": "http://example.com", "snippet": "Best eco bottle review"}]
    except Exception as e:
        print(f"   Error in analysis: {e}")
        products = [{"title": "Mock Eco Bottle", "link": "http://example.com", "snippet": "Best eco bottle review"}]
    
    print(f"   Found {len(products)} products.")

    # 2. Scoring
    print("[2] Testing Scoring...")
    scorer = ProductScorer()
    df = pd.DataFrame(products)
    # Add mock metrics
    df['demand_score'] = 0.8
    df['commission_rate'] = 0.1
    df['competition_score'] = 0.5
    
    scored_df = scorer.score_dataframe(df)
    print("   Scoring successful.")
    
    # 3. Strategy & Content
    print("[3] Testing Strategy & Content...")
    manager = CampaignManager()
    strategist = SalesStrategist()
    content_gen = ContentGenerator()
    
    top_product = scored_df.iloc[0].to_dict()
    # Add mock demographics
    top_product['demographics'] = {"age_range": "20-30", "location": "UK", "gender": "Any"}
    top_product['interests'] = ["sustainability"]
    
    campaign = manager.add_product(top_product, top_product['score'], strategist, content_gen)
    print("   Campaign created.")
    print(f"   Copy snippet: {campaign['copy'][:50]}...")

    # 4. Publisher
    print("[4] Testing Publisher...")
    pub = Publisher()
    html = pub.generate_landing_page(campaign['product']['title'], campaign['copy'])
    print(f"DEBUG HTML: {html[:100]}...")
    assert "<html>" in html.lower() or "<!doctype html>" in html.lower()
    print("   HTML generated.")

    print("End-to-End Test Passed!")

if __name__ == "__main__":
    test_end_to_end()
