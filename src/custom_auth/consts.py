from django.utils.translation import ugettext_lazy as _

STUDENTS_GROUP = 'students'
TEACHERS_GROUP = 'teachers'

GROUP_PERMISSIONS = {
    # TODO: написать права для групп
    STUDENTS_GROUP: (
        {'app': 'labs', 'model': 'Task', 'codename': 'view_task', 'name': 'Can view task'},
    ),
    TEACHERS_GROUP: (
        {'app': 'labs', 'model': 'Task', 'codename': 'add_task', 'name': 'Can add task'},
        {'app': 'labs', 'model': 'Task', 'codename': 'change_task', 'name': 'Can change task'},
        {'app': 'labs', 'model': 'Task', 'codename': 'delete_task', 'name': 'Can delete task'},
        {'app': 'labs', 'model': 'Task', 'codename': 'view_task', 'name': 'Can view task'},
    )
}

FACULTIES = enumerate((
    _('Faculty of Computer-Aided Design'),
    _('Faculty of Information Technologies and Control'),
    _('Faculty of Radioengineering and Electronics'),
    _('Faculty of Computer Systems and Networks'),
    _('Faculty of Infocommunications'),
    _('Faculty of Engineering and Economics'),
    _('Military Faculty'),
    _('Faculty of Innovative Lifelong Learning'),
    _('Faculty of Pre-University Preparation and Occupational Guidance'),
))

CHAIRS = enumerate((
    _('Engineering Graphics'),
    _('Foreign Languages No. 1'),
    _('Human Engineering and Ergonomics'),
    _('Electronic Technology and Engineering'),
    _('Information and Computer-Aided Systems Design'),

    _('Humanities'),
    _('Control Systems'),
    _('Fundamental Electrical Engineering'),
    _('Intellectual Informational Technologies'),
    _('Computational Methods and Programming'),
    _('Informational Technologies in Automated Systems'),

    _('Electronics'),
    _('Micro- and Nanoelectronics'),
    _('Information Radiotechnologies'),

    _('Physics'),
    _('Philosophy'),
    _('Computer Science'),
    _('Higher Mathematics'),
    _('Electronic Computing Facilities'),
    _('Electronic Computing Machines'),
    _('Software for Information Technologies'),

    _('Information Security'),
    _('Infocommunication Technologies'),
    _('Physical Training'),

    _('Economics'),
    _('Management'),
    _('Economic Informatics'),
    _('Foreign Languages No. 2'),

    _('Communication'),
    _('Tactical and General Military Training'),
    _('Radio-Electronic Engineering for Air Force and Air Defence Troops'),

    _('General Subjects'),
))

# TODO: заполнить список специальностей: 1 параметр - код специальности, 2 параметр - название на английском
SPECIALITIES = (
    ('', _('')),
)
