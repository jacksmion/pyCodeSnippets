import sys
import time

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix))
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()

for i in range(100):
    time.sleep(0.1)
    printProgress(i, 100)