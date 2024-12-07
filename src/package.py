class Package:
    def __init__(self, id, start_v, start_time, dest_v, deadline):
        self.id = id
        self.start_v = start_v
        self.start_time = start_time
        self.dest_v = dest_v
        self.deadline = deadline
        self.is_delivered = False
