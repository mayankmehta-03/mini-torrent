"""
Mini Torrent Client Package

This package contains all the modules for the torrent client functionality including:
- peer.py: Core peer functionality
- gui.py: Graphical user interface
- widgets.py: Custom GUI widgets
- dialogs.py: Dialog windows
"""

from .peer import Peer
from .gui import TorrentGUI, run_gui

__all__ = ['Peer', 'TorrentGUI', 'run_gui']
__version__ = '0.1.0'