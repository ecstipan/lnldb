from django import forms
from django.forms import Form, ModelForm, TextInput
from django.forms.extras.widgets import SelectDateWidget

from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Fieldset,Button,ButtonHolder,Submit,Div,MultiField,Field,HTML
from crispy_forms.bootstrap import AppendedText,InlineCheckboxes,InlineRadios,Tab,TabHolder,FormActions

from events.models import Event,Organization,Category,Extra,Location,Lighting,Sound,Projection
from events.widgets import ExtraSelectorWidget,ValueSelectField
from events.fields import ExtraSelectorField

from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput

import datetime

from ajax_select import make_ajax_field
from ajax_select.fields import AutoCompleteSelectMultipleField,AutoCompleteSelectField

CAT_LIGHTING = Category.objects.get(name="Lighting")
CAT_SOUND = Category.objects.get(name="Sound")
CAT_PROJ = Category.objects.get(name="Projection")

LIGHT_EXTRAS = Extra.objects.filter(category=CAT_LIGHTING)
LIGHT_EXTRAS_ID_NAME = LIGHT_EXTRAS.values_list('id','name')
#LIGHT_EXTRAS_NAMES = [[v[1],HTML("br")] for v in LIGHT_EXTRAS_ID_NAME]
LIGHT_EXTRAS_NAMES = ["e_%s" % v[0] for v in LIGHT_EXTRAS_ID_NAME]

SOUND_EXTRAS = Extra.objects.filter(category=CAT_SOUND)
SOUND_EXTRAS_ID_NAME = SOUND_EXTRAS.values_list('id','name')
#SOUND_EXTRAS_NAMES = [[v[1],HTML("br")] for v in SOUND_EXTRAS_ID_NAME]
SOUND_EXTRAS_NAMES = ["e_%s" % v[0] for v in SOUND_EXTRAS_ID_NAME]

JOBTYPES = (
    (0,'Lighting'),
    (1,'Sound'),
    (2,'Projection'),
)

LIGHT_CHOICES = (
    (1,'L1'),
    (2,'L2'),
    (3,'L3'),
    (4,'L4'),
)

SOUND_CHOICES = (
    (1,'S1'),
    (2,'S2'),
    (3,'S3'),
    (4,'S4'),
)
PROJ_CHOICES = (
    (16,'16mm'),
    (35,'35mm'),
    ('d','Digital'),    
)
class WorkorderSubmit(ModelForm):
    class Meta:
        model = Event
        exclude = ('submitted_by','submitted_ip','approved','crew','crew_chief','report','closed','payment_amount','paid')
    def __init__(self, *args, **kwargs):
        super(WorkorderSubmit,self).__init__(*args,**kwargs)
        self.fields['date_setup_start'].widget = SelectDateWidget()
        #self.fields['datetime_start'].widget = datetime()
        #self.fields['datetime_end'].widget = datetime()
        
        
class CrewChiefAssign(forms.ModelForm):
    crewchief = make_ajax_field(Event,'crew_chief','Users',plugin_options = {'minLength':3})
    class Meta:
        model = Event
        fields = ("crewchief",)        
        
    #crew_chief = AutoCompleteSelectMultipleField('crew_chief',plugin_options = {'minLength':3})
        
        
class CrewAssign(forms.ModelForm):
    crew = make_ajax_field(Event,'crew','Users',plugin_options = {'minLength':3})
    #crewchief = make_ajax_field(Event,'crew_chief','Users',plugin_options = {'minLength':3})
    class Meta:
        model = Event
        fields = ("crew",)

class CrewChiefAssign(forms.ModelForm):
    crew_chief = make_ajax_field(Event,'crew_chief','Users',plugin_options = {'minLength':3})
    class Meta:
        model = Event
        fields = ("crew_chief",)
        
class IOrgForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Contact',
                    Field('name'),
                    'email',
                    'exec_email',
                    'address',
                    'phone',
                ),
                Tab(
                    'Options',
                    'email_exec',
                    'email_normal',
                    'associated_orgs',
                ),
                Tab(
                    'Money',
                    'fund',
                    'organization',
                    'account',
                ),
                Tab(
                    'People',
                    'user_in_charge',
                    'associated_users',
                )
            ),
            FormActions(
                Submit('save', 'Save changes'),
            )
        )
        super(IOrgForm,self).__init__(*args,**kwargs)
    class Meta:
        model = Organization
    #associated_orgs = make_ajax_field(Organization,'associated_orgs','Orgs',plugin_options = {'minLength':2})
    #associated_users = make_ajax_field(Organization,'associated_users','Users',plugin_options = {'minLength':3})
    #user_in_charge = AutoCompleteSelectField('Users')
    associated_orgs = AutoCompleteSelectMultipleField('Orgs',required=False)
    associated_users = AutoCompleteSelectMultipleField('Users',required=False)
class EventApprovalForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('description',label="Description (optional)"),
            HTML('<p class="muted">This will describe the event to your CCs</p>'),
            FormActions(
                Submit('save', 'Approve Event'),
            )
        )
        super(EventApprovalForm,self).__init__(*args,**kwargs)
        
    class Meta:
        model = Event
        fields = ['description',]
class InternalEventForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Name And Location',
                    'event_name',
                    'location',
                    'description',
                ),
                Tab(
                    'Contact',
                    'person_name',
                    'org',
                    ),
                Tab(
                    'Scheduling',
                    Field('datetime_setup_start',css_class='dtp'),
                    Field('datetime_setup_complete',css_class='dtp'),
                    Field('datetime_start',css_class='dtp'),
                    Field('datetime_end',css_class='dtp'),
                ),
                Tab(
                    'Lighting',
                    'lighting',
                    'lighting_reqs'
                ),
                Tab(
                    'Sound',
                    'sound',
                    'sound_reqs'
                ),
                Tab(
                    'Projection',
                    'projection',
                    'proj_reqs'
                    )
            ),
            FormActions(
                Submit('save', 'Save changes'),
            )
        )
        super(InternalEventForm,self).__init__(*args,**kwargs)
    class Meta:
        model = Event

    location = forms.ModelChoiceField(
            queryset = Location.objects.all()
        )
    datetime_setup_start = forms.SplitDateTimeField(initial=datetime.datetime.now()),
    person_name = AutoCompleteSelectField('Users',required=False,plugin_options={'position':"{ my : \"right top\", at: \"right bottom\", of: \"#id_person_name_text\"}"})
    org = AutoCompleteSelectMultipleField('Orgs',required=False)
    
    datetime_setup_start =  forms.SplitDateTimeField(initial=datetime.datetime.now())
    datetime_setup_complete = forms.SplitDateTimeField(initial=datetime.datetime.now())
    datetime_start = forms.SplitDateTimeField(initial=datetime.datetime.now())
    datetime_end = forms.SplitDateTimeField(initial=datetime.datetime.now())
        
        
        
        
        
        
        
        
        
        
        
#FormWizard Forms
class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()


class OrgForm(forms.Form):
    group = forms.CharField()
    group_address = forms.CharField(
            widget=forms.Textarea,
            label = "Group Address",
        )


class SelectForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Name',
                'eventname',
                'location'
            ),
            Fieldset(
                'Services',
                InlineCheckboxes('eventtypes')
                )
        )
        super(SelectForm,self).__init__(*args,**kwargs)
        
    eventname = forms.CharField(
            label = 'Event Name',
            required = True
        )
    
    location = forms.ModelChoiceField(
            queryset = Location.objects.all()
        )
    
    
    eventtypes = forms.MultipleChoiceField(
            error_messages={'required': 'Please Select at least one service \n\r'},
            widget=forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}),
            choices=JOBTYPES,
            label = "",
            required = True
            
        )

    
class LightingForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Basics', ### title
                InlineRadios('lighting',),
                Field('requirements', css_class="span8"),
                ),
            Fieldset(
                'Extras', ### title
                *LIGHT_EXTRAS_NAMES
                ),
        )
        super(LightingForm,self).__init__(*args,**kwargs)
        for extra in LIGHT_EXTRAS:
            self.fields["e_%s" % extra.id] = ValueSelectField(label=extra.name,initial=0)
            
    lighting = forms.ModelChoiceField(
            empty_label=None,
            queryset = Lighting.objects.all(),
            widget = forms.RadioSelect(attrs={'class':'radio'}),
        )   

    requirements = forms.CharField(
            widget=forms.Textarea,
            #widget=BootstrapTextInput(prepend='P',),
            label = "Addtl Lighting Requirements",
            required=False
        )

    #extras = ExtraSelectorField(choices=LIGHT_EXTRAS.values_list('id','name'))
    #for extra in LIGHT_EXTRAS:
        #"e__{{0}}" % extra.id = ValueSelectField(extra)
    
class SoundForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Basics', ### title
                'sound',
                Field('requirements', css_class="span8"),
                ),
            Fieldset(
                'Extras', ### title
                *SOUND_EXTRAS_NAMES
                ),
        )
        super(SoundForm,self).__init__(*args,**kwargs)
        for extra in SOUND_EXTRAS:
            self.fields["e_%s" % extra.id] = ValueSelectField(label=extra.name,initial=0)
    sound = forms.ModelChoiceField(
            empty_label=None,
            queryset = Sound.objects.all(),
            widget = forms.RadioSelect(attrs={'class':'radio'}),
        )   
    requirements = forms.CharField(
            widget=forms.Textarea,
            label = "Sound Requirements",
            required=False
        )
    
class ProjectionForm(forms.Form):
    projection = forms.ModelChoiceField(
            queryset = Projection.objects.all()
        )   
    requirements = forms.CharField(
            widget=forms.Textarea,
            label = "Projection Requirements",
        )
        
class ScheduleForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Setup', ### title
                Field('setup_start',css_class="dtp"),
                Field('setup_complete',css_class="dtp"),
                ),
            Fieldset(
                'Event', ### title
                Field('event_start',css_class="dtp"),
                Field('event_end',css_class="dtp"),
                ),
        )
        super(ScheduleForm,self).__init__(*args,**kwargs)
    setup_start = forms.SplitDateTimeField(initial=datetime.datetime.now())
    setup_complete = forms.SplitDateTimeField(initial=datetime.datetime.now())
    event_start = forms.SplitDateTimeField(initial=datetime.datetime.now())
    event_end = forms.SplitDateTimeField(initial=datetime.datetime.now())
    
    
#helpers for the formwizard
named_event_forms = (
    ('contact',ContactForm),
    ('organization',OrgForm),
    ('select',SelectForm),
    ('lighting',LightingForm),
    ('sound',SoundForm),
    ('projection',ProjectionForm),
    ('schedule',ScheduleForm),
)

named_event_tmpls= {
    'organization':'eventform/org.html',
    'contact':'eventform/contact.html',
    'select':'eventform/select.html',
    'lighting':'eventform/lighting.html',
    'sound':'eventform/sound.html',
    'projection':'eventform/projection.html',
    'schedule':'eventform/schedule.html',
}