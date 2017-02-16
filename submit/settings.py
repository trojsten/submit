from django.conf import settings as django_settings

SUBMIT_TASK_MODEL = getattr(django_settings, 'SUBMIT_TASK_MODEL', 'submit.BaseTask')

SUBMIT_PATH = getattr(django_settings, 'SUBMIT_PATH', 'submit/')

# DB can hold names with length up to 128, some space is reserved for extension mapping
SUBMIT_UPLOADED_FILENAME_MAXLENGTH = int(getattr(django_settings, 'SUBMIT_UPLOADED_FILENAME_MAXLENGTH', 120))

# Extensions of uploaded source files will be replaced for compatibility with judge
SUBMIT_EXTENSION_MAPPING_FOR_JUDGE = getattr(django_settings, 'SUBMIT_EXTENSION_MAPPING_FOR_JUDGE',
    {
        '.cpp': '.cc',
        '.cc': '.cc',
        '.pp': '.pas',
        '.pas': '.pas',
        '.dpr': '.pas',
        '.c': '.c',
        '.py': '.py',
        '.py3': '.py',
        '.hs': '.hs',
        '.cs': '.cs',
        '.java': '.java',
        '.zip': '.zip'
    }
)
# SubmitReceiver languages will be checked against this list
SUBMIT_EXTENSIONS_ACCEPTED_BY_JUDGE = list(set(SUBMIT_EXTENSION_MAPPING_FOR_JUDGE.values()))

SUBMIT_EXTENSIONS_VERBOSE_CHOICES = getattr(django_settings, 'SUBMIT_EXTENSIONS_VERBOSE_CHOICES',
    {
        '.cc': 'C++ (.cpp/.cc)',
        '.pas': 'Pascal (.pas/.dpr)',
        '.c': 'C (.c)',
        '.py': 'Python 3.4 (.py/.py3)',
        '.hs': 'Haskell (.hs)',
        '.cs': 'C# (.cs)',
        '.java': 'Java (.java)'

    }
)

SUBMIT_VIEWABLE_EXTENSIONS = getattr(django_settings, 'SUBMIT_VIEWABLE_EXTENSIONS', ('.pdf', '.txt'))

JUDGE_INTERFACE_IDENTITY = getattr(django_settings, 'JUDGE_INTERFACE_IDENTITY', 'TESTOVAC')
JUDGE_ADDRESS = getattr(django_settings, 'JUDGE_ADDRESS', '127.0.0.1')
JUDGE_PORT = getattr(django_settings, 'JUDGE_PORT', 12347)

# Override view methods to set `submit.is_accepted` field or submit success message
SUBMIT_POST_SUBMIT_FORM_VIEW = getattr(django_settings, 'SUBMIT_POST_SUBMIT_FORM_VIEW',
                                       'submit.views.PostSubmitForm')

# Format of displayed score can depend on other models
SUBMIT_PREFETCH_DATA_FOR_SCORE_CALCULATION = getattr(django_settings,
                                                     'SUBMIT_PREFETCH_DATA_FOR_SCORE_CALCULATION',
                                                     'submit.defaults.prefetch_data_for_score_calculation')
SUBMIT_DISPLAY_SCORE = getattr(django_settings, 'SUBMIT_DISPLAY_SCORE',
                               'submit.defaults.display_score')

# Override `SubmitReceiver.__str__()` to be more descriptive than '{}'.format(id)
SUBMIT_DISPLAY_SUBMIT_RECEIVER_NAME = getattr(django_settings, 'SUBMIT_DISPLAY_SUBMIT_RECEIVER_NAME',
                                              'submit.defaults.display_submit_receiver_name')

JUDGE_DEFAULT_INPUTS_FOLDER_FOR_RECEIVER = getattr(django_settings, 'JUDGE_DEFAULT_INPUTS_FOLDER_FOR_RECEIVER',
                                                   'submit.defaults.default_inputs_folder_at_judge')

# Override these functions to set access rights for receivers
SUBMIT_CAN_POST_SUBMIT = getattr(django_settings, 'SUBMIT_CAN_POST_SUBMIT',
                                 'submit.defaults.can_post_submit')
SUBMIT_HAS_ADMIN_PRIVILEGES_FOR_RECEIVER = getattr(django_settings, 'SUBMIT_HAS_ADMIN_PRIVILEGES_FOR_RECEIVER',
                                                   'submit.defaults.has_admin_privileges_for_receiver')

SUBMIT_RECEIVER_TEMPLATES = getattr(django_settings, 'SUBMIT_RECEIVER_TEMPLATES', {
    'Source': {
        'has_form': True,
        'caption': 'Source',
        'extensions': '',
        'languages': 'cc, pas, c, py, hs, cs, java',
        'external_link': '',
        'send_to_judge': True,
        'inputs_folder_at_judge': '',
        'show_all_details': False,
        'show_submitted_file': True,
    },
    'Testable ZIP': {
        'has_form': True,
        'caption': 'Testable ZIP',
        'extensions': '',
        'languages': 'zip',
        'external_link': '',
        'send_to_judge': True,
        'inputs_folder_at_judge': '',
        'show_all_details': True,
        'show_submitted_file': False,
    },
    'Description': {
        'has_form': True,
        'caption': 'Description',
        'extensions': '',
        'languages': '',
        'external_link': '',
        'send_to_judge': False,
        'inputs_folder_at_judge': '',
        'show_all_details': False,
        'show_submitted_file': False,
    },
    'Link': {
        'has_form': False,
        'caption': '',
        'extensions': '',
        'languages': '',
        'external_link': '',
        'send_to_judge': False,
        'inputs_folder_at_judge': '',
        'show_all_details': False,
        'show_submitted_file': False,
    },
})
