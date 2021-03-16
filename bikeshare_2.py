import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:

        get_city = input('to explore some US bikeshare data! Would you like to see data about Chicago, New York, or Washington?')
        if get_city.lower() in ('chicago', 'new york', 'washington'):
            if get_city.lower() == 'chicago':
                city = CITY_DATA['chicago']

            elif get_city.lower() == 'new york':
                city = CITY_DATA['new york']
            elif get_city.lower() == 'washington':
                city = CITY_DATA['washington']
            break
        print('Enter a valid city name provided in the options')

    # get user input for month (all, january, february, ... , june)
    months = ('january', 'february', 'march', 'april', 'may', 'june','all')
    while True:
        month = input('\nWhich month you want to filter? January, February, March, April, May, June, or all?\n')
        if month.lower() in months:
            break
        print('Enter a valid month name provided in the options')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    weekdays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday ','all')
    # ask for the week day of choice
    while True:
        try:
            get_day = int(input(
                '\nWhich day? Please type your response as an integer. if you want all input 7\nE.g. Monday:0, Tuesday:1,wednesday:2,thursday:3,friday:4,saturday:5,sunday:6.'))
            if get_day in np.arange(0, 8, 1, 'int'):
                day = weekdays[get_day]
                break
        except:
            print('Enter a valid day as an integer:')


        print('Enter a valid day as an integer:')

    print('-'*80)
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
    # load data file into a dataframe
    df = pd.read_csv(city)
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df['User Type'].value_counts()
    print("users types")
    print(user_types)

    # Display counts of gender

    if city !='washington.csv':
        gender = df['Gender'].value_counts()
        print("genders")
        print(gender)
        # Display earliest, most recent, and most common year of birth
        # earliest user
        earliest_user = int(df['Birth Year'].min())
        # latest user
        latest = int(df['Birth Year'].max())
        # most common user's year of birth
        mode = int(df['Birth Year'].mode())
        print('The oldest users are born in {}.\nThe youngest users are born in {}.'
              '\nThe most common user\'s year of birth  is {}.'.format(earliest_user, latest, mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('The total trip duration is {} .'.format(total_duration))
    # display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    print('The  average trip duration is {} .'.format(average_duration))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_ss = df['Start Station'].mode().to_string(index=False)
    print('The  most commonly used start station is {}.'.format(common_ss))

    # display most commonly used end station
    common_es = df['End Station'].mode().to_string(index=False)
    print('The  most commonly used End station is {}.'.format(common_es))

    # display most frequent combination of start station and end station trip
    df['journey'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    common_trip = df['journey'].mode().to_string(index=False)
    print('The  most frequent combination of start station and end station trip is {}.'.format(common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month=='all':
        popular_month = df['month'].mode()[0]

        print('Most Popular month is :', popular_month)
    else:
        print('your data is fillterd for only {} '.format(month))

    # display the most common day of week
    if day=='all':
        popular_day = df['day_of_week'].mode()[0]

        print('Most Popular day is :', popular_day)
    else:
        print('your data is fillterd for only {} '.format(day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def display_data (df):
    """Displays rows of the data ."""
    print('\nDisplays rows of the data ...\n')
    head = 0
    tail = 5
    print(df[df.columns[0:-1]].iloc[head:tail])
    while True:
        display = input('\nWould you like to view more 5 rows of the data? '
                        'Type \'yes\' or \'no\'.\n')
        if display.lower() in ('no','yes'):
            if display=='yes':
                head += 5
                tail += 5
                print(df[df.columns[0:-1]].iloc[head:tail])
            elif display.lower() == 'no':
                break
        else:
            print('\nnot valied input? ')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart.lower() not in ['yes', 'no']:
            restart = input("Invalid input. Please type 'yes' or 'no'.")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
