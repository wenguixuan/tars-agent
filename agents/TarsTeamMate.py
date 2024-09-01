class TarsTeamMate(object):
    def __init__(self, planner, executors=[], reviewers=[]) -> None:
        self.planner = planner
        self.executors = executors
        self.reviewers = reviewers
        self.feedbbacks = []
        self.graph = None

    def work(self):
        pass


