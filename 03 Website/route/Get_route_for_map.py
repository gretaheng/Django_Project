# Main: Get the route for mapping
# Xi Chen
# Original code


import csv
import pandas as pd
import numpy as np
import re
import string

import Choose_safest_route as csr


if __name__ == "__main__":

    # An Sample Test
    user_departure_date = "2018,03,20"
    user_departure_time = "20,45"
    user_mode_option = 'walking'
    departure_location = '900-906 E 53rd St, Chicago, IL 60615'
    destination_location = '5800 S Woodlawn Ave, Chicago, IL 60637'

    # Transfer the user's input date/time into valid type for Google Map API
    depart_time = csr.input_date_time(user_departure_date, 
                                      user_departure_time)
    
    # Get the crime data subset accroding to user's departure time
    loc_weight = csr.get_crime_time_df(user_departure_time)
    
    # Build a dictionary to store all the routes returned from the Google API
    google_route_dict = csr.build_route_dict(departure_location, 
                                             destination_location, 
                                             depart_time, 
                                             user_mode_option)
    
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
                                                   user_mode_option,
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


    # For the purpose of debugging, printing the results
    print()
    print('google_route_dict')
    print(google_route_dict)
    print()
    print('The safest route returned by Google API:')
    print(best_choice)
    print()
    print('enriched_each_step_score')
    print(enriched_each_step_score)
    print()
    print("google_best_route", len(google_best_route))
    print(google_best_route)
    print()
    print("google_route_ls", len(google_route_ls))
    print(google_route_ls)
    print()
    print("enriched_best_route", len(enriched_best_route))
    print(enriched_best_route)
    print()
    print("enriched_route_ls", len(enriched_route_ls))
    print(enriched_route_ls)
    print()
    print("altered_best_route", len(altered_best_route))
    print(altered_best_route)
    print()
    print("altered_route_ls", len(altered_route_ls))
    print(altered_route_ls)
    print()
    print("final_route", len(final_route))
    print(final_route)
    print()
    print("final_route_ls", len(final_route_ls))
    print(final_route_ls)
    print()
