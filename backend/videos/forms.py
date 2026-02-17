from django import forms
from core.models import Video

# We define the choices here in the form, not in the model anymore
CATEGORY_CHOICES = [
    ('', 'Select a category'),
    ('productivity', 'Productivity'),
    ('education', 'Education'),
    ('tech', 'Tech'),
    ('study', 'Study'),
    ('other', 'Other'), # This value will trigger the JavaScript
]

class VideoUploadForm(forms.ModelForm):
    # Override the category field to use our new choices and add an ID for JavaScript
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full h-12 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent',
            'id': 'category-select', # We need this ID for our script
        })
    )
    
    # Add a new field for the custom category (it's not part of the model)
    other_category = forms.CharField(
        required=False, # It's only required if 'Other' is selected
        label="Custom Category",
        widget=forms.TextInput(attrs={
            'class': 'w-full h-12 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': 'Please specify your category'
        })
    )

    
    class Meta:
        model = Video
        # --- THIS IS THE CHANGE ---
        # We have removed 'video_format' and 'duration' from this list.
        fields = [
            'title', 'description', 'video_file', 'thumbnail', 
            'category', 'keywords',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full h-12 px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Enter a descriptive title'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'rows': 4, 'placeholder': 'Describe your video...'}),
            'video_file': forms.FileInput(attrs={'class': 'hidden'}),
            'thumbnail': forms.FileInput(attrs={'class': 'hidden'}),
            'category': forms.Select(attrs={'class': 'w-full h-12 px-3 py-2 border border-gray-300 rounded-lg'}),
            'keywords': forms.TextInput(attrs={'class': 'w-full h-12 px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'e.g., python, tutorial'}),
        }

    # This special 'clean' method contains our custom validation logic
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        other_category = cleaned_data.get("other_category")

        if category == "other":
            if not other_category:
                # If they chose "Other" but left the text box empty, raise an error
                self.add_error('other_category', "This field is required when 'Other' is selected.")
            else:
                # If they filled it out, we replace the 'category' value with their custom text
                cleaned_data["category"] = other_category
        return cleaned_data


class VideoEditForm(forms.ModelForm):
     class Meta:
        model = Video
        fields = ['title', 'description', 'thumbnail', 'category', 'keywords', 'video_format', 'duration']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full h-12 px-3 py-2 border border-gray-300 rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'rows': 4}),
            'thumbnail': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0'}),
            'category': forms.TextInput(attrs={'class': 'w-full h-12 px-3 py-2 border border-gray-300 rounded-lg'}),
            'keywords': forms.TextInput(attrs={'class': 'w-full h-12 px-3 py-2 border border-gray-300 rounded-lg'}),
            'video_format': forms.Select(attrs={'class': 'w-full h-12 px-3 py-2 border border-gray-300 rounded-lg'}),
            'duration': forms.NumberInput(attrs={'class': 'w-full h-12 px-3 py-2 border border-gray-300 rounded-lg'}),
        }
