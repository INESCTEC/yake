#!/usr/bin/env python
"""
Quick test to verify lemmatization warning appears only once.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import yake

print("Creating KeywordExtractor with lemmatize=True...")
kw = yake.KeywordExtractor(lan="en", n=1, top=5, lemmatize=True)

text = "Trees are important. Many trees provide shade. Tree conservation matters."

print("\nExtracting keywords 5 times from same extractor instance...")
for i in range(1, 6):
    result = kw.extract_keywords(text)
    print(f"  Extraction {i}: {len(result)} keywords extracted")

print("\n✅ Notice: Warning should appear only ONCE (on first extraction)")
print("   Subsequent extractions should not show the warning again.\n")
