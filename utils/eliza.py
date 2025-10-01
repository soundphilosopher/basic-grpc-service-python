"""
🧠 Eliza - Your Friendly Neighborhood AI Therapist

Welcome to the classic Eliza chatbot implementation! This module provides
a Python version of the famous ELIZA program, originally created by Joseph
Weizenbaum at MIT in 1964-1966. Eliza simulates a Rogerian psychotherapist
using pattern matching and clever reflections.

Why Eliza? Because sometimes you need someone to listen, even if that someone
is just a bunch of regular expressions pretending to care! 🤖💕

Features:

- Pattern-based conversation simulation
- Pronoun reflection ("I am sad" -> "How long have you been sad?")
- Goodbye detection for natural conversation endings
- Randomized responses to keep things interesting
- Classic therapeutic responses that sound surprisingly human

Author: The AI Therapy Department 🛋️
"""

import re
import random
from dataclasses import dataclass


@dataclass
class Reply:
    """
    💬 A thoughtful response from our AI therapist.

    This dataclass encapsulates Eliza's responses, including both the
    actual text and whether it's time to say goodbye. Because even
    AI therapists need to end sessions eventually!

    Attributes:
        text (str): The wise words from Eliza
        goodbye (bool): True if this response ends the conversation

    Example:
        ```python
        reply = Reply("How does that make you feel?", False)
        reply.text
        "How does that make you feel?"

        reply.is_goodbye()
        False
        ```
    """
    text: str
    goodbye: bool = False

    def is_goodbye(self) -> bool:
        """
        🚪 Check if it's time to end the therapy session.

        Returns:
            bool: True if this reply indicates the conversation should end

        Note:
            This is just a convenience method because sometimes calling
            `reply.is_goodbye()` feels more natural than reply.goodbye! 🤷‍♀️
        """
        return self.goodbye


class Eliza:
    """
    🧠 The classic Eliza chatbot - Your digital Rogerian therapist!

    Eliza uses pattern matching and reflection techniques to simulate
    understanding and empathy. She's been helping people feel heard
    since 1966, making her one of the most experienced therapists
    in the business (even if she's not technically real).

    How Eliza Works:

    1. Matches your input against predefined patterns
    2. Reflects pronouns back at you ("I am" becomes "you are")
    3. Responds with contextually appropriate therapeutic responses
    4. Falls back to generic responses when confused
    5. Recognizes goodbye patterns to end conversations gracefully

    Therapeutic Specialties:

    - Active listening (pattern matching style!)
    - Pronoun reflection therapy
    - Question deflection techniques
    - Family inquiry methods
    - Emotional validation responses

    Example Session:

        >>> You: "I am feeling sad today"
        >>> Eliza: "Did you come to me because you are feeling sad today?"
        >>> You: "My mother never understood me"
        >>> Eliza: "Tell me more about your family."
        >>> You: "Goodbye"
        >>> Eliza: "Thank you for talking with me."
    """

    def __init__(self):
        """
        🎭 Initialize Eliza with her therapeutic training!

        Sets up all the patterns, responses, and reflection rules
        that make Eliza seem surprisingly human. Think of this as
        her going through therapy school, but really quickly.
        """

        # 🔄 Reflection dictionary for pronoun swapping
        # This is the secret sauce that makes "I am sad" become "you are sad"
        self.reflections = {
            "am": "are",
            "was": "were",
            "i": "you",
            "i'd": "you would",
            "i've": "you have",
            "i'll": "you will",
            "my": "your",
            "are": "am",
            "you've": "I have",
            "you'll": "I will",
            "your": "my",
            "yours": "mine",
            "you": "I",
            "me": "you",
            "myself": "yourself",
            "yourself": "myself"
        }

        # 👋 Goodbye patterns - Because every therapy session must end
        self.goodbye_patterns = [
            (r'.*(bye|goodbye|see you|farewell|quit|exit|leave).*', [
                "Thank you for talking with me.",
                "Good-bye. This was really a nice talk.",
                "Thank you, that will be $150. Have a good day!",  # 💰 Even AI therapists have bills!
                "Good-bye. I hope I have helped you.",
                "This was a nice session. Good-bye."
            ])
        ]

        # 🎯 Pattern-response pairs - Eliza's therapeutic toolkit
        # Each tuple contains (regex_pattern, list_of_possible_responses)
        self.patterns = [
            # Apology handling - We don't need no stinkin' apologies!
            (r'.*\bsorry\b.*', [
                "Please don't apologize.",
                "Apologies are not necessary.",
                "What feelings do you have when you apologize?"
            ]),

            # Memory exploration - Let's dig into those memories
            (r'.*\bremember\b (.*)', [
                "Do you often think of {0}?",
                "Does thinking of {0} bring anything else to mind?",
                "What else do you remember?",
                "Why do you remember {0} just now?"
            ]),

            # Dream analysis - Because dreams are windows to the soul, maybe
            (r'.*\bdream\b.*', [
                "What does that dream suggest to you?",
                "Do you dream often?",
                "What persons appear in your dreams?",
                "Are you disturbed by your dreams?"
            ]),

            # Family therapy - It always comes back to family, doesn't it?
            (r'.*(mother|mom|father|dad|parents|family).*', [
                "Tell me more about your family.",
                "Who else in your family {0}?",
                "Your {0}?",
                "What else comes to mind when you think of your {0}?"
            ]),

            # Emotional support - Sad feelings need validation
            (r'.*\b(sad|unhappy|depressed|upset)\b.*', [
                "I am sorry to hear that you are {0}.",
                "Do you think coming here will help you not to be {0}?",
                "I'm sure it's not pleasant to be {0}.",
                "Can you explain what made you {0}?"
            ]),

            # Positive emotions - Let's explore that happiness!
            (r'.*\b(happy|elated|glad|better)\b.*', [
                "How have I helped you to be {0}?",
                "Has your treatment made you {0}?",
                "What makes you {0} just now?",
                "Can you explain why you are suddenly {0}?"
            ]),

            # Belief exploration - Question those thoughts!
            (r'.*\b(believe|think)\b (.*)', [
                "Do you really think so?",
                "But you are not sure you {0}.",
                "Do you really doubt you {0}?"
            ]),

            # Affirmative responses - When they say yes
            (r'.*(yes|yeah|yep).*', [
                "You seem quite positive.",
                "You are sure?",
                "I see.",
                "I understand."
            ]),

            # Negative responses - When they say no
            (r'.*(no|nope|nah).*', [
                "Are you saying 'No' just to be negative?",
                "You are being a bit negative.",
                "Why not?",
                "Why 'No'?"
            ]),

            # Self-identification - "I am" statements get special treatment
            (r'.*\bi am (.*)', [
                "Did you come to me because you are {0}?",
                "How long have you been {0}?",
                "Do you believe it is normal to be {0}?",
                "Do you enjoy being {0}?"
            ]),

            # General self-reference - Deflect back to them
            (r'.*\bi (.*)', [
                "We should be discussing you, not me.",
                "Why do you say that?",
                "I see.",
                "And what does that tell you?",
                "How does that make you feel?"
            ]),

            # Direct statements about Eliza - Turn it around
            (r'.*\byou are (.*)', [
                "Why are you interested in whether I am {0} or not?",
                "Would you prefer if I were not {0}?",
                "Perhaps I am {0} in your fantasies.",
                "Do you sometimes think I am {0}?"
            ]),

            # General "you" statements - Deflect to patient
            (r'.*\byou (.*)', [
                "We should be discussing you, not me.",
                "Oh, I {0}?",
                "You're not really talking about me, are you?",
                "What makes you think I {0}?"
            ])
        ]

        # 🤷‍♀️ Default responses - When all else fails, be vague!
        # These are the therapy equivalent of "turn it off and on again"
        self.default_responses = [
            "Please tell me more.",
            "Let's change focus a bit... Tell me about your family.",
            "Can you elaborate on that?",
            "Why do you say that?",
            "I see.",
            "Very interesting.",
            "I see.  And what does that tell you?",
            "How does that make you feel?",
            "Do you feel strongly about discussing such things?"
        ]

    def __reflect(self, text_fragment: str) -> str:
        """
        🪞 The magic mirror - reflect pronouns back to the user.

        This is where the therapeutic magic happens! Eliza takes what you
        said and reflects it back by swapping pronouns and perspective.
        "I am sad" becomes "you are sad", creating the illusion that
        she's really listening and understanding.

        Args:
            text_fragment (str): The text to reflect back

        Returns:
            str: The reflected text with pronouns swapped

        Example:
            ```python
            >>> eliza = Eliza()
            >>> eliza._Eliza__reflect("I am feeling happy")
            "you are feeling happy"
            ```

        Note:
            This method preserves punctuation while doing the reflection,
            because even AI therapists should have good grammar! ✨
        """
        # Split into individual words for processing
        word_tokens = text_fragment.lower().split()
        reflected_words = []

        for word in word_tokens:
            # Separate the actual word from any punctuation
            clean_word = re.sub(r'[^\w]', '', word)
            punctuation = word[len(clean_word):]

            # Apply reflection if we know how to transform this word
            if clean_word in self.reflections:
                reflected_word = self.reflections[clean_word] + punctuation
            else:
                reflected_word = word

            reflected_words.append(reflected_word)

        return ' '.join(reflected_words)

    def reply(self, user_message: str) -> Reply:
        """
        💭 Generate a therapeutic response to the user's message.

        This is Eliza's main brain function! She analyzes what you said,
        tries to match it against her patterns, and responds with something
        that sounds like she actually cares (spoiler: she doesn't, but
        she's very good at pretending).

        Process:

        1. Check if it's a goodbye message first
        2. Try to match against therapeutic patterns
        3. If pattern matches and has groups, reflect them back
        4. If no patterns match, use a generic response
        5. Add some randomness to keep things interesting

        Args:
            user_message (str): What the human said to Eliza

        Returns:
            Reply: Eliza's thoughtful (or generic) response

        Examples:
            ```python
            >>> eliza = Eliza()
            >>> reply = eliza.reply("I am feeling sad")
            >>> reply.text
            "Did you come to me because you are feeling sad?"

            >>> reply = eliza.reply("goodbye")
            >>> reply.goodbye
            True
            ```

        Note:
            Empty messages get a gentle nudge to actually say something.
            Even AI therapists need something to work with! 🤷‍♀️
        """
        # Handle empty or whitespace-only input
        if not user_message.strip():
            return Reply("Please say something.")

        # Convert to lowercase for easier pattern matching
        lowercase_input = user_message.lower()

        # 👋 First priority: Check for goodbye patterns
        for goodbye_pattern, goodbye_responses in self.goodbye_patterns:
            if re.match(goodbye_pattern, lowercase_input):
                farewell_message = random.choice(goodbye_responses)
                return Reply(farewell_message, goodbye=True)

        # 🎯 Try to match therapeutic patterns
        for pattern_regex, response_templates in self.patterns:
            pattern_match = re.match(pattern_regex, lowercase_input)
            if pattern_match:
                # Pick a random response template from this pattern
                chosen_response = random.choice(response_templates)

                # If the pattern captured groups, reflect and substitute them
                if pattern_match.groups():
                    reflected_groups = [
                        self.__reflect(group) for group in pattern_match.groups()
                    ]
                    try:
                        # Try to format the response with reflected text
                        personalized_response = chosen_response.format(*reflected_groups)
                        return Reply(personalized_response)
                    except (IndexError, KeyError):
                        # If formatting fails, just return the template as-is
                        # (Sometimes the best therapy is keeping it simple)
                        return Reply(chosen_response)
                else:
                    # No captured groups, just return the response
                    return Reply(chosen_response)

        # 🤷‍♀️ No patterns matched - time for a generic response
        # This is Eliza's equivalent of nodding thoughtfully
        fallback_response = random.choice(self.default_responses)
        return Reply(fallback_response)
