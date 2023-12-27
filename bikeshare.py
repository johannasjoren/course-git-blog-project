import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). Use a while loop to handle invalid inputs
    while True:
        city = input ("Please select a city out of these three choices:\nChicago, New York City or Washington?\n")
        city = city.lower()
        if city in ['chicago', 'new york city', 'washington']:
            print ("Thank you")
            break
    else:
        print ("Sorry, the city name is not valid - please try again.")
        # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please select a month to filter by:\n January, February, March, April, May, June. If you want to include all months please type 'all'\n")
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            print ("Thank you!")
            break
    else: 
        print ("Sorry, your month input is not valid - please try again.")
           
        # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please select a day to filter by:\nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.\n If you want to include all days please type 'all'\n")
        day = day.lower()
        if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print("Thank you!")
            break
        else:
            print("Sorry, your day input is not valid - please try again.")
                  
    print('-'*40)
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
    # load data to dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # change Start Time column into datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # create 3 new columns out of start time - hour start time, day start time and month start time
    df['hour'] = df['Start Time'].dt.hour
    df['day'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
   
    # filter by month if input is not all
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # create new dataframe by the filtered month
        df= df[df['month'] == month]
        
    # filter by day if input is not all         
    if day != 'all':    
        # create new dataframe by the filtered day
        df = df[df['day'] == day.title()]
        
    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    most_common_month = months[most_common_month - 1]
    print('Most common month:', most_common_month)

    # display the most common day of week
    most_common_day = df['day'].mode()[0]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    most_common_day = days[days.index(most_common_day.title())]
    print('Most common day:', most_common_day)

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print('Most common start hour: {}:00'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
          
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print('Most commonly used start station: ', start_station)
    
    # display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print('\nMost commonly used end station: ', end_station)

    # display most frequent combination of start station and end station trip
    start_and_end_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('\nMost common combination of start and end station trip is:', start_and_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_trip_duration, 60)
    hour, minute = divmod(minute, 60)
    print("Total trip duration is: {} hours, {} minutes, and {} seconds.".format(hour, minute, second))

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean())
    minute, second = divmod(mean_travel_time, 60)
    print("Mean travel time is: {} minutes and {} seconds.".format(minute, second))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print("The count per user type are:\n", count_user_types)

    # Display counts of gender
    if "Gender" in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("The count per gender are:\n", gender_counts)
    else:
        print("Gender information is not available in the data you have chosen")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest = int(df['Birth Year'].min())
        print("The earliest year of birth of users is: ", earliest)
        most_recent = int(df['Birth Year'].max())
        print("The latest year of birth of users is: ", most_recent)
        most_common = int(df['Birth Year'].mode()[0])
        print("Most common year of birth of users is ", most_common)
    else:
        print("Birth year information is not available in the data you have chosen")
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while True:
        answer = ['yes', 'no']
        if view_data in answer:
            if view_data == 'yes':
                end_loc = start_loc + 5
                data = df.iloc[start_loc:end_loc, :]
                print(data)
                start_loc += 5
                view_data = input("Do you wish to continue? Enter yes or no: ").lower()
            else:
                break
        else:
            print("Sorry, your answer is not valid. Please write yes or no.")

# Ask user if they want to restart
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

        
                          
    

