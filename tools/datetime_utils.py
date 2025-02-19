#!/usr/bin/env python3
"""
Datetime utility functions for getting current time and date in various formats.
Supports different timezones and formatting options.
"""

import datetime
import pytz
from typing import Optional, Dict, Any
import json
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_current_datetime(timezone: Optional[str] = None) -> Dict[str, Any]:
    """
    Get current date and time information in various formats.
    
    Args:
        timezone: Optional timezone name (e.g., 'America/New_York', 'UTC')
                 If None, uses local system timezone
    
    Returns:
        Dictionary containing various datetime representations
    """
    try:
        if timezone:
            tz = pytz.timezone(timezone)
            current = datetime.datetime.now(tz)
        else:
            current = datetime.datetime.now()
        
        return {
            "iso": current.isoformat(),
            "timestamp": int(current.timestamp()),
            "readable": {
                "date": current.strftime("%B %d, %Y"),
                "time": current.strftime("%I:%M:%S %p"),
                "day": current.strftime("%A"),
            },
            "components": {
                "year": current.year,
                "month": current.month,
                "day": current.day,
                "hour": current.hour,
                "minute": current.minute,
                "second": current.second,
                "microsecond": current.microsecond,
            },
            "timezone": str(current.tzinfo or "local"),
        }
    except Exception as e:
        logger.error(f"Error getting datetime: {str(e)}")
        return {
            "error": str(e),
            "timestamp": int(datetime.datetime.now().timestamp())
        }

def list_available_timezones() -> Dict[str, list]:
    """List all available timezone names grouped by region."""
    try:
        zones = {}
        for tz in pytz.all_timezones:
            region = tz.split('/')[0]
            if region not in zones:
                zones[region] = []
            zones[region].append(tz)
        return {"timezones": zones}
    except Exception as e:
        logger.error(f"Error listing timezones: {str(e)}")
        return {"error": str(e)}

def main():
    """Main function to run the datetime utility."""
    parser = argparse.ArgumentParser(description='Get current date and time information')
    parser.add_argument('--timezone', '-tz', help='Timezone (e.g., America/New_York)')
    parser.add_argument('--list-zones', '-l', action='store_true', help='List available timezones')
    parser.add_argument('--format', '-f', choices=['json', 'readable'], default='json',
                       help='Output format (default: json)')
    
    args = parser.parse_args()
    
    try:
        if args.list_zones:
            result = list_available_timezones()
        else:
            result = get_current_datetime(args.timezone)
        
        if args.format == 'json':
            print(json.dumps(result, indent=2))
        else:
            if 'readable' in result:
                print(f"Date: {result['readable']['date']}")
                print(f"Time: {result['readable']['time']}")
                print(f"Day: {result['readable']['day']}")
                print(f"Timezone: {result['timezone']}")
            else:
                print(json.dumps(result, indent=2))
    
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        print(json.dumps({"error": str(e)}, indent=2))

if __name__ == "__main__":
    main() 