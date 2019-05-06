#!/usr/bin/python3
""" 
    The initial part of this project is to track habits.

    Expansion to include vices, goals and time tracking.
"""

import logging
import argparse
from personaltracker.personaltracker import PersonalTracker

logging.basicConfig(filename=('logs/personaltracker.log'), level=logging.DEBUG)

##### Main
#####
if __name__ == '__main__':
    personal_tracker = PersonalTracker()
    personal_tracker.run()
    print('Completed')

