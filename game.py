

from cards import Deck, hand_value


class Blackjack:
    def __init__(self):
        self.chips = 100

    def show(self, player, dealer, hide=True):
        shown_dealer = [f"{dealer[0][0]}{dealer[0][1]}", "??"] if hide else [
            f"{r}{s}" for r, s in dealer
        ]
        print("Dealer:", " ".join(shown_dealer))
        print("Player:", " ".join(f"{r}{s}" for r, s in player),
              "=", hand_value(player))

    def draw_card(self, deck, hand, name):
        card = deck.draw()
        if card is None:
            print("Deck is empty.")
            return False
        hand.append(card)
        print(f"{name} draws {card[0]}{card[1]}.")
        return True

    def settle(self, bet, result):
        if result == "win":
            self.chips += bet * 2
            print("Player wins!")
        elif result == "blackjack":
            self.chips += bet + bet * 3 // 2
            print("BLACKJACK! 3:2 payout!")
        elif result == "push":
            self.chips += bet
            print("Push! Bet returned.")
        else:
            print("Dealer wins.")
        print("Chip balance:", self.chips)

    def round(self):
        if self.chips <= 0:
            print("No chips left.")
            return False

        while True:
            try:
                bet = int(input(f"Enter wager (1-{self.chips}): "))
                if 1 <= bet <= self.chips:
                    break
                print("Invalid wager.")
            except ValueError:
                print("Enter a valid whole number.")

        self.chips -= bet
        deck = Deck()
        player = [deck.draw(), deck.draw()]
        dealer = [deck.draw(), deck.draw()]

        print("\n--- New Round ---")
        self.show(player, dealer)

        player_natural = hand_value(player) == 21
        dealer_natural = hand_value(dealer) == 21

        if player_natural or dealer_natural:
            self.show(player, dealer, hide=False)
            if player_natural and dealer_natural:
                self.settle(bet, "push")
            elif player_natural:
                self.settle(bet, "blackjack")
            else:
                self.settle(bet, "lose")
            return True

        while True:
            value = hand_value(player)
            if value > 21:
                print("Player busts!")
                self.settle(bet, "lose")
                return True
            if value == 21:
                break

            key = input("[h]it [s]tand [q]uit: ").strip().lower()

            if key == "q":
                self.chips += bet
                print("Round cancelled. Bet returned.")
                return False
            elif key == "s":
                break
            elif key == "h":
                if not self.draw_card(deck, player, "Player"):
                    self.chips += bet
                    return False
                self.show(player, dealer)
            else:
                print("Invalid command. Enter h, s, or q.")

        print("\nDealer's turn.")
        self.show(player, dealer, hide=False)

        while hand_value(dealer) < 17:
            if not self.draw_card(deck, dealer, "Dealer"):
                self.chips += bet
                return False

        self.show(player, dealer, hide=False)

        pv = hand_value(player)
        dv = hand_value(dealer)

        if dv > 21 or pv > dv:
            self.settle(bet, "win")
        elif pv < dv:
            self.settle(bet, "lose")
        else:
            self.settle(bet, "push")

        return True

    def run(self):
        print("Blackjack - starting chips:", self.chips)

        while self.chips > 0:
            if not self.round():
                if self.chips <= 0:
                    break
                choice = input("Play another round? [y/n]: ").strip().lower()
                if choice != "y":
                    break
                continue

            if self.chips <= 0:
                break

            choice = input("Play again? [y/n]: ").strip().lower()
            while choice not in {"y", "n"}:
                print("Invalid command. Enter y or n.")
                choice = input("Play again? [y/n]: ").strip().lower()
            if choice == "n":
                break

        print("\nGame over!")
        print("Final chip balance:", self.chips)
