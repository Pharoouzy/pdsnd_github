import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv' 
}


months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

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
        city = input("Would you like to see data for Chicago, New York City, or Washington?: ").lower().strip()
        if city in CITY_DATA.keys():
            break
        print(f"Invalid input: [{city}]. Please select a valid city.")


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month? January, February, March, April, May, June or type 'all' if you do not have any preference? ").lower().strip()
        if month in months:
            break
        print(f"Invalid input: [{month}]. Please select a valid month or 'all'.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input('Which day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday. Type "all" for no time filter. ').lower().strip()
        if day in days:
            break
        print(f"Invalid input: [{day}]. Please select a valid day or 'all'.")

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
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time to datetime format for easier extraction
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_num = months.index(month) + 1
        df = df[df['month'] == month_num]
        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
        
    return df

def display_raw_trip_data(df):
    """
        Display raw trip data upon user request.
        
        Args:
        df - Pandas DataFrame containing city data

        Returns:
        None
    """
    start_index = 0
    end_index = 5
    display_more = True
    data_per_row = 5

    while display_more:
        df.rename(columns={df.columns[0]: 'ID'}, inplace=True)
        if start_index >= len(df):
            print("No more data to display.")
            break

        # Ask the user if they want to continue
        user_input = input("\nWould you like to view next 5 raw trip data? Enter yes or no.\n").lower()
        if user_input == 'yes':
            print(df.iloc[start_index:end_index].to_json(orient='records'))
            start_index += data_per_row
            end_index += data_per_row
        elif user_input == 'no':
            display_more = False
        else:
            print(f"Invalid input: [{user_input}]. Please enter 'yes' or 'no'.")

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print(f"Most Common Month: {months[popular_month - 1].title()}")


    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day: {popular_day.title()}")

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {popular_hour}")


    display_elapsed_time(start_time)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"Most commonly used start station: {common_start_station}")

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"Most commonly used end station: {common_end_station}")

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print(f"Most frequent trip (from start station to end station): {common_trip}")

    display_elapsed_time(start_time)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_time} seconds")


    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print(f"Average travel time: {mean_time} seconds")

    display_elapsed_time(start_time)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"Counts of user types:\n{user_types}\n")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f"Counts of gender:\n{gender_counts}\n")


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        
        print(f"Earliest year of birth: {int(earliest_year)}")
        print(f"Most recent year of birth: {int(most_recent_year)}")
        print(f"Most common year of birth: {int(most_common_year)}")


    display_elapsed_time(start_time)

def user_segmentation_analysis(df):
    """Displays bikeshare user segmentation analysis."""
    
    print('\nCalculating User Segmentation Analysis...\n')
    start_time = time.time()

    user_types = df['User Type'].unique()

    for user_type in user_types:
        users_by_type = df[df['User Type'] == user_type]
        num_users = len(users_by_type)
        avg_trip = users_by_type['Trip Duration'].mean()
        print(f'Number of trips by {user_type}: {num_users}')
        print(f'Average trip duration by {user_type}: {avg_trip:.2f} seconds')

    display_elapsed_time(start_time)

def age_demographics(df):
    """Displays age demographics of bikeshare users."""
    
    if 'Birth Year' in df.columns:
        print('\nCalculating Age Demographics...\n')
        start_time = time.time()

        current_year = pd.Timestamp.now().year
        df['Age'] = current_year - df['Birth Year']

        age_bins = [18, 25, 35, 45, 55, 65, 100]
        age_labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        
        df['Age Group'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)
        
        age_group_counts = df['Age Group'].value_counts().sort_index()

        # Print the results
        for group, count in age_group_counts.items():
            print(f'Number of users in age group {group}: {count}')

        display_elapsed_time(start_time)

def weekday_vs_weekend_usage_stats(df):
    """Displays bikeshare weekday vs weekend usage stats."""
    
    print('\nCalculating Weekday vs Weekend Usage...\n')
    start_time = time.time()

    df['Weekday'] = df['Start Time'].dt.weekday
    weekdays = df[df['Weekday'] < 5] # 0-4 represents Monday to Friday
    weekends = df[df['Weekday'] >= 5]  # 5-6 represents Saturday and Sunday
    
    total_duration_weekdays = weekdays['Trip Duration'].sum()
    total_duration_weekends = weekends['Trip Duration'].sum()
    avg_duration_weekdays = weekdays['Trip Duration'].mean()
    avg_duration_weekdays = 0 if pd.isna(avg_duration_weekdays) else avg_duration_weekdays
    avg_duration_weekends = weekends['Trip Duration'].mean()
    avg_duration_weekends = 0 if pd.isna(avg_duration_weekends) else avg_duration_weekends

    print(f'Total trip duration on weekdays: {total_duration_weekdays:.2f} seconds')
    print(f'Average trip duration on weekdays: {avg_duration_weekdays:.2f} seconds')
    print(f'Total trip duration on weekends: {total_duration_weekends:.2f} seconds')
    print(f'Average trip duration on weekends: {avg_duration_weekends:.2f} seconds')

    display_elapsed_time(start_time)


def display_elapsed_time(start_time):
    """Displays the elapsed time since the provided start time."""
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
        user_segmentation_analysis(df)
        age_demographics(df)
        weekday_vs_weekend_usage_stats(df)
        display_raw_trip_data(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower().strip()
            if restart in ['yes', 'no']:
                break
            print("Invalid input. Please enter 'yes' or 'no'.")
        if 'no' == restart:
            break


if __name__ == "__main__":
	main()
