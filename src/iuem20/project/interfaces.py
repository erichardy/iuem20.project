# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective import dexteritytextindexer
from iuem20.project import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.textfield import RichText
from plone.app.vocabularies.catalog import CatalogSource as CS
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import alsoProvides
from zope.interface import Invalid
from zope.interface import invariant
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import Bool
from zope.schema import Date
from zope.schema import List
from zope.schema import Set
from zope.schema import TextLine


class IIuem20ProjectLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


categoriesList = []
categoriesList.append(u'Recherche scientifique')
categoriesList.append(u'création artistique')
categoriesList.append(u'Enseignement')
categoriesList.append(u'Film documentaire')
categoriesList.append(u'Exposition "grand public"')


class IIuem20ProjectSettings(model.Schema):

    project_categories = List(title=_(u'Project categories'),
                              description=_(u'One category per line'),
                              value_type=TextLine(),
                              default=categoriesList,
                              )


class IIuem20ProjectSettingsForm(RegistryEditForm):
    schema = IIuem20ProjectSettings
    label = _(u'iuem20 project Settings')
    description = _(u'iuem20 project Settings Description')


class IIuem20ProjectSettingsControlPanel(ControlPanelFormWrapper):
    form = IIuem20ProjectSettingsForm


class StartBeforeEnd(Invalid):
    __doc__ = _(u'The start or end date is invalid')


class IProject(model.Schema):

    model.fieldset('general',
                   label=_(u'general'),
                   fields=['title',
                           'description',
                           'categories',
                           'image',
                           'img_author',
                           'thumbnail',
                           ])
    dexteritytextindexer.searchable('title')
    title = TextLine(title=_(u'project label'),
                     required=True,
                     )
    dexteritytextindexer.searchable('description')
    description = TextLine(title=_(u'very short project description'),
                           required=False,
                           )
    dexteritytextindexer.searchable('categories')
    directives.widget(
        categories='z3c.form.browser.checkbox.CheckBoxFieldWidget')
    categories = Set(
        title=_(u'project categories'),
        description=_(u'select one or more'),
        value_type=schema.Choice(
            vocabulary=u'iuem20.projectcategories'),
        required=False
        )
    image = NamedBlobImage(
        title=_(u'main photo'),
        required=True
        )
    img_author = TextLine(title=_(u'picture author'),
                          required=False,
                          )
    thumbnail = NamedBlobImage(
        title=_(u'main photo'),
        required=True
        )
    #
    model.fieldset('descriptions',
                   label=_(u'project descriptions'),
                   fields=['presentation',
                           'start_date',
                           'end_date'])
    dexteritytextindexer.searchable('presentation')
    presentation = RichText(title=_(u'presentation'),
                            required=False,
                            )
    dexteritytextindexer.searchable('start_date')
    start_date = Date(title=_(u'start date for the project'),
                      description=_(u''),
                      required=False,
                      )
    dexteritytextindexer.searchable('end_date')
    end_date = Date(title=_(u'end date for the project'),
                    description=_(u''),
                    required=False,
                    )
    #
    model.fieldset('contacts',
                   label=_(u'contacts'),
                   fields=['p_contact_label',
                           'primary_contact',
                           's_contact_label',
                           'second_contact',
                           't_contact_label',
                           'third_contact',
                           'other_label',
                           'other'
                           ])
    # directives.widget(chief='plone.formwidget.contenttree.ContentTreeFieldWidget')

    p_contact_label = TextLine(
        title=_(u'primary contact label'),
        required=False,
        )
    primary_contact = RelationChoice(
        title=_(u'primary contact'),
        source=CS(portal_type='iuem20.portrait'),
        )
    s_contact_label = TextLine(
        title=_(u'second contact label'),
        required=False,
        )
    second_contact = RelationChoice(
        title=_(u'second contact'),
        source=CS(portal_type='iuem20.portrait'),
        required=False,
        )
    t_contact_label = TextLine(
        title=_(u'third contact label'),
        required=False,
        )
    third_contact = RelationChoice(
        title=_(u'third contact'),
        source=CS(portal_type='iuem20.portrait'),
        required=False,
        )
    other_label = TextLine(
        title=_(u'other participants label'),
        default=u'Teams',
        required=True,
        )
    other = RelationList(title=_(u'other participants'),
                         value_type=RelationChoice(
                             title=_(u'Target'),
                             source=CS(portal_type='iuem20.portrait')),
                         required=False,
                         )
    model.fieldset('missions',
                   label=_(u'associated missions'),
                   fields=[
                       'display_missions',
                       'missions_label',
                       ]
                   )
    display_missions = Bool(
        title=_(u'display related missions'),
        default=True,)
    missions_label = TextLine(
        title=_(u'Missions label'),
        default=u'related missions',
        required=False,
        )

    @invariant
    def validateStartEnd(data):
        if data.start_date is not None and data.end_date is not None:
            if data.start_date > data.end_date:
                msg = u'The start date must be before the end date.'
                raise StartBeforeEnd(_(msg))


alsoProvides(IProject, IFormFieldProvider)
