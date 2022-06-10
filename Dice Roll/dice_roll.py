import random
from dices import *

def dice_roll():
    play = True

    while play:
        number_of_dices = get_number_of_rolls()

        dice_rolls = [random.randint(1, 6) for _ in range(number_of_dices)]
        print_dices(dice_rolls)

        play = is_play_again()


def get_number_of_rolls():
    valid_num = False
    while not valid_num: 
        try:
            number_of_dices = int(input("\nHow many dice do you want to roll? (1-6): "))
            if number_of_dices not in range(1, 7):
                raise ValueError
            valid_num = True
            return number_of_dices
        except ValueError:
                print("Invalid input, please add a number between 1-6!\n")


def print_dices(dice_rolls):
    dice_tops = get_dice_tops(dice_rolls)
    dices_list = generate_dices(dice_tops)

    width = len(dices_list[0])
    header = " Roll Results ".center(width, "-")

    dice_visual = "\n".join([header] + dices_list)
    print(dice_visual)


def get_dice_tops(dice_rolls):
    return [dice_map[roll] for roll in dice_rolls]


def generate_dices(dice_tops):
    dices_list = []
    for row in range(dice_height):
        dice_rows = []
        for dice in dice_tops:
            dice_rows.append(dice[row])
        dice = dice_separator.join(dice_rows)
        dices_list.append(dice)
    return dices_list


def is_play_again():
    while True:
        try:
            play_again = input("Do you want to roll again? (Y)es or (N)o: ").upper()
            if play_again != "Y" and play_again != "N":
                raise ValueError
            play = True if play_again == "Y" else False
            return play
        except ValueError:
            print("Invalid keyword, please enter (Y)es or (N)o!\n")

dice_roll()