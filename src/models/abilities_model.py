from typing import Union
from characters.hero import Hero
from models.enemy_model import EnemyModel

class Ability_Model():
    def __init__(self, name: str, cooldown: int):
        """
        Classe base para todas as habilidades.

        :param name: Nome da habilidade.
        :param cooldown: Turnos de recarga antes que a habilidade possa ser usada novamente.
        """
        self.name = name
        self.cooldown = cooldown
        self.current_cooldown = 0

    def use_ability(self, target: Union[EnemyModel, Hero]) -> str:

        raise NotImplementedError("Subclasses devem implementar o método 'use_ability'.")

    def reduce_cooldown(self):
        """
        Reduz a recarga da habilidade ao final de um turno.
        """
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def is_ready(self) -> bool:
        """
        Verifica se a habilidade está pronta para uso.

        :return: True se a habilidade pode ser usada, False caso contrário.
        """
        return self.current_cooldown == 0
