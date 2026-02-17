import random

class Character:
    def __init__(self, name, health, attack, special_ability):
        self.name = name
        self.health = health
        self.attack = attack
        self.special_ability = special_ability

    def is_alive(self):
        return self.health > 0

    def use_special(self):
        return self.special_ability

    def take_damage(self, damage):
        self.health -= damage

    def __str__(self):
        return f'{self.name} - Health: {self.health}, Attack: {self.attack}'

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage

    def attack_player(self):
        return self.attack

    def __str__(self):
        return f'{self.name} - Health: {self.health}'

class Game:
    def __init__(self):
        self.characters = [
            Character('Warrior', 100, 15, "Double Strike"),
            Character('Mage', 80, 20, "Fireball"),
            Character('Rogue', 90, 18, "Sneak Attack")
        ]
        self.enemy = Enemy('Alien', 120, 12)

    def choose_character(self):
        print('Choose your character:')
        for index, character in enumerate(self.characters):
            print(f'{index + 1}: {character}')

        choice = int(input('Enter the number of your choice: ')) - 1
        return self.characters[choice]

    def player_turn(self, player):
        print(f'\n{player.name}, it is your turn!')
        action = input("Choose action: (1: Attack, 2: Special Ability) ")

        if action == '1':
            damage = player.attack
            self.enemy.take_damage(damage)
            print(f'You attacked the enemy for {damage} damage!')
        elif action == '2':
            ability = player.use_special()
            self.enemy.take_damage(30)  # Example fixed damage
            print(f'You used {ability} and dealt 30 damage to the enemy!')

    def enemy_turn(self):
        if self.enemy.is_alive():
            damage = self.enemy.attack_player()
            print(f'The enemy attacks you for {damage} damage!')

    def start(self):
        player = self.choose_character()
        print(f'You chose {player.name}')

        while player.is_alive() and self.enemy.is_alive():
            self.player_turn(player)
            self.enemy_turn()
            print(f'\n{self.enemy}')

        if player.is_alive():
            print('You defeated the enemy!')
        else:
            print('You have been defeated!')

if __name__ == '__main__':
    game = Game()
    game.start()