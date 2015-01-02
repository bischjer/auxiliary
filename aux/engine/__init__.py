from aux.engine.actor import (Reactor, Proactor, Coactor, NoActorFoundError)
import sys
import traceback


class Engine(object):

    def __init__(self, Actor=Reactor):
        self.log_directory = "."
        self.actor = Actor("Engine")
        
    def setup(self, kwargs):
        self.actor.setup()

    def add_callback(self, callback):
        self.actor.add_callback(callback)

    def remove_callback(self, callback):
        self.actor.remove_callback(callback)
        
    def is_running(self):
        return self.actor.is_running()
        
    def start(self):
        try:
            self.actor.start()
        except:
            print traceback.print_exc(file=sys.stdout)

    def stop(self):
        try:
            self.actor.stop()
        except Exception:
            print traceback.print_exc(file=sys.stdout)
        finally:
            if self.is_running():
                pass

def engine_factory(engine_type):
    if engine_type.upper()=='REACTOR':
        return Engine(Reactor)
    elif engine_type.upper()=='PROCATOR':
        return Engine(Proactor)
    elif engine_type.upper()=='COACTOR':
        return Engine(Coactor)
    else:
        raise NoActorFoundError(engine_type)
