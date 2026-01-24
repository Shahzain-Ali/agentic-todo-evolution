"""
Todo Console Application - Main entry point
"""
import sys
from todo.rich_cli import main as rich_main
from todo.cli import main as classic_main

def main():
    # Check if command line arguments are provided
    # If arguments are provided, use classic CLI
    # If no arguments, use rich interactive CLI
    if len(sys.argv) > 1:
        # Use classic CLI for command-line operations
        from todo.cli import main as classic_main
        classic_main()
    else:
        # Use rich interactive CLI when no arguments provided
        rich_main()

if __name__ == "__main__":
    main()