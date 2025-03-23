from abc import ABC, abstractmethod

class FilePublication(ABC):
    def __init__(self, num_of_publ, direction, path):
        self.path = path
        self.num_of_publ = num_of_publ
        self.direction = direction

    @abstractmethod
    def add_post_to_feed(self):
        pass

    @abstractmethod
    def remove_empty_file(self):
        pass

    @abstractmethod
    def initialize_from_user_input(self):
        pass

    @abstractmethod
    def input_num_of_publ_with_validation(self):
        pass
    