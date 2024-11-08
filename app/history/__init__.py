class History:
    """
    Class to manage the history of calculations.
    """
    def __init__(self):
        # Initialize an empty list to store calculations.
        self.calculations = []

    def add_calculation(self, calculation: str):
        """
        Adds a calculation to the history.
        :param calculation: String representation of the calculation.
        """
        if not isinstance(calculation, str):
            raise TypeError("Calculation must be a string.")
        self.calculations.append(calculation)

    def clear_history(self):
        """
        Clears all calculations from the history.
        """
        self.calculations.clear()

    def undo_last(self):
        """
        Removes the last calculation from the history.
        """
        if self.calculations:
            self.calculations.pop()
        else:
            print("History is already empty.")

    def get_history(self):
        """
        Retrieves a copy of the list of calculations.
        :return: List of calculations.
        """
        return self.calculations.copy()  # Ensures a copy is returned to prevent external modifications
