import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}
CALENDAR_MONTHS = {'january': '1', 'february': '2', 'march': '3', 'april': '4', 'may': '5', 'june': '6',
                   'july': '7', 'august': '8', 'september': '9', 'october': '10', 'november': '11', 'december': '12'}
CALENDAR_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month or month number, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month or month number to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # gets user input for city (chicago, new york city, washington).
    while True:
        city = input(
            '\nEnter the city you would like to analyze (Enter either chicago or new york or washington).\n').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('\nPlease Enter Valid City.')

    # gets user input for month (all, january, february, ... , june)
    while True:
        month = input('\nEnter either name of the month or month number in either one or two digit format'
                      '(i.e january=1 or 01, december=12) to filter by month, or "all" to apply no month filter.\n').lower()
        if month in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                     '12', '01', '02', '03', '04', '05', '06', '07', '08', '09']:
            break
        elif month in CALENDAR_MONTHS.keys():
            month = CALENDAR_MONTHS.get(month)
            break
        elif month == 'all':
            break
        else:
            print('\nPlease Enter Valid Month.')

    # gets user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nEnter name of the day of week to filter by, or "all" to apply no day filter.\n').lower()
        if day in CALENDAR_DAYS:
            break
        elif day == 'all':
            break
        else:
            print('\nPlease Enter valid day of week to filter by.')

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month or month number to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA.get(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # filters the dataframe by the selected month
    if month != 'all':
        month = int(month)
        df = df[df['Start Time'].dt.month == month]
    # filters the dataframe by the selected day
    if day != 'all':
        day = day.title()
        df = df[df['Start Time'].dt.day_name() == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    print('\nDisplaying statistics on the most frequent times of travel.\n')

    # displays the most common months
    popular_month = df['Start Time'].dt.month.mode()
    popular_month_string = []
    for month_no in popular_month:
        current_month_no = [month_name for month_name, month_number in CALENDAR_MONTHS.items() if
                            month_number == str(month_no)]
        popular_month_string.extend(current_month_no)

    print('Most common months for the selected data set are:- ' + ', '.join(popular_month_string))

    # displays the most common days of week
    popular_day = df['Start Time'].dt.day_name().mode()
    print('Most common days for the selected data set are:- ' + ', '.join(popular_day))

    # displays the most common start hours
    popular_hour = df['Start Time'].dt.strftime('%I %p').mode()
    print('Most common hours for the selected data set are:- ' + ', '.join(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    print('\nDisplaying statistics on the most popular stations and trip.\n')

    # displays most commonly used start station
    popular_start_station = df['Start Station'].mode()
    print('Most commonly used start stations are:- ' + ', '.join(popular_start_station))

    # displays most commonly used end station
    popular_end_station = df['End Station'].mode()
    print('Most commonly used end stations are:- ' + ', '.join(popular_end_station))

    # displays most frequent combination of start station and end station trip
    df['Start_end_stn_pair'] = df['Start Station'] + ', ' + df['End Station']
    popular_start_end_station_combo = df['Start_end_stn_pair'].mode()
    print('Most frequent combination of start station and end station:- ' + ', '.join(popular_start_end_station_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    print('\nDisplaying statistics on the total and average trip duration.\n')

    # calculate trip duration by subtracting trip end time and trip start time
    df['Trip Duration'] = df['End Time'] - df['Start Time']
    df['Trip Duration'] = df['Trip Duration'] / np.timedelta64(1, 'm')  # convert trip duration to minutes

    # displays total travel time
    total_trip_time = df['Trip Duration'].sum()  # sum all trip duration in minutes
    total_trip_time = pd.to_timedelta(total_trip_time,
                                      unit='m')  # change the format of trip time to readdable format of number of days hh:mm:ss.ssss
    print('Total trip time for the current data set(format days hh:mm:ss.ssss) is:- ' + str(total_trip_time))

    # displays mean travel time
    mean_trip_time = df['Trip Duration'].mean()  # average of all trip duration in minutes
    mean_trip_time = pd.to_timedelta(mean_trip_time,
                                     unit='m')  # change the format of trip time to readdable format of number of days hh:mm:ss.ssss
    print('Mean trip time for the current data set(format days hh:mm:ss.ssss) is:- ' + str(mean_trip_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    print('\nDisplaying statistics on bikeshare users.')

    # Displays counts of user types
    print('\nLet\'s analyze User Type Column Values.\n')
    if 'User Type' in df.columns:
        user_types = pd.DataFrame(
            df['User Type'].value_counts(dropna=False).rename_axis('User Type').reset_index(name='Records'))
        for index, row in user_types.iterrows():
            if str(row['User Type']) == 'nan':
                print('Number of Records whose User Type is missing = ' + str(row['Records']))
            else:
                print('Number of Records whose User Type is ' + str(row['User Type']) + ' = ' + str(row['Records']))
    else:
        print('\nThe column User Type does not exist in the current data set selected.')

        # Displays counts of gender
    print('\nLet\'s analyze Gender Column Values.\n')
    if 'Gender' in df.columns:
        genders = pd.DataFrame(
            df['Gender'].value_counts(dropna=False).rename_axis('Genders').reset_index(name='Records'))
        for index, row in genders.iterrows():
            if str(row['Genders']) == 'nan':
                print('Number of Records whose gender value is missing = ' + str(row['Records']))
            else:
                print('Number of Records whose gender value is ' + str(row['Genders']) + ' = ' + str(row['Records']))
    else:
        print('\nThe column Gender does not exist in the current data set selected.')

    # Displays earliest, most recent, and most common year of birth
    print('\nLet\'s analyze Birth Year Column Values.\n')
    if 'Birth Year' in df.columns:
        popular_birth_year = df['Birth Year'].mode().tolist()
        max_birth_year = df['Birth Year'].max()
        min_birth_year = df['Birth Year'].min()
        print('Most common Birth Years:- ' + ', '.join(str(year) for year in popular_birth_year))
        print('Most recent Birth Year:- ' + str(max_birth_year))
        print('Most earliest Birth Year:- ' + str(min_birth_year))
    else:
        print('\nThe column Birth Year does not exist in the current data set selected.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # prompts user to display 5 rows of data at a time
        while True:
            display_first_five_rows = input('\nWould you like to view the first 5 rows? Enter yes or no.\n').lower()
            if display_first_five_rows in ['yes', 'no']:
                if display_first_five_rows == 'yes':
                    x, y = 0, 5
                    print('\nDisplaying the first 5 rows of the selected data set.\n')
                    print(df[x:y])
                    while True:
                        display_next_five_rows = input(
                            '\nWould you like to view the next 5 rows? Enter yes or no.\n').lower()
                        if display_next_five_rows in ['yes', 'no']:
                            if display_next_five_rows == 'yes':
                                x = y
                                y = y + 5
                                print('\nDisplaying the next 5 rows of the selected data set.\n')
                                print(df[x:y])
                            else:
                                break
                        else:
                            print('\nPlease Enter Valid input.')
                    break
                else:
                    break
            else:
                print('\nPlease Enter Valid input.')

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()


