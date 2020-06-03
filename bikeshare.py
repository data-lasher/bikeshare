import time
import pandas as pd
import sys 

''' Global dictionaries and variables '''

days = {'1':'Monday', '2':'Tuesday', '3':'Wednesday', '4':'Thursday', 
        '5':'Friday', '6':'Saturday', '7':'Sunday', '0':'----'}          
months = {'1':'January', '2':'February', '3':'March', '4':'April', 
          '5':'May', '6':'June', '7':'July', '8':'August', 
          '9':'September', '10':'October', '11':'November', '12':'December', '0':'----'}           
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

''' formating for graphical elements '''
# draw horizontal line
def pline():
    print('-' * 52)
# draw side lines
def pside():
    print('|                                                  |')
# draw centered text with borders    
def ptext(texter):
    text_lenght = len(texter)
    
    # text odd lenght
    if text_lenght % 2 != 0:
        space1 = int((50 - text_lenght)/2)
        space2 = int(space1 + 1)
    # text even    
    else:
        space1 = int((50 - text_lenght)/2)
        space2 = int(space1)
        
    print('|' + (' ' * space1) + texter + (' ' * space2) + '|')
   

def invalid_option_msg():
    ''' standard message for wrongly formated user input.''' 
    print("\n*** Please enter a valid option. ***")

def timer_printer (start_time) :
    '''  takes time, calculates difference and return calculation time message '''
    timer = time.time() - start_time
    ptext("Calculation time: {} seconds.".format ("{:.10f}".format(timer)))
    
def num_format(num):
    ''' returns number formated with commas '''
    return "{:,}".format(num)    

def month_filter_select():
    """ month filter handler -- setup to handle 12 months for future growth""" 
   
    month_valid = False
    while not month_valid:
        print("\n")
        pline()
        ptext('Month Selection')
        pline()
        ptext('      1 - January   5 - May      9 - September    ')
        ptext('      2 - February  6 - June    10 - October      ')
        ptext('      3 - March     7 - July    11 - November     ')
        ptext('      4 - April     8 - August  12 - December     ')
        pline()
    
        try:
            month_input = int(input("\nEnter the number corresponding to the month \nyou want to look up: "))
            
            if month_input >= 1 and month_input <= 6:   
                month_valid = True
            # currently data only availabel jan - jun     
            elif month_input >= 7 and month_input <= 12:
                print("\n*** At this time data is only available from January to June. ***")
            else: 
                invalid_option_msg()
        except:
            invalid_option_msg()

    return month_input        

def day_filter_select():
    ''' handler for day of week filter'''    
    day_valid = False
        
    while not day_valid:
        print("\n")
        pline()
        ptext('Day of Week Selection')
        pline()
        ptext('     1 - Monday    4 - Thursday  6 - Saturday    ')
        ptext('     2 - Tuesday   5 - Friday    7 - Sunday      ')
        ptext('     3 - Wednesday                               ')
        pline()
        
        try:
            day_input = int(input("Enter the number corresponding to the day \nyou want to look up: "))             
            
            if day_input >= 0 and day_input <= 7:
                day_valid = True
            else: 
                invalid_option_msg()
        except:   
            invalid_option_msg()    

    return day_input
           
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    pline()
    ptext('US Bikeshare Data Utility')
    pline()
    
    """ city selector handler"""
    city_valid = False

    while not city_valid:
        city_char = input ("Enter the first letter of the city you \nwant to look up: [C]hicago, [N]ew York, [W]ashington: ")
        
        if city_char.lower() ==  'c':
            city_valid = True
            city = 'chicago'
        elif city_char.lower() == 'n':
            city_valid = True
            city = 'new york'
        elif city_char.lower() == 'w':
            city_valid = True
            city = 'washington'
        else:
            invalid_option_msg()
        
    request_filter = False
    while not request_filter:
      
        pline()
        ptext('Data Filters')
        pline()
        print('|             [N]one     [D]ay of week             |')
        print('|             [M]onth                              |')
        print('|             [B]oth - Month & Day                 |')
        pline()

        selected_filter = input("Enter the corresponding letter to apply a filter to results: ")
        
        if selected_filter.lower() == 'm':
            request_filter = True
            month = month_filter_select()
            day = 0
 
        elif selected_filter.lower() == 'd':
            request_filter = True  
            day = day_filter_select()
            month = 0
            
        elif selected_filter.lower() == 'b':
            month = month_filter_select()
            day = day_filter_select()
            request_filter = True
        
        elif selected_filter.lower() == 'n':
            request_filter = True
            month, day = 0, 0
        else:
            invalid_option_msg()
        
    return city, month, day
   
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # file name from dictionary
    filename = CITY_DATA[city]
    # load data file into a dataframe
    df = pd.read_csv(filename, header=0, sep=',')
    
    # convert the Start Time and end time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    #combine stations to create trip start - end column
    df['station_combo'] = df['Start Station'] + ' \n|                to ' + df ['End Station']
   
    
    #filter the dataframe based on filter selection
    if month != 0 and day == 0:  # month filter active
        is_month = df['month'] == month
        df = df[is_month]
    
    elif month == 0 and day != 0:  #day filter active
        is_day = df['day_of_week'] == day
        df = df[is_day]
    
    elif month!= 0 and day != 0: #both filters active
        is_both = ((df['day_of_week'] == day) & (df['month'] == month))
        df = df[is_both]

    pline()
    ptext('Query Results')
    pline()
    ptext('Active Filters') # message to highlight which filters were selected
    pside()
    ptext('City: {}  Month: {}  Day: {}'.format(city.capitalize(), months.get(str(month)), days.get(str(day))))   
    pline()
    ptext(str(len(df.index)) + " records returned by these filter(s).")
    pline()
    
    return df

def time_stats(df, month, day):
        
    """Displays statistics on the most frequent times of travel based on selected filters"""
    start_time = time.time()
          
    ptext('Most Frequent Times of Travel:')
    pside()
        
    popular_hour = df.loc[:,'hour'].mode().iloc[0]
    print('|   Most popular start hour is: {}:00'.format(popular_hour))
    
    if day == 0:   
        popular_day = df.loc[:,'day_of_week'].mode().iloc[0]
        print('|   Most popular day of week is: {}'.format(days.get(str(popular_day))))
    
    if month == 0:
        popular_month = df.loc[:,'month'].mode().iloc[0]
        print ('|   Most popular Month is: {}'.format(months.get(str(popular_month))))

    pside()
    timer_printer(start_time)
    pline()

def station_stats(df):
    """ display most popular stations and trip base."""

    ptext('Most Popular Stations and Trip:')
    start_time = time.time()
     
    popular_start_loc = df.loc[:,"Start Station"].mode().iloc[0]
    print ('| Start station: {}'.format(popular_start_loc))
    popular_end_loc = df.loc[:,"End Station"].mode().iloc[0]
    print ('|   End station: {}'.format(popular_end_loc))
    popular_station_combo = df.loc[:,"station_combo"].mode().iloc[0]
    print ('|          Trip: {}'.format(popular_station_combo))
    pside()      
    timer_printer(start_time)
    pline()

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    formated for hours minutes seconds"""
    
    ptext('Trip Duration:')
    start_time = time.time()

    # display total travel time
    tminutes = int(df['Trip Duration'].sum())
    thours = int(tminutes / 60)
    thours = num_format(thours)   
    minutes_remaining = (tminutes % 60)
    total_time = " {} hrs and {} mins".format(str(thours),  str(minutes_remaining))
    print ('| Total travel time: {}'.format(str(total_time)))
    
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_time_print = num_format(int(mean_time))
    total_seconds = mean_time * 60
    remain_second = int(total_seconds % 60)
    print ('|  Mean travel time: {} mins and {} secs'.format(str(mean_time_print), str(remain_second)))
    pside()
    timer_printer(start_time)
    pline()

def user_stats(df, city):
    """Bikeshare user summary:"""

    ptext('User demographics:')
    start_time = time.time()

    if city != "washington":
        
        # Display counts of gender
        dfg = df['Gender']
        
        n_values = dfg.value_counts() 
        val_0 = num_format(n_values[0])
        val_1 = num_format(n_values[1])
        
        print ('|    ' + n_values.index[0] + ": " + str(val_0))
        print ('|    ' + n_values.index[1] + ": " + str(val_1))
        
        # Display earliest, most recent, and most common year of birth
        recent = df.loc[:,"Birth Year"].max()
        print ('|    Most recent birth year: {}'.format (int(recent)))
        earliest = df.loc[:,"Birth Year"].min()
        print ('|    Earliest birth year:    {}'.format (int(earliest)))
        popular_year = df.loc[:,"Birth Year"].mode()
        print ('|    Most common birth year: {}'.format (int(popular_year)))
    
    else:
        print ("|   Data not available for the city of {} .".format(city.capitalize()))
    
    pside()    
    timer_printer(start_time)
    pline()

def display_records(df, city):
    
    filename = CITY_DATA[city]
    # set display to show all columns
    pd.set_option('display.max_columns', None)
    #reload csv file to avoid showing altered columns
    df = pd.read_csv(filename, header=0, sep=',') 
    #get number of indexes in file
    max_index = len(df.index)
    i_start, i_end = 0, 5
    print (df[:5])

    inner_menu = True
    while inner_menu == True:
        
        next_record = input('Press [any key] to see the next 5 records or [Q]uit: ')

        if next_record.lower() != 'q':
            try:
                i_start += 5
                i_end += 5
                #load next 5 records
                if i_start > max_index:
                    i_start = max_index
                if i_end > max_index:
                    i_end = max_index
                    
                print(df[i_start:i_end]) 
            except:
                print("Error accessing data.")
        
        elif next_record.lower() == 'q':
            inner_menu = False
        
    menu = True
    while menu == True:    
        
        #menu to generate new query or exit program
        restart = input('Select a menu option:  [N]ew Query  [E]xit Program: ')
        
        if restart.lower() == 'n':
            menu = True
            main()
        elif restart.lower() == 'e':
            menu = False
            inner_menu = False
            sys.exit(0)
        else:
            invalid_option_msg()

def main():
    menu = True
    while menu == True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        #menu for new query, view records or exit program
        restart = input('Select a menu option:\n[N]ew Query  [V]iew records  [E]xit Program: ')
        
        if restart.lower() == 'n':
            menu = True
        elif restart.lower() == 'v':
            pline()
            display_records (df, city)
            menu = False
        elif restart.lower() == 'e': 
            menu = False
            sys.exit(0)
        else:
            invalid_option_msg
        
if __name__ == "__main__":
	main()
