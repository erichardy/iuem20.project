# -*- coding: utf-8 -*-

from plone import api
from plone.i18n.normalizer.interfaces import INormalizer
from zope.component import getUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import logging


logger = logging.getLogger('iuem20.project')


def make_terms(terms, termsList):
    normalizer = getUtility(INormalizer)
    for term in termsList:
        norm = normalizer.normalize(term)
        terms.append(SimpleTerm(value=norm, token=norm, title=term))
    return terms


def make_voc(terms, linesstr):
    return SimpleVocabulary(make_terms(terms, linesstr))


def make_voc_with_blank(terms, linesstr):
    terms.append(SimpleTerm(None, '', u''))
    # import pdb;pdb.set_trace()
    return SimpleVocabulary(make_terms(terms, linesstr))


@implementer(IVocabularyFactory)
class _projectCategories(object):

    def __call__(self, context):
        prefix = 'iuem20.project.interfaces.'
        prefix += 'IIuem20ProjectSettings.project_categories'
        xjobs = api.portal.get_registry_record(prefix)
        terms = []
        voc = make_voc(terms, xjobs)
        # import pdb;pdb.set_trace()
        return voc


projectCategories = _projectCategories()
