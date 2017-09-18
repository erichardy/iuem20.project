# -*- coding: utf-8 -*-

# from operator import attrgetter
from plone import api
from plonetheme.iuem20.utils import sort_by_position
from zope.publisher.browser import BrowserView

import logging


logger = logging.getLogger('iuem20.projects')


class projectsView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getProjectsObjs(self,
                        effective=False):
        """
        :param effective: tri par date de publication
        :type effective: Boolean
        :return: liste des projets triés par ordre de disposition dans le
          dossier, ou par ordre de date de publication. Dans la vue,
          on affiche par ordre de disposition dans le dossier.
        """
        context = self.context
        founds = api.content.find(context=self.context,
                                  portal_type='iuem20.project',
                                  path='/'.join(context.getPhysicalPath()),
                                  depth=1,
                                  )
        if len(founds) == 0:
            return False
        objs = [found.getObject() for found in founds]
        if effective:
            sortedObjs = sorted(objs,
                                key=lambda obj: obj.effective(),
                                reverse=True)
            return sortedObjs
        return sorted(objs, sort_by_position)
