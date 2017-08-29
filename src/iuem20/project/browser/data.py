# -*- coding: utf-8 -*-

from plone.app.textfield.value import RichTextValue

import datetime


lorem = """
Vivamus dictum, nunc a tincidunt semper, lectus justo maximus neque,
et pulvinar ipsum dolor at nisl. Maecenas porttitor dolor nec ante cursus
viverra. Maecenas massa nunc, semper vitae pulvinar at, semper
at metus. Cras a fermentum diam. Sed a lobortis
risus, efficitur tincidunt lorem.
"""

bio_fr_text = """
<h4>Savoir-faire opérationnels</h4>
<ul>
<li>Utiliser les méthodes de prévention et
de gestion des risques<br/></li>
</ul>
<h4>Lieu d'exercice</h4>
<ul>
<li>L’activité s’exerce généralement au sein d'un service informatique<br/>
</li>
</ul>
<h3>Dipl&ocirc;me exig&eacute;</h3>
<ul>
<li>Doctorat, diplôme d’ingénieur<br/></li>
</ul>
<h3>Formations et expérience professionnelle souhaitables</h3>
<ul><li>Filière informatique</li></ul>
"""

bio_fr = RichTextValue(bio_fr_text, 'text/plain', 'text/html')
bio_alt1_text = """
<h2>ALT 1 The RichTextValue<a class="headerlink" href="#the-richtextvalue"
title="Permalink to this headline">¶</a></h2>
<p>The <code class="docutils literal"><span class="pre">RichText</span>
</code> field does not store a string. Instead, it stores a
<code class="docutils literal"><span class="pre">RichTextValue</span>
</code> object. This is an immutable object that has the
following properties:</p>
<dl class="docutils">
<dt><code class="docutils literal"><span class="pre">raw</span></code></dt>
<dd>a unicode string with the original input markup;</dd>
<dt><code class="docutils literal"><span class="pre">mimeType</span></code>
</dt>
<dd>the MIME type of the original markup, e.g.
<code class="docutils literal"><span class="pre">text/html</span></code> or
<code class="docutils literal"><span class="pre">text/structured</span>
</code>;</dd>
<dt><code class="docutils literal"><span class="pre">encoding</span></code>
</dt>
<dd>the default character encoding used when transforming the input markup.
Most likely, this will be UTF-8;</dd>
<dt><code class="docutils literal"><span class="pre">raw_encoded</span>
</code></dt>
<dd>the raw input encoded in the given encoding;</dd>
<dt><code class="docutils literal"><span class="pre">outputMimeType</span>
</code></dt>
<dd>the MIME type of the default output, taken from the field at the time of
instantiation;</dd>
<dt><code class="docutils literal"><span class="pre">output</span></code></dt>
<dd>a unicode object representing the transformed output. If possible, this
is cached persistently until the <code class="docutils literal">
<span class="pre">RichTextValue</span></code> is replaced with a
new one (as happens when an edit form is saved, for example).</dd>
</dl>
"""
bio_alt2_text = """
<h2>ALT 2 The RichTextValue<a class="headerlink" href="#the-richtextvalue"
title="Permalink to this headline">¶</a></h2>
<p>The <code class="docutils literal"><span class="pre">RichText</span>
</code> field does not store a string. Instead, it stores a
<code class="docutils literal"><span class="pre">RichTextValue</span>
</code> object. This is an immutable object that has the
following properties:</p>
<dl class="docutils">
<dt><code class="docutils literal"><span class="pre">raw</span></code></dt>
<dd>a unicode string with the original input markup;</dd>
<dt><code class="docutils literal"><span class="pre">mimeType</span></code>
</dt>
<dd>the MIME type of the original markup, e.g.
<code class="docutils literal"><span class="pre">text/html</span></code> or
<code class="docutils literal"><span class="pre">text/structured</span>
</code>;</dd>
<dt><code class="docutils literal"><span class="pre">encoding</span></code>
</dt>
<dd>the default character encoding used when transforming the input markup.
Most likely, this will be UTF-8;</dd>
<dt><code class="docutils literal"><span class="pre">raw_encoded</span>
</code></dt>
<dd>the raw input encoded in the given encoding;</dd>
<dt><code class="docutils literal"><span class="pre">outputMimeType</span>
</code></dt>
<dd>the MIME type of the default output, taken from the field at the time of
instantiation;</dd>
<dt><code class="docutils literal"><span class="pre">output</span></code></dt>
<dd>a unicode object representing the transformed output. If possible, this
is cached persistently until the <code class="docutils literal">
<span class="pre">RichTextValue</span></code> is replaced with a
new one (as happens when an edit form is saved, for example).</dd>
</dl>
"""
bio_alt1 = RichTextValue(bio_alt1_text, 'text/plain', 'text/html')
bio_alt2 = RichTextValue(bio_alt2_text, 'text/plain', 'text/html')


projectA = {}
projectA['title'] = u'Mon projet'
projectA['description'] = u'C\'est là qu\'on voit si ça colle'
projectA['categories'] = ['film-documentaire', 'enseignement']
projectA['start_date'] = datetime.datetime(2016, 4, 12)
projectA['end_date'] = datetime.datetime(2016, 11, 30)
projectA['presentation'] = bio_fr
projectA['image'] = u'1800-IMGA0052.JPG'
projectA['thumbnail'] = u'200-IMGA0052.JPG'
projectA['img_author'] = u'E. Amice'
projectA['doc'] = None
projectA['display_one'] = True
projectA['presentation_one'] = bio_alt1
projectA['display_two'] = True
projectA['presentation_two'] = bio_alt1

projects = []
projects.append(projectA)
