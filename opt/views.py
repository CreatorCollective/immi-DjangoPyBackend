from django.shortcuts import render, HttpResponse
from django.http import HttpResponseNotFound
from .forms import NameForm
from django.views.decorators.csrf import csrf_exempt
from passporteye import read_mrz
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject
import pycountry
from .models import Person 


@csrf_exempt
def index(request):
    try:
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = NameForm(request.POST, request.FILES)
            # check whether it's valid:
            if form.is_valid():
                passport = request.FILES['passport']

                # Parse and extract passport information
                mrz = read_mrz(passport.read())
                # Filter names to only be there until first spacing
                first_name = mrz.names.split(" ")[0]
                last_name = mrz.surname.split(" ")[0]
                gender = mrz.sex  # example M
                country_of_citizenship = pycountry.countries.get(
                    alpha_3=mrz.nationality).name  # example IND to India
                date_of_birth = mrz.date_of_birth  # example 971208
                dob_correct_format = date_of_birth[2:4] + '/' + date_of_birth[4:6] + ('/19' if (int)(
                    date_of_birth[0:2]) >= 50 else '/20') + date_of_birth[0:2]   # example mm/dd/yyyy
                # If it mistakenly parses "<" due to length requirement, remove it
                passport_number = mrz.number.split("<")[0]  # example M7682205<
                country_that_issued_passport = pycountry.countries.get(
                    alpha_3=mrz.country).name  # example IND to India
                passport_expiration_date = mrz.expiration_date  # example 250420
                expiration_correct_format = passport_expiration_date[2:4] + '/' + \
                    passport_expiration_date[4:6] + '/20' + \
                    passport_expiration_date[0:2]   # example mm/dd/yyyy

                reader = PdfReader("i-765.pdf")
                writer = PdfWriter()
                # copy PDF
                for page in reader.pages:
                    writer.add_page(page)
                
                p = Person(first_name=first_name, last_name=last_name,email=form.cleaned_data['email'] if 'email' in form.cleaned_data else "")
                p.save()
                # Fill page 1
                writer.update_page_form_field_values(
                    writer.pages[0], {"Line1a_FamilyName[0]": last_name,
                                    "Line1b_GivenName[0]": first_name}
                )
                # Mark 1a checkbox for OPT reason
                writer_annot_opt_reason = writer.pages[0]["/Annots"][4].get_object()
                writer_annot_opt_reason.update(
                    {
                        NameObject("/V"): NameObject('/1'),
                        NameObject("/AS"): NameObject('/1')
                    }
                )
                # Fill page 2
                writer.update_page_form_field_values(
                    writer.pages[1],
                    {"Line4b_StreetNumberName[0]": form.cleaned_data['mailing_st_number_and_name'],
                    "Pt2Line5_CityOrTown[0]": form.cleaned_data['mailing_city'],
                    "Pt2Line5_State[0]": form.cleaned_data['mailing_state'],
                    "Pt2Line5_ZipCode[0]": form.cleaned_data['mailing_zip_code'],
                    "Line17a_CountryOfBirth[0]": country_of_citizenship,
                    "Line12b_SSN[0]": form.cleaned_data['ssn']}
                )
                writer_annot_address_same = writer.pages[1]["/Annots"][2].get_object()
                writer_annot_address_same.update(
                    {
                        NameObject("/V"): NameObject('/1'),
                        NameObject("/AS"): NameObject('/Y')
                    }
                )

                # Fill gender based on passport
                if gender == 'M':
                    male_writer_annot = writer.pages[1]["/Annots"][16].get_object()
                    male_writer_annot.update(
                        {
                            NameObject("/AS"): NameObject('/Y')
                        }
                    )
                else:
                    female_writer_annot = writer.pages[1]["/Annots"][15].get_object()
                    female_writer_annot.update(
                        {
                            NameObject("/AS"): NameObject('/N')
                        }
                    )

                # Fill marital status. Assume single by default
                marital_status_writer_annot = writer.pages[1]["/Annots"][19].get_object(
                )
                marital_status_writer_annot.update(
                    {
                        NameObject("/V"): NameObject('/1'),
                        NameObject("/AS"): NameObject('/Single')
                    }
                )

                # Fill previously filed form I-765 as no by default
                prev_filed_opt_writer_annot = writer.pages[1]["/Annots"][21].get_object(
                )
                prev_filed_opt_writer_annot.update(
                    {
                        NameObject("/V"): NameObject('/1'),
                        NameObject("/AS"): NameObject('/N')
                    }
                )
                # Fill have received SSN as yes by default
                have_ssn_writer_annot = writer.pages[1]["/Annots"][42].get_object()
                have_ssn_writer_annot.update(
                    {
                        NameObject("/V"): NameObject('/1'),
                        NameObject("/AS"): NameObject('/Y')
                    }
                )

                # Fill page 3
                writer.update_page_form_field_values(
                    writer.pages[2],
                    {
                        "Line18a_CityTownOfBirth[0]": form.cleaned_data['place_of_birth_city'],
                        "Line18b_CityTownOfBirth[0]": form.cleaned_data['place_of_birth_state'],
                        "Line18c_CountryOfBirth[0]": form.cleaned_data['place_of_birth_country'],
                        "Line19_DOB[0]": dob_correct_format,
                        "Line20a_I94Number[0]": form.cleaned_data['i94_number'],
                        "Line20b_Passport[0]": passport_number,
                        "Line20d_CountryOfIssuance[0]": country_that_issued_passport,
                        "Line20e_ExpDate[0]": expiration_correct_format,
                        "Line21_DateOfLastEntry[0]": form.cleaned_data['date_of_last_arrival'],
                        "place_entry[0]": form.cleaned_data['place_of_last_arrival'],
                        "Line23_StatusLastEntry[0]": "F-1 Student",
                        "Line24_CurrentStatus[0]": "F-1 Student",
                        "Line26_SEVISnumber[0]": form.cleaned_data['sevis_number'],
                        "section_1[0]": "C",
                        "section_2[0]": "3",
                        "section_3[0]": "B"})

                # Fill page 4
                writer.update_page_form_field_values(
                    writer.pages[3],
                    {
                        "Pt3Line3_DaytimePhoneNumber1[0]": form.cleaned_data['phone_number'],
                        "Pt3Line5_Email[0]": form.cleaned_data['email'] if 'email' in form.cleaned_data else ""
                    })

                # Mark that filer understands english
                understands_english_writer_anot = writer.pages[3]["/Annots"][5].get_object(
                )
                understands_english_writer_anot.update(
                    {
                        NameObject("/V"): NameObject('/1'),
                        NameObject("/AS"): NameObject('/A')
                    }
                )

                pdfresponse = HttpResponse(content_type='application/pdf')
                pdfresponse["Access-Control-Allow-Origin"] = "*"
                writer.write(pdfresponse)
                pdfresponse['Content-Disposition'] = 'inline;filename=%s_filled_i765.pdf' % first_name

                return pdfresponse
                
            else:
                print (form.errors)
                response = HttpResponseNotFound("Hello, World! We failed the form")
                response["Access-Control-Allow-Origin"] = "*"
                return response
        return render(request, 'opt/index.html', {})
    except Exception as e:
        print(e)
        response = HttpResponseNotFound('<h1>Threw an exception</h1>')
        response["Access-Control-Allow-Origin"] = "*"
        return response