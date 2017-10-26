from datetime import datetime as dt
from time import time
import json, logging

class log(object):

    def __init__(self, base, folder='logs'):
        self.base = base
        self.folder = folder
        return

    def __call__(self, f):

        # Function to return
        def wrappedF(*args, **kwargs):
            logger = logging.getLogger(self.base)
            logger.info('Starting the function [{}] ...'.format(f.__name__))
            t0     = time()
            result = f(logger, *args, **kwargs)
            logger.info('Finished the function [{}] in {:.2e} seconds'.format(
                f.__name__, time() - t0 ))

            wrappedF.__name__ = f.__name__
            wrappedF.__doc__  = f.__doc__

            return result

        return wrappedF

class logInit(object):

    def __init__(self, base, folder='logs'):
        self.base   = base
        self.folder = folder
        return

    def __call__(self, f):


        # Function to return
        def wrappedF(*args, **kwargs):
            logger    = logging.getLogger(self.base)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fH        = logging.FileHandler(               \
                self.folder  +  '/'                      + \
                dt.now().strftime('%Y-%m-%d_%H-%M-%S')   + \
                '.log')
            fH.setFormatter(formatter)
            logger.addHandler(fH)
            logger.setLevel(logging.INFO)

            logger.info('Starting the main program ...')
            t0     = time()
            result = f(logger, *args, **kwargs)
            logger.info('Finished the main program in {:.2e} seconds'.format( time() - t0 ))

            return result

        return wrappedF