from django.test import TestCase
from .models import Grudge, Story

class GrudgeModelTest(TestCase):

    """Tests for Grudge model."""

    def setUp(self):
        """Create a new Story."""
        self.story = Story.objects.create(
            title="Test Grudge Story",
            origin="This is a test origin story for the grudge."
        )

    def test_grudge_carat_max_values(self):
        """Test Grudge with maximum value for the carat property."""
        grudge = Grudge.objects.create(
            origin_story=self.story,
            grudgee_intention=Grudge.Intention.DEFINITELY_BAD,
            grudgee_knowledge=Grudge.Knowledge.DEFINITELY,
            seriousness_of_situation=Grudge.Seriousness.VERY_SERIOUS,
            grudge_effect=Grudge.StrengthOfEffect.VERY_BAD,
            grudgee_skill=Grudge.GrudgeeSkill.YES,
            harm_level=Grudge.HarmScale.YES,
            grr_factor=Grudge.GRRFactor.HIGH,
            grudge_length=Grudge.GrudgeLength.VERY_LONG,
            grudgee_risk=Grudge.GrudgeeRisk.NO,
            grudge_easily_forgiven=Grudge.EasilyForgiven.NO,
            grudgee_significance=Grudge.GrudgeeSignificance.MASSIVELY
        )
        expected_carat = (
            3 +  # grudgee_intention
            3 +  # grudgee_knowledge
            3 +  # seriousness_of_situation
            3 +  # grudge_effect
            3 +  # grudgee_skill
            3 +  # harm_level
            3 +  # grr_factor
            3 +  # grudge_length
            0 +  # grudgee_risk
            0 +  # grudge_easily_forgiven
            4    # grudgee_significance
        )
        self.assertEqual(grudge.carat, expected_carat)

    def test_grudge_carat_medium_values(self):
        """Test Grudge with middle-of-the-road carat value."""
        grudge = Grudge.objects.create(
            origin_story=self.story,
            grudgee_intention=Grudge.Intention.POSSIBLY_BAD,
            grudgee_knowledge=Grudge.Knowledge.POSSIBLY,
            seriousness_of_situation=Grudge.Seriousness.SOMEWHAT_SERIOUS,
            grudge_effect=Grudge.StrengthOfEffect.QUITE_BAD,
            grudgee_skill=Grudge.GrudgeeSkill.MAYBE,
            harm_level=Grudge.HarmScale.MAYBE,
            grr_factor=Grudge.GRRFactor.MEDIUM,
            grudge_length=Grudge.GrudgeLength.MEDIUM,
            grudgee_risk=Grudge.GrudgeeRisk.YES,
            grudge_easily_forgiven=Grudge.EasilyForgiven.YES,
            grudgee_significance=Grudge.GrudgeeSignificance.QUITE_A_LOT
        )
        expected_carat = (
            2 +  # grudgee_intention
            2 +  # grudgee_knowledge
            2 +  # seriousness_of_situation
            2 +  # grudge_effect
            2 +  # grudgee_skill
            2 +  # harm_level
            2 +  # grr_factor
            2 +  # grudge_length
            -1 + # grudgee_risk
            -1 + # grudge_easily_forgiven
            2    # grudgee_significance
        )
        self.assertEqual(grudge.carat, expected_carat)

    def test_grudge_carat_new_grudge(self):
        """Test that new Grudge with missing values has a None-value carat."""
        grudge = Grudge()
        self.assertIsNone(grudge.carat)

