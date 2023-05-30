class BaseBoss:

    def __init__(self, life: int = 2500, armor_class: int = 17):
        self.life = life
        self.armor_class = armor_class
        self.__initial_life = life

    def get_initial_life(self):
        return self.__initial_life
