import random

class Person:
    def __init__(self, _id, is_vaccinated, infection=None):
        self._id = _id
        self.is_vaccinated = is_vaccinated
        self.infection = infection
        self.is_alive = True

    def did_survive_infection(self):
        if self.infection:
            if random.random() < self.infection.mortality_rate:
                self.is_alive = False
                return False
        self.is_vaccinated = True
        self.infection = None
        return True
