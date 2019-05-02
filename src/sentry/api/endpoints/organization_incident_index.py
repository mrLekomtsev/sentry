from __future__ import absolute_import

from sentry import features
from sentry.api.bases.incident import IncidentPermission
from sentry.api.bases.organization import OrganizationEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.api.paginator import OffsetPaginator
from sentry.api.serializers import serialize
from sentry.incidents.models import Incident


class OrganizationIncidentIndexEndpoint(OrganizationEndpoint):
    permission_classes = (IncidentPermission, )

    def get(self, request, organization):
        """
        List Incidents that a User can access within an Organization
        ````````````````````````````````````````````````````````````
        Returns a paginated list of Incidents that a user can access.

        :auth: required
        """
        if not features.has('organizations:incidents', organization, actor=request.user):
            raise ResourceDoesNotExist

        incidents = Incident.objects.fetch_for_organization(
            organization,
            self.get_projects(request, organization),
        )

        return self.paginate(
            request,
            queryset=incidents,
            order_by='date_started',
            paginator_cls=OffsetPaginator,
            on_results=lambda x: serialize(x, request.user),
        )
