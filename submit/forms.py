import os
from django import forms
from django.utils.translation import ugettext_lazy as _

from . import constants
from . import settings as submit_settings
from .submit_helpers import add_language_preference_to_filename


class BaseSubmitForm(forms.Form):
    """
    Base form with one file field checking if some file was submitted and common parameters of file.
    """
    submit_file = forms.FileField(
        max_length=submit_settings.SUBMIT_UPLOADED_FILENAME_MAXLENGTH,
        allow_empty_file=True,
    )

    def clean_submit_file(self):
        sfile = self.cleaned_data.get('submit_file', None)
        if sfile:
            return sfile
        else:
            raise forms.ValidationError(_('No file was submitted'), code='no file')


class FileSubmitForm(BaseSubmitForm):
    """
    Constructor expects a keyword argument `extensions` -- list of extensions in format [".txt", ".pdf"]
    or None/[] meaning that any extension is accepted.

    Checks, whether the submitted file has correct extension.
    """
    def __init__(self, *args, **kwargs):
        self.extensions = kwargs.pop('extensions')
        super(BaseSubmitForm, self).__init__(*args, **kwargs)

    def clean_submit_file(self):
        sfile = super(FileSubmitForm, self).clean_submit_file()
        extension = os.path.splitext(sfile.name)[1].lower()
        if self.extensions is not None and len(self.extensions) > 0 and extension not in self.extensions:
            raise forms.ValidationError(_('Invalid file extension %(extension)s'),
                                        code='invalid extension',
                                        params={'extension': extension})
        return sfile


class CodeSubmitForm(BaseSubmitForm):
    """
    Constructor expects a keyword argument `languages` -- list of option pairs (extension, verbose description)
    [(".c", "C (.c)"), (".py", "Python 3.4 (.py/.py3)")]. A default option (recognize automatically) is added.

    Checks whether the ext. is allowed, maps extension to judge-supported-ext. and renames file with this new ext.
    """
    def __init__(self, *args, **kwargs):
        self.languages = kwargs.pop('languages')
        super(CodeSubmitForm, self).__init__(*args, **kwargs)

        automatic = [
            [constants.DEDUCE_LANGUAGE_AUTOMATICALLY_OPTION, constants.DEDUCE_LANGUAGE_AUTOMATICALLY_VERBOSE],
        ]
        self.fields['language'] = forms.ChoiceField(label=_('Language'),
                                                    choices=automatic + self.languages,
                                                    required=True)

    def clean(self):
        cleaned_data = super(CodeSubmitForm, self).clean()
        if 'submit_file' in cleaned_data and 'language' in cleaned_data:
            filename = cleaned_data['submit_file'].name
            language = cleaned_data['language']
            allowed_languages = [choice[0] for choice in self.languages]
            try:
                cleaned_data['submit_file'].name = add_language_preference_to_filename(filename, language,
                                                                                            allowed_languages)
            except Exception:
                raise forms.ValidationError(_('Automatic language discovery failed. Unknown language extension.'),
                                            code='invalid language')
        return cleaned_data


def submit_form_factory(*args, **kwargs):
    configuration = kwargs.pop('configuration', dict())
    languages = configuration.get('languages', None)
    extensions = configuration.get('extensions', None)

    if languages is not None:
        return CodeSubmitForm(*args,  **dict(kwargs, languages=languages))

    return FileSubmitForm(*args, **dict(kwargs, extensions=extensions))
