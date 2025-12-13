# Config for Autonomous Sales Agent

# Region Settings
REGIONS = {
    "Global": "wt-wt",
    "India": "in-en"
}
DEFAULT_REGION = "India"

# User Affiliate IDs (Replace with your actual IDs)
AFFILIATE_IDS = {
    "amazon": "my-amazon-tag-20",
    "clickbank": "myclickbankid",
    "shareasale": "123456",
    "flipkart": "my-flipkart-id",
    "hostinger": "my-hostinger-id"
}

# Target Niches for Autonomous Loop
TARGET_NICHES = [
    "SaaS Tools",
    "Web Hosting",
    "Ecommerce",
    "Digital Courses",
    "Email Marketing Software",
    "Payment Solutions"
]

# Pre-populated Affiliate Programs (for Dashboard)
AFFILIATE_PROGRAMS = [
    {
        "name": "Zoho Affiliate Program",
        "commission": "15%",
        "category": "SaaS",
        "region": "Global + India",
        "earning_potential": "₹50,000 - ₹3,00,000/month",
        "url": "zoho.com/affiliate"
    },
    {
        "name": "Flipkart Affiliate Program",
        "commission": "Up to 12%",
        "category": "Ecommerce",
        "region": "India",
        "earning_potential": "₹30,000 - ₹2,00,000/month",
        "url": "flipkart.com/affiliate"
    },
    {
        "name": "Amazon Affiliate",
        "commission": "3-10%",
        "category": "Ecommerce",
        "region": "Global + India",
        "earning_potential": "₹20,000 - ₹1,50,000/month",
        "url": "amazon.in/affiliate"
    },
    {
        "name": "Hostinger Affiliate",
        "commission": "Up to 60%",
        "category": "Hosting",
        "region": "Global",
        "earning_potential": "₹40,000 - ₹5,00,000/month",
        "url": "hostinger.com/affiliate"
    },
    {
        "name": "GetResponse Affiliate",
        "commission": "40-60% recurring",
        "category": "SaaS - Email Marketing",
        "region": "Global",
        "earning_potential": "₹60,000 - ₹4,00,000/month",
        "url": "getresponse.com/affiliate"
    },
    {
        "name": "Cuelinks",
        "commission": "4% - 50%",
        "category": "Affiliate Network",
        "region": "India",
        "earning_potential": "₹30,000 - ₹2,00,000/month",
        "url": "cuelinks.com"
    }
]

# General Settings
MAX_PRODUCTS_TO_ANALYZE = 5
RUN_INTERVAL_HOURS = 24

# Content Generation Settings
TONE = "persuasive"  # persuasive, informative, casual
GENERATE_IMAGES = False
