class Shop:

    def __init__(self, power_list, player):
        self.power_list = power_list
        self.player = player
        self.open = False
        self.shop_background = None

    def open(self):
        pass

    def draw_shop(self):
        self.shop_background.fill((100, 250, 250))
