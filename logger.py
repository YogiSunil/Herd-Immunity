import datetime

class Logger:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'w') as file:
            file.write(f"Simulation Log - {datetime.datetime.now()}\n\n")

    def log_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, repro_rate):
        with open(self.filename, 'a') as file:
            file.write(f"Simulation Date: {datetime.datetime.now()}\n")
            file.write(f"Initial Population Size: {pop_size}\n")
            file.write(f"Initial Infected People: {vacc_percentage * pop_size:.0f}\n")
            file.write(f"Virus Name: {virus_name}\n")
            file.write(f"Virus Mortality Rate: {mortality_rate * 100:.2f}%\n")
            file.write(f"Virus Reproduction Rate: {repro_rate * 100:.2f}%\n")
            file.write("=== Start of Simulation ===\n\n")

    def log_step_summary(self, step, new_infections, deaths, total_living, total_dead, total_vaccinated, total_infections):
        with open(self.filename, 'a') as file:
            file.write(f"Step {step}:\n")
            file.write(f"  New Infections: {new_infections}\n")
            file.write(f"  Deaths This Step: {deaths}\n")
            file.write(f"  Total Living: {total_living}\n")
            file.write(f"  Total Dead: {total_dead}\n")
            file.write(f"  Total Vaccinated: {total_vaccinated}\n")
            file.write("\n")

    def log_interaction(self, person, random_person, did_infect, reason):
        with open(self.filename, 'a') as file:
            if did_infect:
                file.write(f"Person {person._id} infected Person {random_person._id}.\n")
            else:
                file.write(f"Interaction between Person {person._id} and Person {random_person._id} - {reason}.\n")

    def log_final_summary(self, total_living, total_dead, total_vaccinated):
        with open(self.filename, 'a') as file:
            file.write("Final Summary:\n")
            file.write(f"Total Living: {total_living}\n")
            file.write(f"Total Dead: {total_dead}\n")
            file.write(f"Total Vaccinated: {total_vaccinated}\n")
