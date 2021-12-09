class LanternfishSchool:
    def __init__(self, initial_states=None):
        self.initial_states = initial_states

        if initial_states is not None:
            self.fish_at_0 = float(sum(initial_states == 0))
            self.fish_at_1 = float(sum(initial_states == 1))
            self.fish_at_2 = float(sum(initial_states == 2))
            self.fish_at_3 = float(sum(initial_states == 3))
            self.fish_at_4 = float(sum(initial_states == 4))
            self.fish_at_5 = float(sum(initial_states == 5))
            self.fish_at_6 = float(sum(initial_states == 6))
            self.fish_at_7 = float(sum(initial_states == 7))
            self.fish_at_8 = float(sum(initial_states == 8))

    def copy(self):
        new_school = LanternfishSchool()
        new_school.fish_at_0 = self.fish_at_0
        new_school.fish_at_1 = self.fish_at_1
        new_school.fish_at_2 = self.fish_at_2
        new_school.fish_at_3 = self.fish_at_3
        new_school.fish_at_4 = self.fish_at_4
        new_school.fish_at_5 = self.fish_at_5
        new_school.fish_at_6 = self.fish_at_6
        new_school.fish_at_7 = self.fish_at_7
        new_school.fish_at_8 = self.fish_at_8
        return new_school

    def run_school_simulation(self, days):
        for day in range(0, days):
            school_copy = self.copy()

            self.fish_at_8 = school_copy.fish_at_0
            self.fish_at_7 = school_copy.fish_at_8
            self.fish_at_6 = school_copy.fish_at_7 + school_copy.fish_at_0
            self.fish_at_5 = school_copy.fish_at_6
            self.fish_at_4 = school_copy.fish_at_5
            self.fish_at_3 = school_copy.fish_at_4
            self.fish_at_2 = school_copy.fish_at_3
            self.fish_at_1 = school_copy.fish_at_2
            self.fish_at_0 = school_copy.fish_at_1

    def get_total_fish_amount(self):
        return self.fish_at_0 + self.fish_at_1 + self.fish_at_2 + self.fish_at_3 + self.fish_at_4 + self.fish_at_5 +  \
               self.fish_at_6 + self.fish_at_7 + self.fish_at_8
