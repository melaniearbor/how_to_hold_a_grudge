from random import choice, choices
from django.db import models


class BaseMetadata(models.Model):
    """Base class for metadata on all objects"""

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class Story(BaseMetadata):
    """The story behind a grudge."""

    origin_story = models.TextField(help_text="The origin story of this grudge. Be specific.")


class Grudge(BaseMetadata):
    """Model for a grudge."""

    # Choice definitions

    class Intention(models.IntegerChoices):
        """Class representing the intention of the grudgee. Bad intentions create
        higher-carat grudges."""

        DEFINITELY_BAD = 3, "a) definitely or probably bad"
        POSSIBLY_BAD = 2, "b) possibly bad"
        NOT_BAD = 1, "c) not bad"

    class Knowledge(models.IntegerChoices):
        """Class representing the foreknowledge of the grudgee.
        Knowledge of harm creates higher-carat grudges."""

        DEFINITELY = 3, "a) yes, definitely"
        POSSIBLY = 2, "b) possibly"
        NO = 1, "c) not at all"

    class Seriousness(models.IntegerChoices):
        """Class representing the seriousness of the situation.
        More serious situations resutl in higher-carat grudges."""

        VERY_SERIOUS = 3, "a) very serious"
        SOMEWHAT_SERIOUS = 2, "b) somewhat serious"
        NOT_SERIOUS = 1, "c) not very serious"

    class StrengthOfEffect(models.IntegerChoices):
        """
        The impact of the offense. The worse the impact, the
        higher the carat of the grudge."""

        VERY_BAD = 3, "a) very bad"
        QUITE_BAD = 2, "b) quite bad"
        NOT_SO_BAD = 1, "c) not so bad"

    class GrudgeeSkill(models.IntegerChoices):
        """
        The social/emotional skill of the grudgee. If they
        could or should have known better, the grudge will
        have a higher-carat rating.
        """

        YES = 3, "a) yes"
        MAYBE = 2, "b) maybe"
        NO = 1, "c) no"

    class HarmScale(models.IntegerChoices):
        """
        The degree to which you were caused actual harm.
        The greater the harm, the higher the carat rating
        of the harm.
        """

        YES = 3, "a) yes"
        MAYBE = 2, "b) maybe"
        NO = 1, "c) no"

    class GRRFactor(models.IntegerChoices):
        """
        How bothered you are/were by this grudge.
        """

        HIGH = 3, "a) high"
        MEDIUM = 2, "b) medium"
        LOW = 1, "c) low"

    class GrudgeLength(models.IntegerChoices):
        """
        How long you have held the druge, or how long
        you anticipate it will impact you.
        """

        VERY_LONG = 3, "a) for ages; or, for not very long but you know it'll last forever."
        MEDIUM = (
            2,
            "b) for a mediuim length of time; or for a short time and you think you'll hold it for a bit longer but not forever",
        )
        SHORT = (
            1,
            "c) for a short time, and you'll probably have given up this grudge by next week",
        )

    # Model attributes

    title = models.CharField(max_length=2000)
    grudgee_intention = models.IntegerField(
        choices=Intention.choices,
        help_text="How bad was the intention of the grudgee?",
    )
    grudgee_knowledge = models.IntegerField(
        choices=Knowledge.choices,
        help_text="Did they know they were upsetting, hurting, or being unfair to you?",
    )
    seriousness_of_situation = models.IntegerField(
        choices=Seriousness.choices, help_text="How serioius was the situation overall?"
    )
    grudge_effect = models.IntegerField(
        choices=StrengthOfEffect.choices, help_text="Did they cause you real harm?"
    )
    grudgee_skill = models.IntegerField(
        choices=GrudgeeSkill.choices, help_text="Should or could they have known/done better?"
    )
    harm_level = models.IntegerField(
        choices=HarmScale.choices, help_text="Did they cause you real harm?"
    )
    grr_factor = models.IntegerField(
        choices=GRRFactor.choices,
        help_text=(
            "Is the `Grrrr!` factor (the extent to which you still strongly feel, "
            "Wow, that was so out of order! when you think abou the incident now) of "
            "this grudge:"
        ),
    )
    grudge_length = models.IntegerField(
        choices=GrudgeLength.choices, help_text="Have you held this grudge:"
    )

    @property
    def additive_attributes(self):
        """
        These attribute's values are additive. Their values increase the
        overall carat value of the Grudge.
        """
        return [
            self.grudgee_intention,
            self.grudgee_knowledge,
            self.seriousness_of_situation,
            self.grudge_effect,
            self.grudgee_skill,
            self.harm_level,
            self.grr_factor,
            self.grudge_length,
        ]

    @property
    def subtractive_attributes(self):
        """
        These attribute's values are subtractive. Their values reduce
        the overall carat value of the Grudge"""
        return 0

    @property
    def carat(self):
        """Like diamonds, grudges can be on the lighter or weightier side.
        The additive and subtractive attributes of each grudge determine
        its carat value.
        """
        return 0
