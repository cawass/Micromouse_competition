import uio

class DataLogger:
    def __init__(self):
        self.buffer = uio.StringIO()
        self.headers_written = False
        
    def log(self, **kwargs):
        if not self.headers_written:
            self.buffer.write(','.join(kwargs.keys()) + '\n')
            self.headers_written = True
            
        self.buffer.write(','.join(map(str, kwargs.values())) + '\n')
        
    def save(self, filename='log.csv'):
        with open(filename, 'w') as f:
            f.write(self.buffer.getvalue())
        self.buffer.close()