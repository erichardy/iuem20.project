# -*- coding: utf-8 -*-

from data import lorem
from data import projects
from os.path import abspath
from os.path import dirname
from os.path import join
from plone import api
from plone.namedfile import NamedBlobImage
from z3c.relationfield.relation import RelationValue
# from plone.i18n.normalizer.interfaces import INormalizer
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.publisher.browser import BrowserView

import logging


PREFIX = abspath(dirname(__file__))
logger = logging.getLogger('iuem20.project: CREATEDATASET')


def input_image_path(f):
    return join(PREFIX, '../tests/images/', f)


class createDataSet(BrowserView):

    def __call__(self):
        portal = api.portal.get()
        self.deleteProject()
        self.createProject()
        url = portal.absolute_url() + '/folder_contents'
        self.request.response.redirect(url)

    def getPortraits(self):
        portal = api.portal.get()
        intids = getUtility(IIntIds)
        founds = api.content.find(context=portal,
                                  portal_type='iuem20.portrait',
                                  path='/'.join(portal.getPhysicalPath())
                                  )
        p_ids = []
        for found in founds:
            p_ids.append(intids.getId(found.getObject()))
        return p_ids

    def deleteProject(self):
        portal = api.portal.get()
        try:
            api.content.delete(obj=portal['mon-projet'])
        except Exception:
            pass

    def createProject(self):
        portal = api.portal.get()
        project = projects[0]
        obj = api.content.create(type='iuem20.project',
                                 title=project['title'],
                                 description=project['description'],
                                 categories=set(project['categories']),
                                 start_date=project['start_date'],
                                 end_date=project['end_date'],
                                 presentation=project['presentation'],
                                 display_one=project['display_one'],
                                 presentation_one=project[
                                     'presentation_one'],
                                 display_two=project['display_two'],
                                 presentation_two=project[
                                     'presentation_two'],
                                 image=NamedBlobImage(),
                                 img_author=project['img_author'],
                                 thumbnail=NamedBlobImage(),
                                 container=portal)
        # image
        path_main = input_image_path(project['image'])
        fd = open(path_main, 'r')
        obj.image.data = fd.read()
        fd.close()
        obj.image.filename = project['image']
        # Thumbnail
        path_main = input_image_path(project['thumbnail'])
        fd = open(path_main, 'r')
        obj.thumbnail.data = fd.read()
        fd.close()
        obj.thumbnail.filename = project['thumbnail']
        obj.reindexObject()
        allPortraits = self.getPortraits()
        obj.primary_contact = RelationValue(allPortraits[0])
        obj.second_contact = RelationValue(allPortraits[1])
        obj.third_contact = RelationValue(allPortraits[2])
        obj.reindexObject()
        logger.info(obj.title + ' Created')
        self.createCarousel(obj)
        # self.createMissions(obj)

    def _loadImage(self, objField, image):
        imgPath = image.split('/')
        if len(imgPath) > 1:
            title = imgPath[len(imgPath) - 1]
        else:
            title = image
        path = input_image_path(image)
        fd = open(path, 'r')
        objField.data = fd.read()
        fd.close()
        objField.filename = title

    def _loadImagesInFolder(self, folderish, images):
        for img in images:
            imgPath = img.split('/')
            if len(imgPath) > 1:
                title = imgPath[len(imgPath) - 1]
            else:
                title = img
            image = api.content.create(type='Image',
                                       title=title,
                                       image=NamedBlobImage(),
                                       description=lorem,
                                       container=folderish)
            self._loadImage(image.image, img)
            image.reindexObject()
            api.content.transition(obj=image, transition='publish')
            image.reindexObject()

    def createCarousel(self, loc):
        carousel = api.content.create(type='Folder',
                                      title=u'carousel',
                                      container=loc)
        api.content.transition(obj=carousel, transition='publish')
        imgs = [u'1800-IMGA0536.JPG', u'1800-IMGA0537.JPG',
                u'1800-IMGA0538.JPG', u'1800-IMGA0671.JPG',
                u'1800-IMGA0971.JPG']
        self._loadImagesInFolder(carousel, imgs)
        logger.info(carousel.title + ' Created')
