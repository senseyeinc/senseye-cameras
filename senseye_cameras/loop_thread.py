import threading
import time
from logging import getLogger

log = getLogger(__name__)


class LoopThread(threading.Thread):
    '''
    Class to follow common pattern of looping thread
    '''
    def __init__(self, frequency=1000, stop_on_error=False):
        super().__init__(daemon=True)

        # Flag to inidicate that the thread should stop
        self._should_finish = False
        self._did_finish = False

        # Flag wether it will exit on error
        self.stop_on_error = stop_on_error

        # delay between Loops
        self._frequency = frequency
        self._delay = 1 / frequency if frequency > 0 else 0

    #######################
    ## Optional Methods
    #######################
    # Called when the thread is started, before the loop
    # Main looped function to be overwritten
    def loop(self):
        pass

    def on_start(self):
        pass

    # Called when the thread is stopped, after the loop
    def on_stop(self):
        pass

    # Called when a uncaught error is passed in the loop
    def on_error(self, e):
        pass

    #######################
    ## Defined Methods
    #######################

    # Thread main run method
    def run(self):
        self.on_start()

        self._should_finish = False
        self._did_finish = False

        start_time = time.time()
        count = 0

        while not self._should_finish:
            try:
                # calculate sleep time
                count += 1
                sleep_time = start_time + count * self._delay - time.time()
                if sleep_time > 0:
                    time.sleep(sleep_time)

                # call loop function
                self.loop()

            except Exception as e:
                log.exception(f'Uncaught Error in Looping Thread: {e}')
                self.on_error(e)

                if self.stop_on_error:
                    break

        self.on_stop()

        self._did_finish = True

    # called to Stop the thread
    def stop(self, join=True):
        self._should_finish = True

        if join:
            # Catch self.join errors so this function can be called from within itself
            try:
                self.join()
            except RuntimeError:
                pass

    def restart(self):
        '''
        Restart at thread
        Seperated from start / stop because thread functions like join  / is alive
        May return unexpected results from this
        '''
        # Re-initialize the thread parent
        threading.Thread.__init__(self, daemon=True)

        # Start the thread
        return self.start()
