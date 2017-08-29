# -*- coding: utf-8 -*-
"""
Nous auront besoin des references :
http://docs.plone.org/external/plone.app.dexterity/docs/advanced/references.html
pour associer un projet a des missions et des portraits.
"""

from iuem20.project import _
from iuem20.project.interfaces import IProject
from plone import api
# from plone.dexterity.browser import edit
from plone.dexterity.browser import add
from plone.dexterity.content import Container
from plonetheme.iuem20.utils import getGalleryImages as ggi
# import urllib
# import re
from plonetheme.iuem20.utils import getTitleFromVoc
# from Products.CMFPlone.utils import safe_unicode
from z3c.form import button
from zope.interface import implementer
from zope.publisher.browser import BrowserView

import logging


logger = logging.getLogger('iuem20 PROJECT')
CheckBoxFieldWidget = 'z3c.form.browser.checkbox.CheckBoxFieldWidget'


class AddForm(add.DefaultAddForm):
    portal_type = 'iuem20.project'
    ignoreContext = True
    label = _(u'Add a new project !')

    def update(self):
        super(add.DefaultAddForm, self).update()

    def updateWidgets(self):
        super(add.DefaultAddForm, self).updateWidgets()

    @button.buttonAndHandler(_(u'Save this project'), name='save_this_project')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _('Please correct errors')
            return
        try:
            obj = self.createAndAdd(data)
            logger.info(obj.absolute_url())
            contextURL = self.context.absolute_url()
            self.request.response.redirect(contextURL)
        except Exception:
            raise

    @button.buttonAndHandler(_(u'Cancel this project'))
    def handleCancel(self, action):
        data, errors = self.extractData()
        # context is the thesis repo
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)


class AddView(add.DefaultAddView):
    form = AddForm


"""
class editForm(edit.DefaultEditForm):
    pass
"""


class ProjectView(BrowserView):

    def getGalleryImages(self):
        return ggi(self.context)


@implementer(IProject)
class project(Container):

    def getImgAuthor(self):
        if not self.img_author:
            return False
        return self.img_author

    def getPrimaryContact(self):
        return self.primary_contact.to_object

    def getSecondContact(self):
        try:
            return self.second_contact.to_object
        except Exception:
            return False

    def getThirdContact(self):
        try:
            return self.third_contact.to_object
        except Exception:
            return False

    def getMissions(self):
        bmissions = api.content.find(portal_type='iuem20.mission',
                                     path='/'.join(self.getPhysicalPath()),
                                     depth=1,
                                     )
        missions = [mission.getObject() for mission in bmissions]
        if len(missions) == 0:
            return False
        return [mission.getObject() for mission in bmissions]

    def sort_by_title(self, a, b):
        a_name = a.family_name + ' ' + a.first_name
        b_name = b.family_name + ' ' + b.first_name
        if a_name < b_name:
            return -1
        return 1

    def getMissionsTeams(self):
        """
        :returns: la liste de tous les participants à toutes les missions,
          par ordre alpabétique et épurée des doublons
          A cette liste est ajoutée la liste des portraits ajoutés dans
          le champ other du projet
        """
        missions = self.getMissions()
        if not missions:
            return False
        p = []
        for mission in missions:
            p += mission.getChiefs()
            team = mission.getTeam()
            if team:
                p += team
        other = []
        if self.other:
            other = [o.to_object for o in self.other]
        participants = []
        for participant in p:
            if participant not in participants:
                participants.append(participant)
        if len(other) > 0:
            for o in other:
                if o not in participants:
                    participants.append(o)
        return sorted(participants, self.sort_by_title)

    def getPresentation(self):
        """
        :return: Le texte en format ``raw`` s'il existe.
           Sinon ``False``
        """
        try:
            if len(self.presentation.raw) < 6:
                # logger.info('inf a 6')
                return False
            else:
                return self.presentation.raw
        except Exception:
            # logger.info('excepppppp')
            return False

    def getProjectCategories(self):
        voc = 'iuem20.projectcategories'
        c = self
        clist = [getTitleFromVoc(voc, category) for category in c.categories]
        cat = [ctg + '<br />' for ctg in clist
               if ctg != clist[-1]]
        cat.append(clist[-1])
        return ''.join(cat)

    def _toHTML(self, ch):
        s = ch.replace('\'', '&rsquo;').\
            replace('\'', '&rdquo;')
        return s
