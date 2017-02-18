from django.utils.translation import ugettext_lazy as _

# Extensions used to store submit and review files
SUBMITTED_FILE_EXTENSION = '.submit'
REVIEWED_FILE_EXTENSION = '.review'
TESTING_PROTOCOL_EXTENSION = '.protocol'
TESTING_RAW_EXTENSION = '.raw'

# DB can hold names with length up to 128, some space is reserved for extension mapping
SUBMIT_UPLOADED_FILENAME_MAXLENGTH = 120


class JudgeTestResult(object):
    """
    Groups all common values of test results in protocol.
    Stores verbose versions of results.
    """
    OK = 'OK'
    WRONG_ANSWER = 'WA'
    TIME_LIMIT_EXCEEDED = 'TLE'
    RUNTIME_EXCEPTION = 'EXC'
    SECURITY_EXCEPTION = 'SEC'
    IGNORED = 'IGN'
    COMPILATION_ERROR = 'CERR'

    VERBOSE_RESULT = {
        OK: _('OK'),
        WRONG_ANSWER: _('Wrong answer'),
        TIME_LIMIT_EXCEEDED: _('Time limit exceeded'),
        RUNTIME_EXCEPTION: _('Runtime exception'),
        SECURITY_EXCEPTION: _('Security exception'),
        IGNORED: _('Ignored'),
        COMPILATION_ERROR: _('Compilation error'),
    }

    @classmethod
    def verbose(cls, result):
        return cls.VERBOSE_RESULT.get(result, result)


class ReviewResponse(JudgeTestResult):
    """
    Groups all common values of Review.short_response.
    Stores verbose versions of responses.
    """

    SENDING_TO_JUDGE = 'Sending to judge'
    SENT_TO_JUDGE = 'Sent to judge'
    JUDGE_UNAVAILABLE = 'Judge unavailable'
    PROTOCOL_CORRUPTED = 'Protocol corrupted'
    REVIEWED = 'Reviewed'

    VERBOSE_RESPONSE = {
        # strings are as literals here so `manage.py makemessages` will include them into django.po file
        SENDING_TO_JUDGE: _('Sending to judge'),
        SENT_TO_JUDGE: _('Sent to judge'),
        JUDGE_UNAVAILABLE: _('Judge unavailable'),
        PROTOCOL_CORRUPTED: _('Protocol corrupted'),
        REVIEWED: _('Reviewed'),
    }

    @classmethod
    def verbose(cls, response):
        if response in cls.VERBOSE_RESPONSE:
            return cls.VERBOSE_RESPONSE[response]
        return cls.VERBOSE_RESULT.get(response, response)

    @classmethod
    def all_items_as_choices(cls):
        judge_responses = list(cls.VERBOSE_RESULT.items())
        communication = [(k, v) for k, v in cls.VERBOSE_RESPONSE.items() if k != ReviewResponse.REVIEWED]
        manual = ((ReviewResponse.REVIEWED, cls.verbose(ReviewResponse.REVIEWED)), )

        choices = (
            (_('Manual review'), manual),
            (_('Judge test results'), judge_responses),
            (_('Judge communication'), communication),
        )

        return choices

DEDUCE_LANGUAGE_AUTOMATICALLY_OPTION = '.'
DEDUCE_LANGUAGE_AUTOMATICALLY_VERBOSE = _('Deduce from extension')

# Definitions of programming languages supported by judge in a following format:
# language_identifier: (language_name, extension_expected_by_judge, list_of_extensions)
LANGUAGE_DEFINITIONS = {
    'cc':   ('C++',         '.cc',      ('.cc', '.cpp')),
    'pas':  ('Pascal',      '.pas',     ('.pas', '.dpr')),
    'c':    ('C',           '.c',       ('.c',)),
    'py':   ('Python 3.4',  '.py',      ('.py', '.py3')),
    'hs':   ('Haskell',     '.hs',      ('.hs', )),
    'cs':   ('C#',          '.cs',      ('.cs', )),
    'java': ('Java',        '.java',    ('.java', )),
}

LANGUAGE_IDENTIFIERS = list()
LANGUAGE_EXTENSIONS = list()
LANGUAGE_EXTENSION_MAPPING = dict()
LANGUAGE_CHOICE_TEXTS = dict()

for identifier, (name, judge_extension, extensions) in LANGUAGE_DEFINITIONS.items():
    LANGUAGE_IDENTIFIERS.append(identifier)
    LANGUAGE_EXTENSIONS.extend(extensions)
    LANGUAGE_EXTENSION_MAPPING.update({extension: judge_extension for extension in extensions})
    LANGUAGE_CHOICE_TEXTS[identifier] = '{} ({})'.format(name, '/'.join(extensions))
