from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import quiz_results,User
from django.http import JsonResponse
import json

# need to add complete paragraphs but added start of each paragraph to make it work
paragraphs = [
    "One of the easiest ways to be more sustainable is to reduce energy consumption at home. Switch to energy-efficient appliances and LED lightbulbs, which use up to 75% less energy than traditional incandescent bulbs. Unplug devices when they are not in use, as many electronics consume energy even when turned off. Additionally, consider using a programmable thermostat to optimize heating and cooling, and take advantage of natural light during the day to reduce the need for artificial lighting.",
    "Water is a precious resource, and conserving it is essential for sustainability. Fix leaky faucets and pipes promptly, as a single drip can waste gallons of water over time. Install low-flow showerheads and faucets to reduce water usage without sacrificing performance. When doing laundry or dishes, always run full loads to maximize efficiency. Outside the home, consider collecting rainwater for gardening and landscaping, and opt for drought-resistant plants to reduce the need for irrigation.",
    "The '3 Rs' of sustainability: Reduce, Reuse, Recycle—are a cornerstone of eco-friendly living. Start by reducing your consumption of single-use items like plastic bags, bottles, and packaging. Reuse whenever possible, such as repurposing glass jars for storage or using cloth bags for shopping. Recycle materials like paper, glass, and metal, but be sure to follow local recycling guidelines to avoid contamination. Composting organic waste is another great way to reduce landfill waste and create soil for gardening.",
    "Transportation is a major contributor to greenhouse gas emissions. To reduce your carbon footprint, opt for walking, biking, or using public transportation whenever possible. If you need to drive, consider carpooling or switching to an electric or hybrid vehicle. For longer trips, choose trains over planes, as trains generally have a lower environmental impact. Additionally, maintaining your vehicle by keeping tires properly inflated and performing regular tune-ups can improve fuel efficiency and reduce emissions.",
    "Making sustainable choices while shopping can significantly reduce your environmental impact. Buy locally produced goods to support local economies and reduce the carbon footprint associated with transportation. Choose products with minimal packaging, or packaging made from recycled materials. When shopping for food, opt for organic and seasonal produce, which often requires fewer pesticides and less energy to grow. Finally, consider buying second-hand items or repairing broken ones instead of purchasing new products.",
    "Your diet plays a significant role in your environmental footprint. Reducing meat and dairy consumption, particularly beef and lamb, can lower greenhouse gas emissions, as livestock farming is a major contributor to climate change. Incorporate more plant-based meals into your diet, such as fruits, vegetables, legumes, and grains. When buying seafood, choose sustainably sourced options to help protect ocean ecosystems. Additionally, avoid food waste by planning meals, storing food properly, and using leftovers creatively."
]



@login_required
def registerScore_view(request):
    data = json.loads(request.body)
    score = int(data['score'])
    user = User.objects.get(id=request.user.id)
    print(score)
    print(user)
    try:
        results = quiz_results.objects.get(user=user,id=1)
    except quiz_results.DoesNotExist:
        results = quiz_results(user=user, best_result=0, previous_best=0, new_result=0)
        results.save()
    high_score = results.best_result
    results.previous_best = high_score
    results.new_result = score
    if score > results.previous_best:
        results.best_result = score
    results.save()
    return JsonResponse({'status': 'success', 'redirect_url': '/guides/results/'})

@login_required
def results_view(request):
    return render(request, 'guides/results.html')

@login_required
def content_view(request):
    return render(request, 'guides/content.html', {'paragraphs': paragraphs})

@login_required
def quiz_view(request):
    return render(request, 'guides/quiz.html')

