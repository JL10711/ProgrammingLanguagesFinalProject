import random
import asyncio

class Creature:
    def __init__(self, name, hp, attacks):
        self.name = name
        self.hp = hp
        self.attacks = attacks

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        print(f"{self.name} takes {damage} damage! ({self.hp} HP left)")

    async def player_turn(self, opponent):
        print(f"\n--- {self.name}'s Turn ---")
        print("Choose an attack:")
        for i, (atk, dmg) in enumerate(self.attacks.items(), 1):
            print(f"{i}. {atk} ({dmg} dmg)")
        choice = None
        while choice not in range(1, len(self.attacks) + 1):
            try:
                choice = int(input("Enter choice: "))
            except ValueError:
                pass
        atk_name = list(self.attacks.keys())[choice - 1]
        damage = self.attacks[atk_name]
        print(f"{self.name} uses {atk_name}!")
        opponent.take_damage(damage)
        await asyncio.sleep(0)

    async def ai_turn(self, opponent):
        print(f"\n--- {self.name}'s Turn ---")
        atk_name, damage = random.choice(list(self.attacks.items()))
        print(f"{self.name} uses {atk_name}!")
        opponent.take_damage(damage)
        await asyncio.sleep(0)


async def battle(player, enemy):
    print(f"A wild {enemy.name} appears!")
    await asyncio.sleep(0)

    player_turn = player.player_turn(enemy)
    ai_turn = enemy.ai_turn(player)

    while player.is_alive() and enemy.is_alive():
        await player.player_turn(enemy)
        if not enemy.is_alive():
            break
        await enemy.ai_turn(player)

    if player.is_alive():
        print(f"\n{enemy.name} fainted! You win!")
    else:
        print(f"\n{player.name} fainted! You lose!")


if __name__ == "__main__":
    player = Creature("Pika", 50, {
        "Thunder Shock": 10,
        "Quick Attack": 8,
        "Electro Ball": 12
    })

    enemy = Creature("Zilla", 45, {
        "Scratch": 7,
        "Poison Sting": 9,
        "Bite": 11
    })

    asyncio.run(battle(player, enemy))
