import numpy as np 
from typing import NamedTuple

class RiskAttackReport(NamedTuple):
    atk_troop_lost: int 
    def_troop_lost: int 

def execute_attack(atk_player_cnt: int, def_player_cnt: int) -> RiskAttackReport:
    if not ((isinstance(atk_player_cnt, int)) and (isinstance(def_player_cnt, int))):
        return AssertionError("Wrong Input needs to be an Integer")
    if atk_player_cnt < 1 or atk_player_cnt > 3:
        return ValueError("Attack Player Must have at least 1 and at most 3 attacking troops.")
    if def_player_cnt < 1 or def_player_cnt > 2:
        return ValueError("Defending Player Must have at least 1 and at most 2 defending troops.")
    
    atk_dice_rolls = np.array(sorted(np.random.randint(1, 7, atk_player_cnt), reverse=True))
    def_dice_rolls = np.array(sorted(np.random.randint(1, 7, def_player_cnt), reverse=True))
    
    number_valid_attackers = np.minimum(np.minimum(2, atk_player_cnt),def_player_cnt)
    number_valid_defenders = np.minimum(number_valid_attackers, def_player_cnt)
    atk_dice_rolls = atk_dice_rolls[
        : number_valid_attackers 
    ]
    def_dice_rolls = def_dice_rolls[:number_valid_defenders]
    res = atk_dice_rolls - def_dice_rolls
    num_def_lost = np.where(res > 0, 1, 0).sum()
    num_atk_lost = number_valid_defenders - num_def_lost
    
    return RiskAttackReport(
        atk_troop_lost=num_atk_lost,
        def_troop_lost=num_def_lost
    )
    
class RiskMassAttackReport(NamedTuple):
    atk_player_troop: int
    def_player_troop: int

def execute_mass_attack(
    atk_player_troop_cnt: int, 
    def_player_troop_cnt: int,
    atk_player_cnt_stop: int | None = None
    ) -> RiskMassAttackReport:
    
    if atk_player_cnt_stop is None:
        atk_player_cnt_stop = 1
        
    while (atk_player_troop_cnt > np.maximum(2, atk_player_cnt_stop)) and def_player_troop_cnt > 0:
        available_troops_atk = atk_player_troop_cnt - 1 
        atk_troop_cnt = int(np.minimum(available_troops_atk, 3))
        def_troop_cnt = int(np.minimum(def_player_troop_cnt, 2))
        
        battle_res = execute_attack(atk_player_cnt=atk_troop_cnt, def_player_cnt=def_troop_cnt)
        
        atk_player_troop_cnt -= battle_res.atk_troop_lost
        def_player_troop_cnt -= battle_res.def_troop_lost
        
    return RiskMassAttackReport(
        atk_player_troop=atk_player_troop_cnt,
        def_player_troop=def_player_troop_cnt
    )
        
    
def main():
    for _ in range(100):
        print(execute_mass_attack(42,42,10))
    
if __name__ == "__main__":
    main()