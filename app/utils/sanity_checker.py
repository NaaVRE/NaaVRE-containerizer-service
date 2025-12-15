import inspect


class SanityChecker:

    def run_all(self):
        """
        Call all instance methods named `check_<something>.
        Methods are run in deterministic order (sorted by name).
        """
        for name, method in sorted(
                inspect.getmembers(self, predicate=inspect.ismethod)):
            if name.startswith('check_'):
                method()
