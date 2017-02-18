import os

from django import forms
from django.utils.translation import ugettext_lazy as _

from submit import constants
from submit.submit_helpers import add_language_preference_to_filename


class BaseSubmitForm(forms.Form):
    """
    Base form with one file field checking if some file was submitted and common parameters of file.
    """
    submit_file = forms.FileField(
        max_length=constants.SUBMIT_UPLOADED_FILENAME_MAXLENGTH,
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
    Constructor expects a keyword argument `languages` -- list of language identifiers in format ["cc", "py"].

    Checks whether the programming language of submitted file is allowed,
    maps extension to judge-supported-extension
    and modifies the name of submitted file with this new extension.
    """
    def __init__(self, *args, **kwargs):
        self.languages = kwargs.pop('languages')
        super(CodeSubmitForm, self).__init__(*args, **kwargs)

        choices = [(constants.DEDUCE_LANGUAGE_AUTOMATICALLY_OPTION, constants.DEDUCE_LANGUAGE_AUTOMATICALLY_VERBOSE)]
        choices.extend([(lang, constants.LANGUAGE_CHOICE_TEXTS[lang]) for lang in self.languages])
        self.fields['language'] = forms.ChoiceField(label=_('Language'),
                                                    choices=choices,
                                                    required=True)

    def clean(self):
        cleaned_data = super(CodeSubmitForm, self).clean()
        if 'submit_file' in cleaned_data and 'language' in cleaned_data:
            filename = cleaned_data['submit_file'].name
            language = cleaned_data['language']
            try:
                cleaned_data['submit_file'].name = add_language_preference_to_filename(filename, language,
                                                                                       self.languages)
            except Exception:
                raise forms.ValidationError(_('Automatic language discovery failed. Unknown language extension.'),
                                            code='invalid language')
        return cleaned_data


def submit_form_factory(*args, **kwargs):
    receiver = kwargs.pop('receiver')

    languages = receiver.get_languages()
    if languages:
        return CodeSubmitForm(*args,  **dict(kwargs, languages=languages))

    extensions = receiver.get_extensions()
    return FileSubmitForm(*args, **dict(kwargs, extensions=extensions))
