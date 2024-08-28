from django.views.generic import ListView, DetailView

from grudge_cabinet.models import Grudge


class GrudgeListView(ListView):
    """
    List view for Grudges.
    """

    model = Grudge


class GrudgeDetailView(DetailView):
    """
    Detail view for Grudges.
    """

    model = Grudge

    def get_queryset(self):
        """
        Return a queryset of Grudge objects for the request's user."""
        return Grudge.objects.filter(user=self.request.user)
