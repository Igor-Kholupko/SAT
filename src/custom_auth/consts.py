from django.utils.translation import ugettext_lazy as _

GROUP_PERMISSIONS = {
    # TODO: написать права для групп
    'students': ('can_view_task_list',
                 'can_view_task'),
    'teachers': ('can_view_task_list',
                 'can_create_task',
                 'can_view_task',
                 'can_edit_task',
                 'can_del_task_list'),
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
