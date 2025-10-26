# ============================================================
# IMPORT LIBRARIES
# ============================================================
import time
import sys


# ============================================================
# FUNCTION DEFINITIONS
# ============================================================

def print_slow(text, delay=0.03):
    """Print text with typing effect for immersion"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_separator():
    """Print visual separator between story sections"""
    print("\n" + "~" * 50 + "\n")


def get_choice(options):
    """
    Get valid user input from list of options
    Args:
        options: list of valid choice numbers (as strings)
    Returns:
        validated user choice as string
    """
    while True:
        choice = input("\nWhat do you do? ").strip()
        if choice in options:
            return choice
        else:
            print(f"Please pick 1 or 2!")


def game_over(message, success=False):
    """
    Display game over message and exit
    Args:
        message: ending message to display
        success: whether player won (True) or lost (False)
    """
    print_separator()
    if success:
        print_slow("🎉 THE END - YOU WIN! 🎉")
    else:
        print_slow("💙 THE END - TRY AGAIN! 💙")
    print()
    print_slow(message)
    print_separator()
    print_slow("Thanks for playing!")
    sys.exit()


# ============================================================
# GAME VARIABLES
# ============================================================

# Player info
player_name = ""
friends_made = 0

# Character names
dolphin_name = "Splash"
turtle_name = "Shelly"
octopus_name = "Inky"
shark_name = "Finn"


# ============================================================
# GAME START
# ============================================================

print_separator()
print_slow("🐠 THE LITTLE FISH'S BIG ADVENTURE 🐠", delay=0.05)
print_separator()

# Get player name
player_name = input("What is your fish's name? ").strip()
if not player_name:
    player_name = "Bubbles"

print_slow(f"\nHello {player_name}! You are a small, colorful fish.")
print_slow("Today is your first day exploring the big ocean all by yourself!")
time.sleep(1)


# ============================================================
# CHOICE 1: WHO TO ASK FOR HELP
# ============================================================

print_separator()
print_slow(f"""
You swim away from your coral home, excited to explore!
But soon you realize... the ocean is HUGE! You're not sure
which way to go.

Up ahead you see two of your neighbors:
- {dolphin_name} the friendly dolphin is jumping and playing
- {turtle_name} the wise old sea turtle is swimming slowly
""")

print_separator()
print("1. Swim up to ask Splash the dolphin for help")
print("2. Swim over to ask Shelly the turtle for help")

choice_1 = get_choice(["1", "2"])


# ============================================================
# PATH A: DOLPHIN FRIEND
# ============================================================

if choice_1 == "1":
    friends_made += 1
    print_separator()
    print_slow(f"""
You swim up to {dolphin_name}.

'{player_name}!' she clicks happily. 'Want to come play with me?
I know two fun places! There's a cave with glowing jellyfish,
or we could visit my friend {octopus_name} the octopus!'
""")
    
    # ============================================================
    # CHOICE 2A: WHERE TO GO WITH DOLPHIN
    # ============================================================
    
    print_separator()
    print("1. Go see the glowing jellyfish cave")
    print("2. Go meet Inky the octopus")
    
    choice_2a = get_choice(["1", "2"])
    
    if choice_2a == "1":
        print_separator()
        print_slow(f"""
{dolphin_name} leads you to a beautiful cave. Inside, hundreds of
jellyfish glow like little lanterns - pink, blue, and green!

'They're moon jellies,' {dolphin_name} explains. 'They won't sting
you! Want to swim through them, or just watch from here?'
""")
        
        # ============================================================
        # CHOICE 3A: JELLYFISH DECISION
        # ============================================================
        
        print_separator()
        print("1. Swim through the glowing jellyfish")
        print("2. Stay safe and just watch them")
        
        choice_3a = get_choice(["1", "2"])
        
        if choice_3a == "1":
            # Good ending - brave
            friends_made += 1
            game_over(
                f"{dolphin_name} was right! The jellyfish are gentle and friendly.\n"
                f"You swim through them and they glow even brighter around you!\n"
                f"It's the most beautiful thing you've ever seen.\n\n"
                f"The jellyfish crown you 'Bravest Little Fish' and now you\n"
                f"have magical friends who will light your way forever!\n\n"
                f"You made {friends_made} new friends today!",
                success=True
            )
        else:
            # Okay ending - safe choice
            game_over(
                f"You watch the beautiful jellyfish dance and glow.\n"
                f"{dolphin_name} swims through them to show you a cool trick.\n\n"
                f"It's pretty, but you wonder what it would have felt like\n"
                f"to swim with them. Maybe next time you'll be braver!\n\n"
                f"You made {friends_made} new friend today!",
                success=False
            )
    
    else:  # choice_2a == "2"
        friends_made += 1
        print_separator()
        print_slow(f"""
You and {dolphin_name} swim to a rocky area. {octopus_name} pops out
from behind a rock!

'Hello!' he says, changing colors from red to purple to blue.
'I'm practicing my color changing. Want to play hide and seek?
Or would you rather hear a story about the old shipwreck?'
""")
        
        # ============================================================
        # CHOICE 3B: OCTOPUS ACTIVITY
        # ============================================================
        
        print_separator()
        print("1. Play hide and seek with Inky")
        print("2. Listen to the shipwreck story")
        
        choice_3b = get_choice(["1", "2"])
        
        if choice_3b == "1":
            # Good ending - playful
            friends_made += 1
            game_over(
                f"You play hide and seek! {octopus_name} is SO good at hiding\n"
                f"because he can change colors and squeeze into tiny spaces.\n\n"
                f"But you find the BEST hiding spot inside a giant clam shell!\n"
                f"Everyone agrees you won the game.\n\n"
                f"{octopus_name} and {dolphin_name} want to play with you every day!\n\n"
                f"You made {friends_made} new friends today!",
                success=True
            )
        else:
            # Good ending - curious
            friends_made += 1
            game_over(
                f"{octopus_name} tells an amazing story about a sunken pirate ship\n"
                f"full of treasure! He shows you a shiny coin he found there.\n\n"
                f"'Maybe tomorrow we can all go explore it together!' he says.\n\n"
                f"{dolphin_name} and {octopus_name} are excited to have a new friend\n"
                f"who loves adventures!\n\n"
                f"You made {friends_made} new friends today!",
                success=True
            )


# ============================================================
# PATH B: TURTLE FRIEND  
# ============================================================

else:  # choice_1 == "2"
    friends_made += 1
    print_separator()
    print_slow(f"""
You swim over to {turtle_name}.

'Ah, young {player_name},' she says in a slow, kind voice.
'First time out alone? I remember my first adventure!
I can show you the peaceful kelp forest, or if you're brave,
I know where {shark_name} the shark lives. He's actually very nice!'
""")
    
    # ============================================================
    # CHOICE 2B: WHERE TO GO WITH TURTLE
    # ============================================================
    
    print_separator()
    print("1. Visit the peaceful kelp forest")
    print("2. Go meet Finn the shark (sounds scary!)")
    
    choice_2b = get_choice(["1", "2"])
    
    if choice_2b == "1":
        print_separator()
        print_slow(f"""
{turtle_name} takes you to a tall underwater forest made of kelp.
Sea horses float by, and you see otters playing above you!

'This is my favorite place,' {turtle_name} says. 'So peaceful.
Would you like to rest here with me, or explore deeper into
the forest?'
""")
        
        # ============================================================
        # CHOICE 3C: KELP FOREST DECISION
        # ============================================================
        
        print_separator()
        print("1. Rest peacefully with Shelly")
        print("2. Explore deeper into the kelp forest")
        
        choice_3c = get_choice(["1", "2"])
        
        if choice_3c == "1":
            # Good ending - peaceful
            game_over(
                f"You rest in the kelp forest with {turtle_name}.\n"
                f"She tells you stories about the ocean and teaches you\n"
                f"about all the creatures that live here.\n\n"
                f"You learn so much! A family of sea horses even lets\n"
                f"you watch their babies hatch!\n\n"
                f"Sometimes the best adventures are quiet ones.\n\n"
                f"You made {friends_made} new friend today!",
                success=True
            )
        else:
            # Okay ending - got lost
            game_over(
                f"You swim deeper into the kelp forest, but it's like a maze!\n"
                f"You get a little lost and can't find {turtle_name}.\n\n"
                f"Luckily, a friendly sea otter helps you find your way back.\n"
                f"{turtle_name} is waiting for you.\n\n"
                f"'Always stay close to your friends in new places,' she\n"
                f"advises gently. You learned an important lesson!\n\n"
                f"You made {friends_made} new friend today.",
                success=False
            )
    
    else:  # choice_2b == "2"
        friends_made += 1
        print_separator()
        print_slow(f"""
{turtle_name} takes you to a deep part of the reef. A big shark
swims toward you! You're scared, but {turtle_name} stays calm.

'Hello {shark_name}!' she calls out.

The shark smiles (as much as sharks can smile). 'Hey {turtle_name}!
Who's your little friend? I was just about to eat lunch. Want
to join me? I caught some yummy fish!'

Wait... eat FISH? You're a fish!
""")
        
        # ============================================================
        # CHOICE 3D: SHARK DECISION
        # ============================================================
        
        print_separator()
        print("1. Trust Shelly and stay for lunch")
        print("2. Say 'no thank you' and swim away fast")
        
        choice_3d = get_choice(["1", "2"])
        
        if choice_3d == "1":
            # Good ending - trust
            friends_made += 1
            game_over(
                f"{turtle_name} laughs. 'Don't worry, {player_name}! {shark_name}\n"
                f"only eats tuna fish from the deep ocean, not little reef fish!'\n\n"
                f"{shark_name} nods. 'That's right! I would never eat a friend.\n"
                f"Come on, I have some tasty seaweed too!'\n\n"
                f"You have lunch with a SHARK! All your friends back home\n"
                f"will be so impressed. You learned that even scary-looking\n"
                f"creatures can be kind friends.\n\n"
                f"You made {friends_made} new friends today!",
                success=True
            )
        else:
            # Bad ending - ran away
            game_over(
                f"You swim away as fast as you can!\n\n"
                f"Later, {turtle_name} finds you. 'Oh {player_name}, {shark_name}\n"
                f"wouldn't hurt you! He only eats big tuna fish. You missed\n"
                f"a chance to make a wonderful friend.'\n\n"
                f"You feel a little silly. Maybe you should have trusted\n"
                f"{turtle_name}. She's very wise.\n\n"
                f"You made {friends_made} new friend, but missed meeting another.",
                success=False
            )