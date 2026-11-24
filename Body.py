class Body:

    def __init__(self, mass, capacity, temperature):
        self.mass = mass
        self.capacity = capacity
        self.temperature = temperature

    def add_heat(self, heat):
        delta_temperature = heat/(self.mass*self.capacity)
        self.temperature = self.temperature + delta_temperature
        return self.temperature

if __name__ == '__main__':
    body1 = Body(100,0.15,200)
    print(body1.add_heat(20))
    print(body1.add_heat(-40))
