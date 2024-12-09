class IDGenerator:
    current_id = 3

    @staticmethod
    def generate_id():
        unique_id = IDGenerator.current_id
        IDGenerator.current_id += 1
        return unique_id