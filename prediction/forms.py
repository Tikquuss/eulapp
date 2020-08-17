from django import forms

accept="application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
supported_extension = [".txt", ".md", ".pdf", ".doc", ".docx"] 

class DocumentForm(forms.Form):
    docfile = forms.FileField(
                label='', 
                help_text='',  
                required=False, 
                widget=forms.FileInput(attrs={
                    'accept': ",".join(supported_extension) + "," + accept,
                    'class':"custom-file-input"
                })
            )


