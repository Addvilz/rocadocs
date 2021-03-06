import gfm
import markdown
from markdown.extensions import Extension
from markdown.extensions.admonition import AdmonitionExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.smart_strong import SmartEmphasisExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension
from markdown.inlinepatterns import LINK_RE
from slugify import slugify

from .const import VALID_EXTENSIONS


class RocaExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        # Nl2BrExtension().extendMarkdown(md, md_globals)
        FencedCodeExtension().extendMarkdown(md, md_globals)
        SmartEmphasisExtension().extendMarkdown(md, md_globals)
        TableExtension().extendMarkdown(md, md_globals)
        AdmonitionExtension().extendMarkdown(md, md_globals)

        CodeHiliteExtension(
            use_pygments=True,
            css_class='roca_css'
        ).extendMarkdown(md, md_globals)

        TocExtension(
            anchorlink=False,
            permalink=True
        ).extendMarkdown(md, md_globals)

        gfm.AutomailExtension().extendMarkdown(md, md_globals)
        gfm.SemiSaneListExtension().extendMarkdown(md, md_globals)
        gfm.SpacedLinkExtension().extendMarkdown(md, md_globals)
        gfm.StrikethroughExtension().extendMarkdown(md, md_globals)
        gfm.AutolinkExtension().extendMarkdown(md, md_globals)
        gfm.TaskListExtension().extendMarkdown(md, md_globals)

        SubstituteExtension().extendMarkdown(md, md_globals)


def ends_with_valid_extension(path):
    for ext in VALID_EXTENSIONS:
        if path.endswith(ext):
            return True
    return False


def remove_extension(path):
    for ext in VALID_EXTENSIONS:
        if path.endswith(ext):
            return path[:-(len(ext))]
    return path


class SubstituteExtensionPattern(markdown.inlinepatterns.LinkPattern):
    def handleMatch(self, m):
        el = super(SubstituteExtensionPattern, self).handleMatch(m)
        href = el.get('href')
        if '://' in href or href.startswith('//'):
            return
        if ends_with_valid_extension(href):
            el.set('href', 'javascript:article(\'' + slugify(remove_extension(href)) + '\');')
        return el


class SubstituteExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        pattern = SubstituteExtensionPattern(
            LINK_RE,
            md
        )
        md.inlinePatterns['link'] = pattern
