import time
import random
import json
import os
from datetime import datetime
import config
from modules.analyzer import ProductAnalyzer
from modules.scorer import ProductScorer
from modules.strategist import SalesStrategist
from modules.content_generator import ContentGenerator
from modules.campaign_manager import CampaignManager
from modules.publisher import Publisher

# Ensure output directory exists
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

LOG_FILE = os.path.join(OUTPUT_DIR, 'activity.log')
CAMPAIGNS_FILE = os.path.join(OUTPUT_DIR, 'campaigns.json')

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def load_campaigns():
    if os.path.exists(CAMPAIGNS_FILE):
        with open(CAMPAIGNS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_campaigns(campaigns):
    with open(CAMPAIGNS_FILE, 'w') as f:
        json.dump(campaigns, f, indent=2)

def run_autonomous_cycle():
    log("Starting autonomous cycle...")
    
    # 1. Pick a random niche and region
    niche = random.choice(config.TARGET_NICHES)
    region_name = config.DEFAULT_REGION
    region_code = config.REGIONS.get(region_name, "wt-wt")
    
    log(f"Targeting Niche: {niche} | Region: {region_name}")
    
    # 2. Analyze Market
    analyzer = ProductAnalyzer()
    products = analyzer.find_trending_products(niche, limit=3, region=region_code)
    
    if not products:
        log("No products found. Skipping cycle.")
        return

    # 3. Score Products
    import pandas as pd
    scorer = ProductScorer()
    df = pd.DataFrame(products)
    # Add mock metrics for scoring
    df['demand_score'] = [random.uniform(0.6, 1.0) for _ in range(len(df))]
    df['commission_rate'] = [random.uniform(0.05, 0.25) for _ in range(len(df))]
    df['competition_score'] = [random.uniform(0.3, 0.7) for _ in range(len(df))]
    
    scored_df = scorer.score_dataframe(df)
    top_product = scored_df.iloc[0].to_dict()
    
    log(f"Top Product Found: {top_product['title']} (Score: {top_product['score']})")
    
    # 4. Generate Strategy & Content
    manager = CampaignManager()
    strategist = SalesStrategist()
    content_gen = ContentGenerator()
    
    # Mock demographics
    top_product['demographics'] = {"age_range": "25-45", "location": region_name, "gender": "All"}
    top_product['interests'] = [niche, "deals", "online shopping"]
    
    campaign = manager.add_product(top_product, top_product['score'], strategist, content_gen)
    
    # 5. Publish/Save
    existing_campaigns = load_campaigns()
    # Check for duplicates based on title
    if not any(c['product']['title'] == campaign['product']['title'] for c in existing_campaigns):
        existing_campaigns.append(campaign)
        save_campaigns(existing_campaigns)
        log("Campaign generated and saved successfully.")
        
        # Generate HTML file
        publisher = Publisher()
        html = publisher.generate_landing_page(campaign['product']['title'], campaign['copy'])
        filename = f"campaign_{int(time.time())}.html"
        with open(os.path.join(OUTPUT_DIR, filename), 'w') as f:
            f.write(html)
        log(f"Landing page created: {filename}")
    else:
        log("Campaign for this product already exists. Skipping.")

    log("Cycle complete.")

if __name__ == "__main__":
    log("Autonomous Agent Started. Press Ctrl+C to stop.")
    try:
        while True:
            run_autonomous_cycle()
            # Wait for the configured interval (converted to seconds)
            # For demo purposes, we'll wait 60 seconds instead of hours
            wait_time = 60 # config.RUN_INTERVAL_HOURS * 3600
            log(f"Sleeping for {wait_time} seconds...")
            time.sleep(wait_time)
    except KeyboardInterrupt:
        log("Agent stopped by user.")
