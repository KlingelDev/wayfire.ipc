#!/usr/bin/env python3

import sys
import os
import argparse

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Ensure we can find the wayfire package
wayfire_path = '/home/karl/opt/wayfire/lib/python3.13/site-packages'
if wayfire_path not in sys.path:
    sys.path.append(wayfire_path)

from applicator import ConfigApplicator

def main():
    parser = argparse.ArgumentParser(description='Wayfire Desktop Configuration Manager')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to config file')
    parser.add_argument('--apply', action='store_true', help='Apply the configuration once')
    parser.add_argument('--daemon', action='store_true', help='Apply configuration and watch for new windows')
    
    args = parser.parse_args()

    if not os.path.exists(args.config):
        print(f"Error: Config file {args.config} not found.")
        sys.exit(1)

    try:
        applicator = ConfigApplicator(args.config)
    except Exception as e:
        print(f"Error initializing: {e}")
        print("Ensure Wayfire is running and the socket is accessible.")
        sys.exit(1)
    
    if args.apply or args.daemon:
        applicator.apply()
        
    if args.daemon:
        try:
            applicator.watch_events()
        except KeyboardInterrupt:
            print("\nExiting...")
    elif not args.apply:
        print(f"Config {args.config} loaded successfully. Use --apply or --daemon to apply it.")

if __name__ == '__main__':
    main()
