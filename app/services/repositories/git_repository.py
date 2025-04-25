from abc import abstractmethod


class GitRepository:

    @abstractmethod
    def commit(self, commit_list: list[{}]):
        pass

    @abstractmethod
    def dispatch_containerization_workflow(self):
        pass
