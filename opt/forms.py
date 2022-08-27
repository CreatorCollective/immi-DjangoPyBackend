from django import forms

class NameForm(forms.Form):
    # Place of birth
    place_of_birth_city = forms.CharField(label="Enter your city of birth: ")
    place_of_birth_state = forms.CharField(label="Enter your state of birth: ")
    place_of_birth_country = forms.CharField(label="Enter your country of birth: ")

    # Mailing Address
    mailing_st_number_and_name = forms.CharField(label="Enter street number and name: ")
    mailing_city = forms.CharField(label="Enter mailing city: ")
    mailing_state = forms.CharField(label="Enter state: ")
    mailing_zip_code = forms.CharField(label="Enter zip code: ")

    ssn = forms.CharField(label="Enter your SSN")
    i94_number = forms.CharField(label="Enter your I-94 number")
    date_of_last_arrival = forms.CharField(label="Enter date when you last arrived in US")
    place_of_last_arrival = forms.CharField(label="Enter place you last arrived from")
    sevis_number = forms.CharField(label="Enter your sevis number")
    phone_number = forms.CharField(label="Enter your phone number: ")
    email = forms.CharField(label="Enter your e-mail address", required=False)
    passport = forms.FileField()