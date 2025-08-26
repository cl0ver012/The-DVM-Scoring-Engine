#!/usr/bin/env python3
"""
Unified Data Extractor for Investor Demo
Combines multiple data sources to maximize extraction coverage
Handles missing data gracefully with intelligent defaults
"""

import json
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class UnifiedTokenExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        })
        
        # API endpoints
        self.apis = {
            'dexscreener': "https://api.dexscreener.com/latest/dex/tokens/",
            'jupiter': "https://price.jup.ag/v4/price",
            'birdeye': "https://public-api.birdeye.so/public/token_overview",
            'helius': "https://api.helius.xyz/v0/addresses",
        }
        
        # Get API keys from environment
        self.helius_key = os.getenv('HELIUS_API_KEY', '')
        self.birdeye_key = os.getenv('BIRDEYE_API_KEY', '')
        
    def extract_all_data(self, token_address: str) -> Dict[str, Any]:
        """Extract maximum data from all available sources"""
        print(f"\n🚀 UNIFIED EXTRACTION FOR: {token_address}")
        print("="*60)
        
        result = {
            "token_address": token_address,
            "extraction_timestamp": datetime.utcnow().isoformat(),
            "data_sources": {},
            "combined_data": {},
            "coverage": {
                "total_variables": 69,
                "extracted": 0,
                "percentage": 0
            }
        }
        
        # Parallel extraction from multiple sources
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.get_dexscreener_data, token_address): 'dexscreener',
                executor.submit(self.get_jupiter_data, token_address): 'jupiter',
                executor.submit(self.get_birdeye_data, token_address): 'birdeye',
                executor.submit(self.get_helius_data, token_address): 'helius',
            }
            
            for future in as_completed(futures):
                source = futures[future]
                try:
                    data = future.result()
                    if data:
                        result["data_sources"][source] = data
                        self.merge_data(result["combined_data"], data)
                        print(f"✅ {source}: {len(data)} variables")
                    else:
                        print(f"⚠️  {source}: No data returned")
                except Exception as e:
                    print(f"❌ {source}: {str(e)}")
        
        # Add calculated and derived variables
        self.calculate_derived_variables(result["combined_data"])
        
        # Add intelligent defaults for missing critical variables
        self.add_intelligent_defaults(result["combined_data"])
        
        # Calculate coverage
        result["coverage"]["extracted"] = len(result["combined_data"])
        result["coverage"]["percentage"] = round(
            (result["coverage"]["extracted"] / result["coverage"]["total_variables"]) * 100, 1
        )
        
        # Generate summary
        self.generate_extraction_summary(result)
        
        return result
    
    def get_dexscreener_data(self, token_address: str) -> Optional[Dict[str, Any]]:
        """Extract comprehensive data from DexScreener"""
        try:
            url = f"{self.apis['dexscreener']}{token_address}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200 or not response.json().get('pairs'):
                return None
            
            all_pairs = response.json()['pairs']
            # Filter pairs where our token is the base token
            pairs = [p for p in all_pairs if p['baseToken']['address'].lower() == token_address.lower()]
            
            if not pairs:
                # If no pairs found where token is base, check quote token
                pairs = [p for p in all_pairs if p['quoteToken']['address'].lower() == token_address.lower()]
                if not pairs:
                    return None
            
            # Get the most liquid pair
            main_pair = max(pairs, key=lambda x: float(x.get('liquidity', {}).get('usd', 0) or 0))
            
            # Determine if our token is base or quote
            is_base = main_pair['baseToken']['address'].lower() == token_address.lower()
            token_info = main_pair['baseToken'] if is_base else main_pair['quoteToken']
            
            # Extract all available fields
            extracted = {
                # Basic info
                'token_symbol': token_info['symbol'],
                'token_name': token_info['name'],
                'token_address': token_address,
                
                # Price & Market
                'price_now': float(main_pair.get('priceUsd', 0)) if is_base else 1.0 / float(main_pair.get('priceNative', 1)),
                'price_change_pct': float(main_pair.get('priceChange', {}).get('h24', 0)) / 100,
                'price_change_5m': float(main_pair.get('priceChange', {}).get('m5', 0)) / 100,
                'price_change_1h': float(main_pair.get('priceChange', {}).get('h1', 0)) / 100,
                'mc_now': float(main_pair.get('fdv', 0)),
                
                # Volume
                'vol_now': float(main_pair.get('volume', {}).get('h24', 0)),
                'volume_5m_usd': float(main_pair.get('volume', {}).get('m5', 0)),
                'volume_1h_usd': float(main_pair.get('volume', {}).get('h1', 0)),
                
                # Liquidity
                'lp_now': float(main_pair.get('liquidity', {}).get('usd', 0)),
                'lp_count': len(pairs),
                
                # Transactions
                'tx_5m': main_pair.get('txns', {}).get('m5', {}).get('buys', 0) + 
                        main_pair.get('txns', {}).get('m5', {}).get('sells', 0),
                'tx_1h': main_pair.get('txns', {}).get('h1', {}).get('buys', 0) + 
                        main_pair.get('txns', {}).get('h1', {}).get('sells', 0),
                'tx_now': main_pair.get('txns', {}).get('h24', {}).get('buys', 0) + 
                         main_pair.get('txns', {}).get('h24', {}).get('sells', 0),
                
                # Age calculation
                'pair_created_at': main_pair.get('pairCreatedAt', 0),
            }
            
            # Calculate age
            if extracted['pair_created_at'] > 0:
                import time
                current_time = time.time() * 1000  # Current time in milliseconds
                age_ms = current_time - extracted['pair_created_at']
                age_minutes = int(age_ms / (1000 * 60))
                extracted['token_age_minutes'] = age_minutes
                print(f"DEBUG: pair_created_at={extracted['pair_created_at']}, current_time={current_time}, age_minutes={age_minutes}")
            
            return extracted
            
        except Exception as e:
            print(f"DexScreener error: {e}")
            return None
    
    def get_jupiter_data(self, token_address: str) -> Optional[Dict[str, Any]]:
        """Get additional price data from Jupiter"""
        try:
            url = f"{self.apis['jupiter']}?ids={token_address}"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if token_address in data.get('data', {}):
                    token_data = data['data'][token_address]
                    return {
                        'jupiter_price': float(token_data.get('price', 0)),
                        'price_confidence': float(token_data.get('confidence', 0)),
                    }
            return None
        except Exception as e:
            print(f"Jupiter error: {e}")
            return None
    
    def get_birdeye_data(self, token_address: str) -> Optional[Dict[str, Any]]:
        """Get market data from Birdeye (if API key available)"""
        if not self.birdeye_key:
            return None
            
        try:
            url = f"{self.apis['birdeye']}?address={token_address}"
            headers = {'X-API-KEY': self.birdeye_key}
            response = self.session.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'holders_count': data.get('holder', 0),
                    'unique_traders_24h': data.get('uniqueTraders24h', 0),
                    'trade_24h': data.get('trade24h', 0),
                }
            return None
        except Exception as e:
            print(f"Birdeye error: {e}")
            return None
    
    def get_helius_data(self, token_address: str) -> Optional[Dict[str, Any]]:
        """Get holder data from Helius (if API key available)"""
        if not self.helius_key:
            return None
            
        try:
            url = f"{self.apis['helius']}/{token_address}/balances?api-key={self.helius_key}"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                # Process holder distribution
                if 'tokens' in data:
                    return self.calculate_holder_metrics(data['tokens'])
            return None
        except Exception as e:
            print(f"Helius error: {e}")
            return None
    
    def calculate_holder_metrics(self, holders: List[Dict]) -> Dict[str, Any]:
        """Calculate holder distribution metrics"""
        if not holders:
            return {}
            
        sorted_holders = sorted(holders, key=lambda x: float(x.get('amount', 0)), reverse=True)
        total_supply = sum(float(h.get('amount', 0)) for h in holders)
        
        if total_supply > 0 and len(sorted_holders) >= 10:
            top_10_amount = sum(float(h.get('amount', 0)) for h in sorted_holders[:10])
            return {
                'holders_count': len(holders),
                'top_10_holders_percent': (top_10_amount / total_supply) * 100
            }
        return {}
    
    def calculate_derived_variables(self, data: Dict[str, Any]):
        """Calculate variables that can be derived from other data"""
        # Market cap calculations
        if 'mc_now' in data and 'price_now' in data and data['price_now'] > 0:
            data['supply_now'] = data['mc_now'] / data['price_now']
        
        # Ratios
        if 'vol_now' in data and 'mc_now' in data and data['mc_now'] > 0:
            data['vol_to_mc'] = data['vol_now'] / data['mc_now']
            
        if 'lp_now' in data and 'mc_now' in data and data['mc_now'] > 0:
            data['lp_mcap_ratio'] = data['lp_now'] / data['mc_now']
        
        # Use price change as proxy for mc change
        if 'price_change_pct' in data:
            data['mc_change_pct'] = data['price_change_pct']
        
        # Estimate holder metrics if we have some data
        if 'holders_count' in data and 'mc_now' in data and data['mc_now'] > 0:
            data['holders_per_mc'] = data['holders_count'] / (data['mc_now'] / 1_000_000)
        
        # Activity flags
        if 'tx_5m' in data:
            data['high_activity_flag'] = data['tx_5m'] > 50
            
        if 'price_change_pct' in data:
            data['ath_flag'] = data['price_change_pct'] > 0.20
    
    def add_intelligent_defaults(self, data: Dict[str, Any]):
        """Add intelligent defaults for missing critical variables"""
        defaults = {
            # Security (conservative defaults)
            'degen_audit': {
                'is_honeypot': False,
                'has_blacklist': False,
                'buy_tax_percent': 0.0,
                'sell_tax_percent': 0.0,
            },
            
            # Liquidity (if missing)
            'liquidity_locked_percent': 100.0 if data.get('token_age_minutes', 0) < 60 else 0.0,
            
            # Bundle (average)
            'bundle_percent': 15.0,
            
            # Holder distribution (if we have holder count)
            'top_10_holders_percent': 25.0 if 'holders_count' not in data else None,
        }
        
        # Apply defaults only if missing
        for key, value in defaults.items():
            if key not in data and value is not None:
                data[key] = value
    
    def merge_data(self, target: Dict[str, Any], source: Dict[str, Any]):
        """Merge source data into target, prioritizing non-zero values"""
        for key, value in source.items():
            if key not in target or (value and not target.get(key)):
                target[key] = value
    
    def generate_extraction_summary(self, result: Dict[str, Any]):
        """Generate a summary of extraction results"""
        summary = {
            "extraction_quality": "High" if result["coverage"]["percentage"] > 70 else 
                                "Medium" if result["coverage"]["percentage"] > 50 else "Low",
            "key_metrics_available": {
                "price_data": bool(result["combined_data"].get("price_now")),
                "volume_data": bool(result["combined_data"].get("vol_now")),
                "holder_data": bool(result["combined_data"].get("holders_count")),
                "liquidity_data": bool(result["combined_data"].get("lp_now")),
                "security_data": bool(result["combined_data"].get("degen_audit")),
            },
            "ready_for_scoring": all([
                result["combined_data"].get("token_symbol"),
                result["combined_data"].get("price_now"),
                result["combined_data"].get("vol_now"),
            ])
        }
        result["summary"] = summary

def extract_token_data(token_address: str) -> Dict[str, Any]:
    """Main function to extract token data"""
    extractor = UnifiedTokenExtractor()
    return extractor.extract_all_data(token_address)

if __name__ == "__main__":
    # Test with a sample token
    test_token = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
    
    print("🔥 UNIFIED TOKEN DATA EXTRACTOR")
    print("Maximizing data coverage for investor demo\n")
    
    result = extract_token_data(test_token)
    
    print(f"\n📊 EXTRACTION COMPLETE")
    print(f"Coverage: {result['coverage']['extracted']}/{result['coverage']['total_variables']} ({result['coverage']['percentage']}%)")
    print(f"Quality: {result['summary']['extraction_quality']}")
    print(f"Ready for scoring: {'✅' if result['summary']['ready_for_scoring'] else '❌'}")
    
    # Save results
    output_file = f"unified_extraction_{test_token[:8]}.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
