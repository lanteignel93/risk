import sys
import warnings
import copy
import pprint
import time
from typing import NamedTuple
import numpy as np


class PlayerDistribution(NamedTuple):
    name: str
    distribution_arr: np.ndarray


class Player:
    def __init__(self, name: str, territories: int):
        self._name = name
        self._territories = territories
        self._arr_troops = np.ones(territories)

    @property
    def troops(self):
        return self._arr_troops

    @property
    def name(self):
        return self._name

    @property
    def territories(self):
        return self._territories


class Risk:
    _troop_count = {2: 40, 3: 35, 4: 30, 5: 25, 6: 20}
    _num_territory_cards = 42
    _num_wild_cards = 2

    def __init__(self, num_players: int):
        self._players = []
        self._num_players = num_players

    @property
    def num_players(self):
        return self._num_players

    def add_player(self, player: Player):
        self._players.append(player)

    def get_player_num_territories(self) -> int:
        num_attempts_allowed = 5

        max_terr_cnt = np.ceil(
            (self._num_territory_cards + self._num_wild_cards) / self.num_players
        ).astype(int)
        min_terr_cnt = ((self._num_territory_cards + self._num_wild_cards) // self.num_players) - self._num_wild_cards
        while num_attempts_allowed > 0:
            try:
                count = int(input("Enter number of territories: "))
            except ValueError:
                warnings.warn(
                    f"Invalidate Type Input, please enter an integer between {min_terr_cnt} and {max_terr_cnt}.",
                    stacklevel=1,
                )
                num_attempts_allowed -= 1
                continue

            if count < min_terr_cnt or count > max_terr_cnt:
                warnings.warn(
                    f"Invalidate Value Input, please enter an integer between {min_terr_cnt} and {max_terr_cnt}.",
                    stacklevel=1,
                )
                num_attempts_allowed -= 1

            else:
                return count

        raise RuntimeError("Number of attemps failed. Program exit.")

    def init_players(self):
        tot_number_territories = copy.copy(self._num_territory_cards)
        for _ in range(self.num_players):
            name = input("Enter your name: ")
            num_terr = self.get_player_num_territories()
            tot_number_territories -= num_terr
            self.add_player(Player(name=name, territories=num_terr))

        if tot_number_territories != 0:
            num_terr_accounted_for = self._num_territory_cards - tot_number_territories
            raise ValueError(
                f"Terminating Program, there were {num_terr_accounted_for} Territories accounted for \n \
                  Please check each player cards. "
            )

        return None

    def generate_random_allocation(self):
        self.init_players()
        num_of_troops = self._troop_count[self.num_players]
        player_ndarray = []

        for player in self._players:
            troops = player.troops
            name = player.name
            num_territories = player.territories
            num_add_troops = num_of_troops - num_territories

            for _ in range(num_add_troops):
                troops[int(np.random.randint(num_territories))] += 1

            troop_dis = {f"Territory {i+1}": int(troops[i]) for i in range(len(troops))}
            player_ndarray.append(
                PlayerDistribution(name=name, distribution_arr=troops)
            )

            print(f" \n{name} troops distribution:")

            pprint.pprint(troop_dis, sort_dicts=False)
            
        print('\n')
        player_rank_dict = {}
        for player_distr in player_ndarray:
            theo_std = return_theo_std(num_players=self.num_players, num_territories=len(player_distr.distribution_arr))
            actual_std = player_distr.distribution_arr.std()
            if actual_std > theo_std:
                rank = "better"
                sign = "+"
            else:
                rank = "worse"
                sign = "-"
            
            rel_std = (actual_std/theo_std - 1)
            player_rank_dict[player_distr.name] = rel_std * 100 
            print(
                f"{player_distr.name}:: Troops STD: {actual_std :.3f}, Theoretical STD: {theo_std :.3f}, {sign}{100 * abs(rel_std): .2f}% {rank} STD than Theo."
            )
            
        print("Player Relative STD Ranking:")
        pprint.pprint(player_rank_dict)

def return_theo_std(num_players: int, num_territories: int):
    theo_stds = {
        (2, 20) : 0.9635745477314908,
        (2, 21): 0.9180822569592594, 
        (2, 22): 0.8740197525744429, 
        (3, 12): 1.298274028415833,
        (3, 13): 1.2248953558756124,
        (3, 14): 1.1584803925101936,
        (3, 15): 1.1584803925101936,
        (4, 9): 1.3992841362826913,
        (4, 10): 1.3065546805169754, 
        (4, 11): 1.2230916524434108, 
        (5, 6): 1.5481111647264714,
        (5, 7): 1.4273512481610773,
        (5, 8): 1.4273512481610773,
        (5, 9): 1.2212116591283604, 
        (6, 5): 1.46134964090963,
        (6, 6): 1.3325576470588079,
        (6, 7): 1.2160876250085135,
        (6, 8): 1.1100555909837486
    }
    
    return theo_stds[(num_players, num_territories)]

def print_welcome_message():
    print("******************************************************************")
    print("\t Welcome To Risk Random Army Distribution Software \t")
    print("****************************************************************** \n")


def get_player_count() -> int:
    num_attempts_allowed = 5
    while num_attempts_allowed > 0:
        try:
            count = int(input("Enter Number of Players: "))
        except ValueError:
            warnings.warn(
                "Invalidate Type Input, please enter an integer between 2 and 6.",
                stacklevel=1,
            )
            num_attempts_allowed -= 1
            continue

        if count < 2 or count > 6:
            warnings.warn(
                "Invalidate Value Input, please enter an integer between 2 and 6",
                stacklevel=1,
            )
            num_attempts_allowed -= 1

        else:
            return count

    raise RuntimeError("Number of attemps failed. Program exit.")

class TroopRange(NamedTuple):
    min_val: int
    max_val: int 
    max_troop: int
    
def monte_carlo(n: int = 100000):
    dic_troop_map = {
        2: TroopRange(min_val=20, max_val=22, max_troop=40),
        3: TroopRange(min_val=12, max_val=15, max_troop=35),
        4: TroopRange(min_val=9, max_val=11, max_troop=30),
        5: TroopRange(min_val=6, max_val=9, max_troop=25),
        6: TroopRange(min_val=5, max_val=8, max_troop=20),
    }
    for num_players in np.arange(2,7,1):
        sim_mean = {}
        troop_range = dic_troop_map[num_players]
        for terr_count in np.arange(troop_range.min_val, troop_range.max_val +1, 1):
            troops_mc_std = []
            for sim in range(n):
                num_new_troops = troop_range.max_troop - terr_count
                troops = np.ones(terr_count)
                for _ in range(num_new_troops):
                    troops[int(np.random.randint(terr_count))] += 1
                troops_mc_std.append(troops.std())
            sim_mean[terr_count] = np.array(troops_mc_std).mean()
        print(f"\n{num_players} Players:")
        pprint.pprint(sim_mean, width=40)
        
def run_monte_carlo():
    t1 = time.time()
    monte_carlo(100000)
    print(time.time() - t1)
    
    
def main():
    print_welcome_message()
    player_count = get_player_count()
    game = Risk(num_players=player_count)
    game.generate_random_allocation()
    input("Press enter to exit ;)")
    sys.exit(0)
    
if __name__ == "__main__":
    main()