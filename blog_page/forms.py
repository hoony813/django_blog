from django import forms

class BlogForm(forms.Form):
    title = forms.CharField(max_length=255, label='제목', error_messages={'required':'제목을 입력해주세요'})
    contents = forms.CharField(widget=forms.Textarea, label='내용', error_messages={'required':'내용을 입력해주세요.'})
    tags = forms.CharField(label='태그',required=False)
    image = forms.ImageField(label='썸네일',required=False)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        contents = cleaned_data.get('contents')

        if not title:
            self.add_error('title','제목을 입력해주세요.')

        if not contents:
            self.add_error('contents', '내용을 입력해주세요.')