import time
import logging


class Speedometer(object):
    def __init__(self, batch_size, frequent=50):
        self.batch_size = batch_size
        self.frequent = frequent
        self.init = False
        self.tic = 0
        self.last_count = 0

    def __call__(self, param):
        """Callback to Show speed."""
        count = param.nbatch
        if self.last_count > count:
            self.init = False
        self.last_count = count

        if self.init:
            if count % self.frequent == 0:
                speed = self.frequent * self.batch_size / (time.time() - self.tic)
                if param.eval_metric is not None:
                    name, value = param.eval_metric.get()
                    s = ''
                    for n, v in zip(name, value):
                        s += '{}={:.6f},\t'.format(n, v)
                    logging.info("Epoch[%d] Batch [%d]\tSpeed: %.2f samples/sec\tTrain-%s",
                                 param.epoch, count, speed, s)
                else:
                    logging.info("Iter[%d] Batch [%d]\tSpeed: %.2f samples/sec",
                                 param.epoch, count, speed)
                self.tic = time.time()
        else:
            self.init = True
            self.tic = time.time()
