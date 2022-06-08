from django import forms
from blog.models import Comment,Post,Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_no', 'bio', 'facebook', 'instagram', 'linkedin', 'image', )
class PostForm(forms.ModelForm):
#So those are my two widgets and this is the main idea of how you connect specific widgets to styling.
    class Meta():
        model = Post
        fields =('title','text','image')

        widgets={
        'title':forms.TextInput(attrs={'class':'textinputclass'}),
        'text' :forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})#postcontent,textinputclass is our own class
                                                                                         #editable and medium editor text area are imported css which kind of gives it the styling of the actual medium editor.
                }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields =('text',)

        widgets={

        'text' :forms.Textarea(attrs={'class':'editable medium-editor-textarea'})#postcontent,textinputclass is our own class
                                                                                         #editable and medium editor text area are imported css which kind of gives it the styling of the actual medium editor.
                }
