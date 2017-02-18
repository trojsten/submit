import os

from django.http import Http404
from django.utils.module_loading import import_string
from sendfile import sendfile

from submit import constants
from submit import settings as submit_settings
from submit.models import Submit


def add_language_preference_to_filename(filename, language_preference, allowed_languages):
    """
    Change the extension of file to judge-supported-format,
    if a specific language is preferred (chosen by user), use this extension instead.
    """
    name, extension = os.path.splitext(filename)
    extension = extension.lower()

    if language_preference != constants.DEDUCE_LANGUAGE_AUTOMATICALLY_OPTION:
        extension = constants.LANGUAGE_DEFINITIONS[language_preference][1]

    if extension in constants.LANGUAGE_EXTENSIONS:
        extension = constants.LANGUAGE_EXTENSION_MAPPING[extension]
    else:
        raise Exception

    allowed_extensions = [ext for language in allowed_languages
                          for ext in constants.LANGUAGE_DEFINITIONS[language][2]]
    if extension not in allowed_extensions:
        raise Exception

    return ''.join((name, extension))


def write_chunks_to_file(file_path, chunks):
    try:
        os.makedirs(os.path.dirname(file_path))
    except os.error:
        pass

    with open(file_path, 'wb+') as destination:
        for chunk in chunks:
            destination.write(chunk)


def create_submit(user, receiver, sfile=None):
    """
    Use this function to create submits so that is_accepted field is set and submitted file is saved properly.
    """
    submit = Submit(receiver=receiver,
                    user=user,
                    filename='' if sfile is None else sfile.name)
    submit.is_accepted = import_string(submit_settings.SUBMIT_IS_SUBMIT_ACCEPTED)(submit)
    submit.save()
    if sfile is not None:
        write_chunks_to_file(submit.file_path(), sfile.chunks())
    return submit


def send_file(request, filepath, filename):
    """
    Send file requested to be downloaded.
    Display files with extensions in `submit_settings.SUBMIT_VIEWABLE_EXTENSIONS` in browser.
    Returns a response object.
    """
    extension = os.path.splitext(filename)[1]
    as_attachment = extension.lower() not in submit_settings.SUBMIT_VIEWABLE_EXTENSIONS
    if os.path.exists(filepath):
        response = sendfile(
            request,
            filepath,
            attachment=as_attachment,
            attachment_filename=filename,
        )
        response['Content-Disposition'] = 'inline; filename="%s"' % filename
        return response
    else:
        raise Http404
