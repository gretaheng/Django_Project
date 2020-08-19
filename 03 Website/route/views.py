# Jie Heng
# Original code (algorithm part is direct copy from Xi's code)
# Reference: https://stackoverflow.com/questions/27753574/python-remove-first-number-from-string-if-its-0

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response,redirect
import datetime, json
from django.urls import reverse
from django import forms
from django.contrib import messages
from route.checkplace import *
import route.Choose_safest_route as csr


def index(request):
    return render(request, 'route/index.html')

# Reference:
# https://stackoverflow.com/questions/27753574/python-remove-first-number-from-string-if-its-0
def map(request):
    '''
    Get users input and show routes on route/map.html.

    If users provide an invlid address, they will be redirect to route/index.html and receive an error message.
    The algorithm only works on future dates and time, so we set default values as current time and dates. If users
    choose past time and date, we will use the default values.

    Returns:
         pts: a list of waypoints that a safe route will pass
         mode_option: choosen mode option
    '''
    origin = request.GET['origin']
    # check if address valid
    origin = check(origin)[0]
    destin = request.GET['destination']
    # check if address valid
    destin = check(destin)[0]
    # show message
    if not destin or not origin:
        messages.error(request, 'Please enter a valid address.')
        return HttpResponseRedirect( reverse('type') )
    if destin==origin:
        messages.error(request, 'Please enter different addresses for origin place and destination.')
        return HttpResponseRedirect( reverse('type') )
    else:
        org_geo = check(origin)[1]
        des_geo = check(destin)[1]

    mode_option = request.GET['mode']

    # check if user_date and user_time are future dates and time
    user_date = request.GET['user_date'].replace("-", ",")
    today = datetime.datetime.now().strftime('%Y,%m,%d')
    user_time = request.GET['user_time'].replace(":", ",")
    right_moment = datetime.datetime.now().strftime('%H,%M')
    if not user_time:
        user_time = right_moment
    if not user_date:
        user_date = today
    if user_date <= today:
        user_date = today
        if user_time < right_moment:
            user_time = right_moment
    # delete start 0 for time
    user_time = user_time[0].strip('0') + user_time[1:]

    pts = org_geo

    # Transfer the user's input date/time into valid type for Google Map API
    depart_time = csr.input_date_time(user_date,
                                      user_time)

    # Get the crime data subset accroding to user's departure time
    loc_weight = csr.get_crime_time_df(user_time)

    # Build a dictionary to store all the routes returned from the Google API
    google_route_dict = csr.build_route_dict(origin,
                                             destin,
                                             depart_time,
                                             mode_option)

    # Construct the enriched route by adding mid-steps to the locations
    # that have a long distance
    enriched_route_dict = csr.enrich_routes_steps(google_route_dict)

    # Compare the dangerous score for each enriched route, get the safest one
    best_choice, enriched_best_route, best_score = csr.compare_routes(
        loc_weight,
        enriched_route_dict)

    # Get the safest route returned from the Google Map API
    google_best_route = google_route_dict[best_choice]

    # Get the dangerous score for each step at the safest enriched route
    enriched_each_step_score = csr.get_each_step_score(loc_weight,
                                                       enriched_best_route)

    # Construct the alternative safest route if part(s) of the enriched route
    # is dangerous
    altered_best_route = csr.find_alternative_step(enriched_each_step_score,
                                                   depart_time,
                                                   mode_option,
                                                   loc_weight)

    # Construct the final route which would be displayed in the website's map
    final_route = csr.get_route_for_map(google_best_route,
                                        enriched_best_route,
                                        altered_best_route)

    # Change the types of the routes for the purpose of displaying requirement
    # in the website's map
    google_route_ls = csr.transfer_tuple_to_list(google_best_route)
    enriched_route_ls = csr.transfer_tuple_to_list(enriched_best_route)
    altered_route_ls = csr.transfer_tuple_to_list(altered_best_route)
    final_route_ls = csr.transfer_tuple_to_list(final_route)

    pts += final_route_ls
    pts += des_geo
    # google javascript api takes uppercase mode option, whereas direction api takes lowercase.
    mode_option = mode_option.swapcase()
    return render(request, 'route/map.html', {'pts':pts,'mode_option': mode_option})
