from django.db import models


class BaseMetadata(models.Model):
    """Base class for metadata on all objects"""

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Story(BaseMetadata):
    """The story behind a grudge."""

    title = models.CharField(max_length=2000)
    origin = models.TextField(help_text="The origin story of this grudge. Be specific.")

    class Meta:
        verbose_name_plural = "Stories"

    def __str__(self) -> str:
        return f"{self.title}"


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

    class GrudgePotency(models.IntegerChoices):
        """
        Is this incident enough on its own to make you hold a grudge?
        """

        YES = 1, "a) yes"
        NO = 0, "no, only with other incidents taken into account too"

    class GrudgeeRisk(models.IntegerChoices):
        """Would something bad or frightening have happened to the
        grudgee if they hadn't performed the grudge-sparking action?
        """

        NO = 0, "a) no"
        YES = -1, "b) yes"

    class EasilyForgiven(models.IntegerChoices):
        """Could you forgive the grudge with a proper apology?"""

        NO = 0, "a) no"
        YES = -1, "b) yes"

    class GrudgeeSignificance(models.IntegerChoices):
        """
        Does the grudgee matter to you? Do you matter to them?
        """

        MASSIVELY = 4, "a) yes, massively"
        QUITE_A_LOT = 2, "b) yes, quite a lot"
        NOT_ESPECIALLY = 0, "c) not especially—only as a fellow human being"

    # Model attributes

    origin_story = models.OneToOneField(Story, on_delete=models.CASCADE, related_name="grudge")
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

    grudgee_risk = models.IntegerField(
        choices=GrudgeeRisk.choices,
        help_text=(
            "Would something bad or frightening have happened to your "
            "grudgee if they hadn't performed the grudge-sparking action?"
        ),
    )

    grudge_easily_forgiven = models.IntegerField(
        choices=EasilyForgiven.choices,
        help_text=(
            "Would this grudge be canceled out/terminated if your "
            "grudgee apologized fully and wholeheartedly?"
        ),
    )

    grudgee_significance = models.IntegerField(
        choices=GrudgeeSignificance.choices,
        help_text=("Is your grudgee someone who matters to you, and to whom you matter?"),
    )

    @property
    def carat(self):
        """Like diamonds, grudges can be on the lighter or weightier side.
        The additive and subtractive attributes of each grudge determine
        its carat value.
        """
        return sum(
            getattr(self, field.name)
            for field in self._meta.get_fields()
            if isinstance(field, models.IntegerField)
        )

    def __str__(self):
        """
        The string representation of the Grudge. If there's a story, use that
        title, otherwise use the Grudge ID.
        """
        if self.origin_story:
            return f"Grudge for {self.origin_story.title}"
        return f"Grudge {self.id}"
