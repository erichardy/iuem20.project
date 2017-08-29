# -*- coding: utf-8 -*-
from iuem20.project.interfaces import Iproject
from iuem20.project.testing import IUEM20_PROJECT_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class projectIntegrationTest(unittest.TestCase):

    layer = IUEM20_PROJECT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='project')
        schema = fti.lookupSchema()
        self.assertEqual(Iproject, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='project')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='project')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(Iproject.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='project',
            id='project',
        )
        self.assertTrue(Iproject.providedBy(obj))
