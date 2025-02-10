from django.shortcuts import render

# need to add complete paragraphs but added start of each paragraph to make it work
paragraphs = [
    "Sustainability is a key concept that encompasses...",
    "One of the most effective ways to enhance sustainability...",
    "Transportation is a significant contributor to greenhouse gas emissions...",
    "Waste generation is a significant challenge for sustainability...",
    "Diet plays a crucial role in sustainability...",
    "Water is a finite resource, and conservation efforts are necessary...",
    "Sustainable living extends beyond direct environmental choices...",
    "Many common household products contain harmful chemicals...",
    "Gardening is an effective way to contribute to sustainability...",
    "Living a sustainable life requires conscious effort and ongoing commitment..."
]

def content_view(request):
    return render(request, 'guides/content.html', {'paragraphs': paragraphs})

def quiz_view(request):
    return render(request, 'guides/quiz.html')
