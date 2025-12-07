"""
Mini Torrent Tracker Package

This package contains the tracker server implementation:
- server.py: Core tracker functionality
- tracker_gui.py: Optional tracker GUI
"""

from .server import app, peers, run_tracker

__all__ = ['app', 'peers', 'run_tracker']
__version__ = '0.1.0'