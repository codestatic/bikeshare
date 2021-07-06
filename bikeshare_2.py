import time

import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data from Chicago, New York City, or Washington? ').lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print('Please try again.')
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('What month would you like to filter by? Type all for no filter. ').lower()
        if month != 'all' and month not in ('january', 'february', 'march', 'april', 'may', 'june'):
            print('Please try again.')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('What day would you like to filter by? Type all for no filter. ').lower()
        if day != 'all' and day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print('Please try again.')
        else:
            break

    print('-' * 40)
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
    # loading data from csv file
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)

        df = df[df['month'] == month]

    # filter by day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = df['month'].mode()[0]
    print('The most common month is: ', {months[common_month - 1]})

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day is: ', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour is: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common station to start at is: ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common station to end at is: ', common_end_station)

    # display most frequent combination of start station and end station trip
    start_end_stations = (df['Start Station'] + ' _ ' + df['End Station']).mode([0])
    print('The most frequently used combination of start and end stations is: ', start_end_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print('The total travel time is:', (travel_time / 86400).round(1), 'days.')

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('The average travel time is:', (average_travel_time / 60).round(2), 'minutes.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('Counts of user types:\n', user_type_count)

    # Display counts of gender
    if 'Gender' in df:
        print('Number of male and female riders:\n', df['Gender'].value_counts())

    # Display earliest, recent, and common year of birth
    if 'Birth Year' in df:
        earliest_birth = int(df['Birth Year'].min())
        print('The earliest year of birth is:', earliest_birth)

        recent_birth = int(df['Birth Year'].max())
        print('The most recent birth year is:', recent_birth)

        common_birth = int(df['Birth Year'].value_counts().idxmax())
        print('The most common year of birth is:', common_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


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
