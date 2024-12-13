import random
from person import Person
from virus import Virus
from logger import Logger

class Simulation:
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected):
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.virus = virus
        self.initial_infected = initial_infected
        self.population = []
        self.logger = Logger("simulation_log.txt")
        self.total_dead = 0
        self.total_vaccinated = 0
        self.new_infections = []
        self._create_population()

    def _create_population(self):
        num_vaccinated = int(self.pop_size * self.vacc_percentage)
        num_infected = self.initial_infected

        for i in range(self.pop_size):
            if i < num_vaccinated:
                self.population.append(Person(i, is_vaccinated=True))
            elif i < num_vaccinated + num_infected:
                self.population.append(Person(i, is_vaccinated=False, infection=self.virus))
            else:
                self.population.append(Person(i, is_vaccinated=False))

    def _simulation_should_continue(self):
        living = [p for p in self.population if p.is_alive]
        infected = [p for p in living if p.infection]
        return len(infected) > 0

    def run(self):
        step = 0
        self.logger.log_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)

        while self._simulation_should_continue():
            step += 1
            self.time_step(step)

        total_living = len([p for p in self.population if p.is_alive])
        total_vaccinated = len([p for p in self.population if p.is_vaccinated])
        self.logger.log_final_summary(total_living, self.total_dead, total_vaccinated)

    def time_step(self, step):
        self.new_infections = []

        for person in [p for p in self.population if p.is_alive and p.infection]:
            self.interact(person)

        deaths = 0
        for person in self.population:
            if person.is_alive and person.infection:
                if not person.did_survive_infection():
                    deaths += 1

        self.total_dead += deaths
        self.total_vaccinated = len([p for p in self.population if p.is_vaccinated])
        total_living = len([p for p in self.population if p.is_alive])
        total_infections = len([p for p in self.population if not p.is_alive or p.is_vaccinated])

        self.logger.log_step_summary(step, len(self.new_infections), deaths, total_living, self.total_dead, self.total_vaccinated, total_infections)

    def interact(self, person):
        for _ in range(100):
            random_person = random.choice(self.population)
            if not random_person.is_alive:
                continue
            if random_person.is_vaccinated:
                self.logger.log_interaction(person, random_person, False, "Already Vaccinated")
                continue
            if random_person.infection:
                self.logger.log_interaction(person, random_person, False, "Already Infected")
                continue

            if random.random() < self.virus.repro_rate:
                self.new_infections.append(random_person)
                random_person.infection = self.virus
                self.logger.log_interaction(person, random_person, True, "Infected")

if __name__ == "__main__":
    print("Welcome to the Herd Immunity Simulation!")
    try:
        while True:
            # Collect user inputs
            pop_size = int(input("Enter Population Size: "))
            vacc_percentage = float(input("Enter Vaccination Percentage (e.g., 0.1 for 10%): "))
            virus_name = input("Enter Virus Name: ")
            mortality_rate = float(input("Enter Mortality Rate (e.g., 0.12 for 12%): "))
            repro_rate = float(input("Enter Reproduction Rate (e.g., 0.5 for 50%): "))
            initial_infected = int(input("Enter Number of People Initially Infected: "))

            # Validate inputs
            if initial_infected > pop_size:
                raise ValueError("Number of initially infected people cannot exceed the population size.")

            # Create the virus and simulation instances
            virus = Virus(virus_name, repro_rate, mortality_rate)
            sim = Simulation(pop_size, vacc_percentage, virus, initial_infected)
            sim.run()

            # Ask the user if they want to test for another disease
            retry = input("Would you like to test for a different disease? (Y/N): ").strip().lower()
            if retry != 'y':
                print("Exiting the program. Thank you!")
                break

    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
