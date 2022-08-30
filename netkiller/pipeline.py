import os
class Pipeline:
    def __init__(self, workspace):
        self.workspace = workspace
        self.pipelines = {}
        pass
    def start(self):
        os.chdir(self.workspace)
        self.pipelines['start'] = []
        return self
    def init(self):
        self.pipelines['init'] = []
        return self
    def checkout(self):
        self.pipelines['checkout'] = []
        return self
    def build(self):
        self.pipelines['build'] = []
        return self
    def package(self):
        self.pipelines['package'] = []
        return self
    def test(self):
        self.pipelines['test'] = []
        return self
    def deploy(self):
        self.pipelines['deploy'] = []
        return self
    def startup(self):
        self.pipelines['startup'] = []
        return self
    def end(self):
        self.pipelines['end'] = []