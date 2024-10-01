from abc import abstractmethod


class GitRepository:

    @abstractmethod
    def commit(self, content):
        pass

    @abstractmethod
    def dispatch_containerization_workflow(self):
        pass
