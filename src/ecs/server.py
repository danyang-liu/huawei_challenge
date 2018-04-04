class Server(object):
    def __init__(self,cpu_size,mem_size,hard_disk_size):
        self.cpu_size = cpu_size
        self.mem_size = mem_size
        self.hard_disk_size = hard_disk_size
        self.free_cpu_size = cpu_size
        self.free_mem_size = mem_size
        self.flavor_num = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    def put_flavor(self,flavor_type,cpu_size,mem_size):
        if cpu_size>self.free_cpu_size or mem_size>self.free_cpu_size:
            return False
        else:
            self.flavor_num[flavor_type-1] = self.flavor_num[flavor_type-1] + 1
            self.free_cpu_size = self.free_cpu_size - cpu_size
            self.free_mem_size = self.free_mem_size - mem_size
            return True

    def pop_flavor(self):
        pass