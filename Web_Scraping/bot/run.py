from booking.booking import Booking


try:
    with Booking(teardown=False) as bot:

        #a = 2 / 0
        bot.land_first_page()
        #bot.change_currency("USD")
        bot.choose_city("New York")
        bot.select_dates('2026-08-19', '2026-09-09')
        bot.select_adults(5)
        bot.search_button()
        bot.apply_filterations()
        bot.report_results()
        input('press enter to close')

except Exception as e:
    if "in PATH" in str(e):
        print('You are trying to run the bot from command line \n'
              'Please add to PATH your Selenium Drivers \n'
              'Windows:\n(set PATH=%PATH%;C:path-to-your-folder)\n'
              'Linux:\n(PATH=$PATH;/path/toyour/folder/)\n')
    else:
        raise

