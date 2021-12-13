class LanternfishSchool:
    def __init__(self, initial_states=None, min_state=None, max_state=None):
        self._count_per_fish_state = {}

        if initial_states is not None:
            for state in range(min_state, max_state+1):
                self._count_per_fish_state[state] = float(sum(initial_states == state))

    def copy(self):
        new_school = LanternfishSchool()
        for key in self._count_per_fish_state.keys():
            new_school._count_per_fish_state[key] = self._count_per_fish_state[key]
        return new_school

    def run_school_simulation(self, days):
        for day in range(0, days):
            school_copy = self.copy()

            for key in self._count_per_fish_state.keys():
                if key == 8:
                    self._count_per_fish_state[key] = school_copy._count_per_fish_state[0]
                elif key == 6:
                    self._count_per_fish_state[key] = school_copy._count_per_fish_state[key + 1] + \
                                                      school_copy._count_per_fish_state[0]
                else:
                    self._count_per_fish_state[key] = school_copy._count_per_fish_state[key + 1]

    def get_total_fish_amount(self):
        return sum(self._count_per_fish_state.values())
